<?php

use App\Models\Category;
use App\Models\Item;

it('ships a valid web app manifest so the menu can be installed on a phone', function () {
    $path = public_path('manifest.webmanifest');

    expect(file_exists($path))->toBeTrue();

    $manifest = json_decode(file_get_contents($path), true);

    expect($manifest)->toBeArray()
        ->and($manifest['display'])->toBe('standalone')
        ->and($manifest['start_url'])->toBe('/menu')
        ->and($manifest['icons'])->not->toBeEmpty();
});

it('ships a service worker and offline fallback for phones', function () {
    expect(file_exists(public_path('sw.js')))->toBeTrue()
        ->and(file_exists(public_path('offline.html')))->toBeTrue()
        ->and(file_exists(public_path('icons/icon-192.png')))->toBeTrue()
        ->and(file_exists(public_path('icons/icon-512.png')))->toBeTrue();
});

it('customer layout includes phone viewport, PWA tags, and bottom navigation', function () {
    $header = file_get_contents(resource_path('views/customer/layouts/__header.blade.php'));
    $navbar = file_get_contents(resource_path('views/customer/layouts/__navbar.blade.php'));
    $bottom = file_get_contents(resource_path('views/customer/layouts/__bottom_nav.blade.php'));
    $master = file_get_contents(resource_path('views/customer/layouts/master.blade.php'));

    expect($header)->toContain('width=device-width')
        ->and($header)->toContain('manifest.webmanifest')
        ->and($header)->toContain('apple-mobile-web-app-capable')
        ->and($navbar)->toContain('data-cart-count')
        ->and($bottom)->toContain('customer-bottom-nav')
        ->and($master)->toContain('customer.layouts.__bottom_nav')
        ->and($master)->toContain('mobile-app.js');
});

it('resolves local menu photos and falls back when a file is missing', function () {
    expect(\App\Support\MenuImage::url('1746522699.jpg'))
        ->toContain('img_item_upload/1746522699.jpg')
        ->and(\App\Support\MenuImage::url('missing-file.png'))
        ->toContain('img_item_upload/default.jpg');
});

it('serves the customer menu as a phone-ready page', function () {
    $this->get('/menu')
        ->assertOk()
        ->assertSee('customer-bottom-nav', false)
        ->assertSee('manifest.webmanifest', false)
        ->assertSee('width=device-width', false)
        ->assertSee('Pasang di HP');
});

it('cart and checkout use card layouts on small screens instead of wide tables only', function () {
    $cart = file_get_contents(resource_path('views/customer/cart.blade.php'));
    $checkout = file_get_contents(resource_path('views/customer/checkout.blade.php'));
    $success = file_get_contents(resource_path('views/customer/success.blade.php'));

    expect($cart)->toContain('cart-list d-md-none')
        ->and($checkout)->toContain('checkout-items d-md-none')
        ->and($success)->toContain('max-width: 450px');
});

function phoneCartSession(Item $item): array
{
    return [
        $item->id.':none' => [
            'key' => $item->id.':none',
            'id' => $item->id,
            'name' => $item->name,
            'price' => (int) $item->price,
            'image' => $item->img,
            'category' => 'Makanan',
            'qty' => 2,
            'addons' => [],
        ],
    ];
}

it('saves a cash order so it appears in the cashier list', function () {
    $category = Category::create([
        'cat_name' => 'Makanan',
        'description' => 'Kategori Makanan',
    ]);
    $item = Item::factory()->create([
        'name' => 'Nasi Goreng Tunai',
        'category_id' => $category->id,
        'price' => 20000,
        'is_active' => 1,
        'stock' => 10,
        'img' => 'default.jpg',
    ]);
    $cart = phoneCartSession($item);

    $response = $this->withSession(['cart' => $cart, 'tableNumber' => 8])
        ->post(route('checkout.store'), [
            'fullname' => 'Budi Santoso',
            'phone' => '081234567890',
            'table_number' => 8,
            'payment_method' => 'tunai',
            'note' => 'Pedas',
        ]);

    $order = \App\Models\Order::first();
    expect($order)->not->toBeNull()
        ->and($order->payment_method)->toBe('tunai')
        ->and($order->table_number)->toBe(8)
        ->and($order->status)->toBe('pending')
        ->and($order->user?->fullname)->toBe('Budi Santoso')
        ->and(\App\Models\Role::where('role_name', 'customer')->exists())->toBeTrue();

    $response->assertRedirect(route('checkout.success', $order->order_code));
    $this->get(route('checkout.success', $order->order_code))->assertOk()->assertSee('Pesanan berhasil');
});

it('renders a filled cart as phone cards and keeps the checkout form usable', function () {
    $category = Category::create([
        'cat_name' => 'Makanan',
        'description' => 'Kategori Makanan',
    ]);
    $item = Item::factory()->create([
        'name' => 'Nasi Goreng HP',
        'category_id' => $category->id,
        'price' => 25000,
        'is_active' => 1,
        'stock' => 10,
        'img' => 'nasi.jpg',
    ]);
    $cart = phoneCartSession($item);

    $this->withSession(['cart' => $cart, 'tableNumber' => 7])
        ->get('/cart')
        ->assertOk()
        ->assertSee('cart-card', false)
        ->assertSee('Nasi Goreng HP')
        ->assertSee('Lanjut ke Pembayaran');

    $this->withSession(['cart' => $cart, 'tableNumber' => 7])
        ->get('/checkout')
        ->assertOk()
        ->assertSee('checkout-items', false)
        ->assertSee('Nasi Goreng HP')
        ->assertSee('Nomor WhatsApp')
        ->assertSee('Bayar Sekarang');
});
