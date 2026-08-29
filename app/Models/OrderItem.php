<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;

class OrderItem extends Model
{
    use SoftDeletes;

    protected $fillable = ['order_id', 'item_id', 'quantity', 'price', 'tax','total_price', 'addons', 'created_at', 'updated_at'];
    protected $dates = ['deleted_at'];

    protected function casts(): array
    {
        return [
            'addons' => 'array',
        ];
    }

    public function addonLabel(): string
    {
        $names = [];
        foreach ($this->addons ?? [] as $addon) {
            if (! empty($addon['name'])) {
                $names[] = $addon['name'];
            }
        }

        return implode(', ', $names);
    }

    public function order()
    {
        return $this->belongsTo(Order::class);
    }

    public function item()
    {
        return $this->belongsTo(Item::class)->withTrashed();
    }
}
