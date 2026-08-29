<?php

namespace Database\Seeders;

use App\Models\Addon;
use App\Models\AddonGroup;
use App\Models\Category;
use Illuminate\Database\Seeder;

class AddonSeeder extends Seeder
{
    public function run(): void
    {
        $food = Category::where('cat_name', 'Makanan')->first();
        $drink = Category::where('cat_name', 'Minuman')->first();
        if (! $food) {
            return;
        }

        $sizeFood = AddonGroup::updateOrCreate(
            ['name' => 'Ukuran porsi'],
            [
                'type' => AddonGroup::TYPE_SIZE,
                'category_id' => $food->id,
                'min_select' => 1,
                'max_select' => 1,
                'is_active' => true,
            ]
        );
        $addFood = AddonGroup::updateOrCreate(
            ['name' => 'Tambah bahan'],
            [
                'type' => AddonGroup::TYPE_ADD,
                'category_id' => $food->id,
                'min_select' => 0,
                'max_select' => 3,
                'is_active' => true,
            ]
        );
        $removeFood = AddonGroup::updateOrCreate(
            ['name' => 'Kurangi / tanpa bahan'],
            [
                'type' => AddonGroup::TYPE_REMOVE,
                'category_id' => $food->id,
                'min_select' => 0,
                'max_select' => 3,
                'is_active' => true,
            ]
        );
        $sideFood = AddonGroup::updateOrCreate(
            ['name' => 'Menu pendamping'],
            [
                'type' => AddonGroup::TYPE_COMPANION,
                'category_id' => $food->id,
                'min_select' => 0,
                'max_select' => 2,
                'is_active' => true,
            ]
        );

        $this->options($sizeFood, [
            ['name' => 'Porsi reguler', 'price' => 0],
            ['name' => 'Porsi jumbo', 'price' => 8000],
        ]);
        $this->options($addFood, [
            ['name' => 'Telur mata sapi', 'price' => 5000],
            ['name' => 'Telur dadar', 'price' => 5000],
            ['name' => 'Keju', 'price' => 6000],
            ['name' => 'Sosis', 'price' => 7000],
            ['name' => 'Extra ayam', 'price' => 10000],
            ['name' => 'Sambal extra', 'price' => 2000],
        ]);
        $this->options($removeFood, [
            ['name' => 'Tanpa acar', 'price' => 0],
            ['name' => 'Tanpa bawang', 'price' => 0],
            ['name' => 'Tanpa sambal', 'price' => 0],
        ]);
        $this->options($sideFood, [
            ['name' => 'Extra nasi', 'price' => 4000],
            ['name' => 'Kerupuk', 'price' => 3000],
        ]);

        if ($drink) {
            $sizeDrink = AddonGroup::updateOrCreate(
                ['name' => 'Ukuran minuman'],
                [
                    'type' => AddonGroup::TYPE_SIZE,
                    'category_id' => $drink->id,
                    'min_select' => 1,
                    'max_select' => 1,
                    'is_active' => true,
                ]
            );
            $this->options($sizeDrink, [
                ['name' => 'Gelas sedang', 'price' => 0],
                ['name' => 'Gelas besar', 'price' => 5000],
            ]);
        }
    }

    private function options(AddonGroup $group, array $rows): void
    {
        foreach ($rows as $row) {
            Addon::updateOrCreate(
                ['name' => $row['name']],
                [
                    'addon_group_id' => $group->id,
                    'price' => $row['price'],
                    'stock' => 100,
                    'is_active' => true,
                ]
            );
        }
    }
}
