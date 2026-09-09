<?php

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
