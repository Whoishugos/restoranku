<?php

use App\Models\Order;
use App\Models\Role;
use App\Models\User;

function staffUser(string $roleName = 'cashier'): User
{
    $role = Role::query()->firstOrCreate(
        ['role_name' => $roleName],
        ['description' => ucfirst($roleName)]
    );

    return User::factory()->create(['role_id' => $role->id]);
}

function makeOrder(array $overrides = []): Order
{
    $customerRole = Role::query()->firstOrCreate(
        ['role_name' => 'customer'],
        ['description' => 'Pelanggan']
    );
    $customer = User::factory()->create(['role_id' => $customerRole->id]);

    return Order::create(array_merge([
        'order_code' => 'ORD-TEST-'.uniqid(),
        'user_id' => $customer->id,
        'subtotal' => 10000,
        'tax' => 1000,
        'grand_total' => 11000,
        'status' => 'settlement',
        'kitchen_status' => Order::KITCHEN_READY,
        'table_number' => 5,
        'payment_method' => 'tunai',
        'note' => null,
    ], $overrides));
}

test('status menu includes selesai', function () {
    $staff = staffUser();
    $order = makeOrder();

    $this->actingAs($staff)
        ->get(route('orders.index'))
        ->assertOk()
        ->assertSee('Selesai')
        ->assertSee($order->order_code)
        ->assertSee('Sudah Dilayani');
});

test('marking an order as selesai moves it to the served list', function () {
    $staff = staffUser();
    $order = makeOrder(['kitchen_status' => Order::KITCHEN_READY]);

    $this->actingAs($staff)
        ->from(route('orders.index'))
        ->post(route('orders.updateKitchenStatus', $order->id), [
            'kitchen_status' => Order::KITCHEN_DONE,
        ])
        ->assertRedirect(route('orders.index', ['filter' => Order::LIST_FILTER_SERVED]));

    $order->refresh();
    expect($order->kitchen_status)->toBe(Order::KITCHEN_DONE)
        ->and($order->isServed())->toBeTrue();

    $this->actingAs($staff)
        ->get(route('orders.index'))
        ->assertOk()
        ->assertDontSee($order->order_code);

    $this->actingAs($staff)
        ->get(route('orders.index', ['filter' => 'served']))
        ->assertOk()
        ->assertSee($order->order_code)
        ->assertSee('Sudah Dilayani')
        ->assertSee('tidak dapat diubah lagi');
});

test('completed orders cannot be changed again', function () {
    $staff = staffUser();
    $order = makeOrder(['kitchen_status' => Order::KITCHEN_DONE]);

    $this->actingAs($staff)
        ->from(route('orders.index', ['filter' => 'served']))
        ->post(route('orders.updateKitchenStatus', $order->id), [
            'kitchen_status' => Order::KITCHEN_READY,
        ])
        ->assertRedirect(route('orders.index', ['filter' => 'served']))
        ->assertSessionHas('error', 'Pesanan yang sudah selesai tidak dapat diubah lagi.');

    $order->refresh();
    expect($order->kitchen_status)->toBe(Order::KITCHEN_DONE);

    $this->actingAs($staff)
        ->get(route('orders.show', $order->id))
        ->assertOk()
        ->assertSee('disabled', false)
        ->assertSee('tidak dapat diubah lagi');
});
