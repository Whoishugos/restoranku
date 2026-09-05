<?php

use Illuminate\Support\Facades\View;

it('resolves the kitchen display add-on partial', function () {
    expect(View::exists('admin.order._kds_addons'))->toBeTrue();
});

it('renders add-on badges for kitchen display', function () {
    $html = view('admin.order._kds_addons', [
        'addons' => [
            [
                'type' => 'ingredient_add',
                'type_label' => 'Tambah bahan',
                'name' => 'Extra cheese',
            ],
        ],
    ])->render();

    expect($html)
        ->toContain('TAMBAH BAHAN')
        ->toContain('EXTRA CHEESE')
        ->toContain('bg-success');
});

it('renders nothing when there are no add-ons', function () {
    $html = view('admin.order._kds_addons', ['addons' => []])->render();

    expect(trim($html))->toBe('');
});
