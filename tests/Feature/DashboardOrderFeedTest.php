<?php

use App\Models\Order;

test('dashboard shows newest oldest and paid order lists', function () {
    $staff = staffUser();
    $oldest = makeOrder([
        'order_code' => 'ORD-OLD-WAIT',
        'status' => 'pending',
        'kitchen_status' => Order::KITCHEN_WAITING,
        'created_at' => now()->subHours(3),
        'updated_at' => now()->subHours(3),
    ]);
    $newest = makeOrder([
        'order_code' => 'ORD-NEW-WAIT',
        'status' => 'pending',
        'kitchen_status' => Order::KITCHEN_WAITING,
        'created_at' => now(),
        'updated_at' => now(),
    ]);
    $paid = makeOrder([
        'order_code' => 'ORD-PAID-OK',
        'status' => 'settlement',
        'kitchen_status' => Order::KITCHEN_PROCESSING,
        'created_at' => now()->subHour(),
        'updated_at' => now()->subHour(),
    ]);

    $this->actingAs($staff)
        ->get(route('dashboard'))
        ->assertOk()
        ->assertSee('Pesanan Terbaru')
        ->assertSee('Pesanan Terlama')
        ->assertSee('Sudah Dibayarkan')
        ->assertSee('ORD-NEW-WAIT')
        ->assertSee('ORD-OLD-WAIT')
        ->assertSee('ORD-PAID-OK')
        ->assertSee('Notifikasi pesanan', false);
});

test('notification feed reports new orders after since id', function () {
    $staff = staffUser();
    $existing = makeOrder(['order_code' => 'ORD-EXISTING']);
    $fresh = makeOrder(['order_code' => 'ORD-FRESH-NEW']);

    $this->actingAs($staff)
        ->getJson(route('dashboard.notifications', ['since_id' => $existing->id]))
        ->assertOk()
        ->assertJsonPath('latest_id', $fresh->id)
        ->assertJsonPath('new_count', 1)
        ->assertJsonPath('new_orders.0.order_code', 'ORD-FRESH-NEW');
});

test('guests cannot read the order notification feed', function () {
    $this->get(route('dashboard.notifications'))
        ->assertRedirect(route('login'));
});
