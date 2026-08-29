<?php

use App\Http\Controllers\AddonGroupController;
use App\Http\Controllers\CategoryController;
use App\Http\Controllers\DashboardController;
use App\Http\Controllers\ItemController;
use App\Http\Controllers\MenuController;
// use App\Http\Controllers\MidtransController;
use App\Http\Controllers\OrderController;
use App\Http\Controllers\RoleController;
use App\Http\Controllers\TableQrController;
use App\Http\Controllers\UserController;
use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return redirect()->route('menu');
});

Route::get('/menu', [MenuController::class, 'index'])->name('menu');
Route::get('/meja/{tableNumber}', [MenuController::class, 'scanTable'])
    ->whereNumber('tableNumber')
    ->name('menu.scan');
Route::get('/menu/{item}/customize', [MenuController::class, 'customize'])->name('menu.customize');
Route::get('/cart', [MenuController::class, 'cart'])->name('cart');
Route::post('/cart/add', [MenuController::class, 'addToCart'])->name('cart.add');
Route::post('/cart/update', [MenuController::class, 'updateCart'])->name('cart.update');
Route::post('/cart/remove', [MenuController::class, 'removeCart'])->name('cart.remove');
Route::post('/cart/addons', [MenuController::class, 'updateAddons'])->name('cart.addons');
Route::get('/cart/clear', [MenuController::class, 'clearCart'])->name('cart.clear');

Route::get('/checkout', [MenuController::class, 'checkout'])->name('checkout');
Route::post('/checkout/store', [MenuController::class, 'storeOrder'])->name('checkout.store');
Route::get('/checkout/success/{orderId}', [MenuController::class, 'checkoutSuccess'])->name('checkout.success');

Route::get('/pesanan', [MenuController::class, 'trackOrders'])->name('customer.orders');
Route::get('/pesanan/{orderCode}/status', [MenuController::class, 'trackOrderStatus'])->name('customer.orders.status');
Route::get('/pesanan/{orderCode}', [MenuController::class, 'trackOrder'])->name('customer.orders.show');

// Route::post('/midtrans/notification', [MidtransController::class, 'notification'])->name('midtrans.notification');

Route::middleware(['auth', 'role:admin'])->group(function () {
    Route::resource('categories', CategoryController::class);
    Route::resource('roles', RoleController::class);
    Route::resource('users', UserController::class);
    Route::get('/qr-meja', [TableQrController::class, 'index'])->name('tables.qr');
    Route::resource('addon-groups', AddonGroupController::class)->except(['show']);
    Route::post('addon-groups/{addon_group}/options', [AddonGroupController::class, 'storeOption'])->name('addon-groups.options.store');
    Route::put('addons/{addon}', [AddonGroupController::class, 'updateOption'])->name('addons.update');
    Route::delete('addons/{addon}', [AddonGroupController::class, 'destroyOption'])->name('addons.destroy');
    Route::post('items/update-status/{item}', [ItemController::class, 'updateStatus'])->name('items.updateStatus');
    Route::resource('items', ItemController::class)->except(['index', 'destroy', 'show']);
});

Route::middleware(['auth', 'role:admin,cashier'])->group(function () {
    Route::get('items', [ItemController::class, 'index'])->name('items.index');
    Route::delete('items/{item}', [ItemController::class, 'destroy'])->name('items.destroy');
    Route::get('orders/laporan-excel', [OrderController::class, 'exportExcel'])->name('orders.exportExcel');
});

Route::middleware(['auth', 'role:admin,cashier,chef'])->group(function () {
    Route::get('/dashboard', [DashboardController::class, 'index'])->name('dashboard');
    Route::get('orders', [OrderController::class, 'index'])->name('orders.index');
    Route::get('orders/{order}', [OrderController::class, 'show'])->name('orders.show');
    Route::post('orders/{order}/payment', [OrderController::class, 'confirmPayment'])->name('orders.confirmPayment');
    Route::post('orders/{order}/kitchen-status', [OrderController::class, 'updateKitchenStatus'])->name('orders.updateKitchenStatus');
});
