<?php

use App\Models\Order;

test('selesai is a kitchen status option', function () {
    expect(Order::kitchenStatusOptions())->toHaveKey(Order::KITCHEN_DONE)
        ->and(Order::kitchenStatusOptions()[Order::KITCHEN_DONE])->toBe('Selesai');
});

test('completed orders are served and locked', function () {
    $order = new Order([
        'status' => 'settlement',
        'kitchen_status' => Order::KITCHEN_DONE,
        'payment_method' => 'tunai',
    ]);

    expect($order->kitchenStatus())->toBe(Order::KITCHEN_DONE)
        ->and($order->isServed())->toBeTrue()
        ->and($order->canUpdateKitchenStatus())->toBeFalse()
        ->and($order->kitchenStatusLabel())->toBe('Selesai')
        ->and($order->progressStep())->toBe(4)
        ->and($order->kitchenStatusBadgeClass())->toBe('bg-dark');
});

test('ready paid orders can still be updated', function () {
    $order = new Order([
        'status' => 'settlement',
        'kitchen_status' => Order::KITCHEN_READY,
        'payment_method' => 'tunai',
    ]);

    expect($order->isServed())->toBeFalse()
        ->and($order->canUpdateKitchenStatus())->toBeTrue()
        ->and($order->kitchenStatusLabel())->toBe('Siap disajikan')
        ->and($order->progressStep())->toBe(3);
});

test('done kitchen status is not overridden by cooked payment status', function () {
    $order = new Order([
        'status' => 'cooked',
        'kitchen_status' => Order::KITCHEN_DONE,
        'payment_method' => 'tunai',
    ]);

    expect($order->kitchenStatus())->toBe(Order::KITCHEN_DONE)
        ->and($order->isServed())->toBeTrue();
});
