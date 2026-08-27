<?php

namespace Database\Seeders;

use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;
use App\Models\Item;
use App\Models\Category;

class ItemSeeder extends Seeder
{
    public function run(): void
    {
        Item::factory(10)->create();
    }
}
