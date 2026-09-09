<?php

namespace Database\Seeders;

use App\Models\Category;
use App\Models\Item;
use Illuminate\Database\Seeder;

class ItemSeeder extends Seeder
{
    public function run(): void
    {
        $food = Category::where('cat_name', 'Makanan')->first();
        $drink = Category::where('cat_name', 'Minuman')->first();
        if (! $food || ! $drink) {
            return;
        }

        Item::query()->where('img', 'like', 'http%')->forceDelete();

        $items = [
            [
                'name' => 'Mie Ayam',
                'description' => 'Mie kuning dengan ayam kecap dan sawi hijau.',
                'price' => 18000,
                'category_id' => $food->id,
                'img' => '1746522699.jpg',
            ],
            [
                'name' => 'Mie Ayam Jamur',
                'description' => 'Mie ayam dengan jamur kancing dan sayuran.',
                'price' => 20000,
                'category_id' => $food->id,
                'img' => '1746603477.jpg',
            ],
            [
                'name' => 'Mie Goreng Sayur',
                'description' => 'Mie goreng dengan telur, wortel, dan kacang polong.',
                'price' => 17000,
                'category_id' => $food->id,
                'img' => '1787975646.jpg',
            ],
            [
                'name' => 'Nasi Goreng Ayam',
                'description' => 'Nasi goreng ayam dengan wortel, kacang polong, dan daun bawang.',
                'price' => 22000,
                'category_id' => $food->id,
                'img' => '1787975844.jpg',
            ],
            [
                'name' => 'Nasi Capcay',
                'description' => 'Nasi goreng telur disiram capcay udang dan sayuran.',
                'price' => 24000,
                'category_id' => $food->id,
                'img' => 'nasi-capcay.jpg',
            ],
            [
                'name' => 'Chicken Steak',
                'description' => 'Steak ayam goreng tepung dengan saus lada hitam, kentang, dan sayuran.',
                'price' => 35000,
                'category_id' => $food->id,
                'img' => '1787976034.jpeg',
            ],
            [
                'name' => 'Spaghetti Carbonara',
                'description' => 'Spaghetti creamy dengan smoked beef dan keju.',
                'price' => 32000,
                'category_id' => $food->id,
                'img' => '1787977405.jpeg',
            ],
            [
                'name' => 'Spaghetti Bolognese',
                'description' => 'Spaghetti saus daging cincang dan keju parmesan.',
                'price' => 30000,
                'category_id' => $food->id,
                'img' => 'spaghetti-bolognese.jpg',
            ],
            [
                'name' => 'Lumpia Goreng',
                'description' => 'Lumpia goreng renyah dengan kentang goreng dan salad.',
                'price' => 15000,
                'category_id' => $food->id,
                'img' => '1787977566.jpg',
            ],
            [
                'name' => 'Jus Jeruk',
                'description' => 'Jus jeruk peras segar, tanpa pengawet.',
                'price' => 12000,
                'category_id' => $drink->id,
                'img' => '1746610542.jpg',
            ],
            [
                'name' => 'Es Teh Manis',
                'description' => 'Teh manis dingin, segar untuk teman makan.',
                'price' => 6000,
                'category_id' => $drink->id,
                'img' => 'es-teh.jpg',
            ],
            [
                'name' => 'Es Kopi Susu',
                'description' => 'Kopi susu dingin dengan es batu.',
                'price' => 14000,
                'category_id' => $drink->id,
                'img' => 'es-kopi.jpg',
            ],
        ];

        foreach ($items as $row) {
            Item::updateOrCreate(
                ['name' => $row['name']],
                $row + ['is_active' => 1, 'stock' => 50]
            );
        }
    }
}
