<?php

namespace Database\Factories;

use App\Models\Category;
use Illuminate\Database\Eloquent\Factories\Factory;

class ItemFactory extends Factory
{

    public function definition()
{
    return [
        'name' => $this->faker->word,
        'category_id' => Category::inRandomOrder()->first()->id, // Ambil ID kategori yang valid
        'price' => $this->faker->numberBetween(1000, 10000),
        'description' => $this->faker->sentence,
        'img' => $this->faker->imageUrl(),
        'is_active' => $this->faker->boolean,
        'stock' => 50,
        ];
    }
}
