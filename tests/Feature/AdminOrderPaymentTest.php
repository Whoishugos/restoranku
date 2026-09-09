<?php

use App\Models\Order;
use App\Models\Role;
use App\Models\User;
use App\Services\MidtransService;

function staffUser(string $roleName = 'admin'): User
{
    $role = Role::firstOrCreate(
        ['role_name' => $roleName],
        ['description' => ucfirst($roleName)]
    );

    return User::factory()->create(['role_id' => $role->id]);
}

function customerOrder(array $overrides = []): Order
{
    $role = Role::firstOrCreate(
        ['role_name' => 'customer'],
        ['description' => 'Pelanggan']
    );
    $customer = User::factory()->create(['role_id' => $role->id]);

    return Order::create(array_merge([
        'order_code' => 'ORD-5-'.uniqid(),
        'user_id' => $customer->id,
        'subtotal' => 20000,
        'tax' => 2000,
        'grand_total' => 22000,
        'status' => 'pending',
        'kitchen_status' => Order::KITCHEN_WAITING,
        'table_number' => 5,
        'payment_method' => 'tunai',
        'note' => null,
    ], $overrides));
}

test('halaman admin menampilkan kolom saat pembayaran kosong jika belum lunas', function () {
    $admin = staffUser();
    $order = customerOrder();

    $this->actingAs($admin)
        ->get(route('orders.index'))
        ->assertOk()
        ->assertSee('Saat Pembayaran')
        ->assertSee('Status Pembayaran')
        ->assertSee('Menunggu pembayaran')
        ->assertSee($order->order_code);

    $this->actingAs($admin)
        ->get(route('orders.show', $order))
        ->assertOk()
        ->assertSee('Saat Pembayaran:')
        ->assertSee('Menunggu pembayaran');
});

test('konfirmasi tunai mengisi saat pembayaran di daftar dan detail admin', function () {
    $this->travelTo(now()->setTime(9, 45));

    $admin = staffUser();
    $order = customerOrder();

    $this->actingAs($admin)
        ->post(route('orders.confirmPayment', $order))
        ->assertRedirect(route('orders.index'));

    $order->refresh();
    expect($order->isPaid())->toBeTrue();
    expect($order->paid_at)->not->toBeNull();
    expect($order->paidAtLabel())->toBe($order->paid_at->format('d-m-Y H:i'));

    $this->actingAs($admin)
        ->get(route('orders.index'))
        ->assertOk()
        ->assertSee('Pembayaran diterima')
        ->assertSee($order->paidAtLabel());

    $this->actingAs($admin)
        ->get(route('orders.show', $order))
        ->assertOk()
        ->assertSee('Saat Pembayaran: '.$order->paidAtLabel())
        ->assertSee('Pembayaran diterima');

    $this->actingAs($admin)
        ->get(route('orders.nota', $order))
        ->assertOk()
        ->assertSee('Dibayar')
        ->assertSee($order->paidAtLabel());
});

test('webhook midtrans mengisi saat pembayaran dari waktu transaksi', function () {
    $admin = staffUser();
    $order = customerOrder([
        'payment_method' => 'qris',
        'order_code' => 'ORD-QRIS-'.uniqid(),
    ]);

    $midtrans = Mockery::mock(MidtransService::class);
    $midtrans->shouldReceive('isConfigured')->andReturn(true);
    $midtrans->shouldReceive('notification')->andReturn((object) [
        'order_id' => $order->order_code,
        'transaction_status' => 'settlement',
        'fraud_status' => 'accept',
        'payment_type' => 'qris',
        'transaction_time' => '2026-09-09 08:15:00',
    ]);
    $this->instance(MidtransService::class, $midtrans);

    $this->post(route('midtrans.notification'))
        ->assertOk()
        ->assertSee('OK');

    $order->refresh();
    expect($order->isPaid())->toBeTrue();
    expect($order->paidAtLabel())->toBe('09-09-2026 08:15');

    $this->actingAs($admin)
        ->get(route('orders.index'))
        ->assertOk()
        ->assertSee('09-09-2026 08:15')
        ->assertSee('Pembayaran diterima');
});

test('markAsPaid tidak menimpa saat pembayaran yang sudah tersimpan', function () {
    $order = customerOrder();
    $firstPaidAt = now()->subHour();
    $order->markAsPaid($firstPaidAt);

    $order->markAsPaid(now());

    expect($order->fresh()->paid_at->format('Y-m-d H:i:s'))->toBe($firstPaidAt->format('Y-m-d H:i:s'));
});

test('laporan excel menyertakan kolom saat pembayaran', function () {
    $admin = staffUser();
    $order = customerOrder();
    $order->markAsPaid('2026-09-09 10:30:00');

    $response = $this->actingAs($admin)->get(route('orders.exportExcel', [
        'month' => now()->format('Y-m'),
    ]));

    $response->assertOk();
    $content = $response->streamedContent();
    expect($content)->toContain('Saat Pembayaran');
    expect($content)->toContain($order->paidAtLabel());
    expect($content)->toContain('Pembayaran diterima');
});
