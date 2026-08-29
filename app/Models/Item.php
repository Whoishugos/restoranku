<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;
use Illuminate\Database\Eloquent\Factories\HasFactory;

class Item extends Model
{
    use SoftDeletes, HasFactory;

    protected $fillable = ['name', 'description', 'price', 'category_id', 'img', 'is_active', 'stock', 'created_at', 'updated_at'];
    protected $dates = ['deleted_at'];

    public function category()
    {
        return $this->belongsTo(Category::class);
    }

    public function orderItems()
    {
        return $this->hasMany(OrderItem::class);
    }

    public function addonGroups()
    {
        return $this->belongsToMany(AddonGroup::class, 'addon_group_item');
    }

    public function isAvailable(): bool
    {
        return (bool) $this->is_active && (int) $this->stock > 0;
    }

    public function scopeAvailable($query)
    {
        return $query->where('is_active', 1)->where('stock', '>', 0);
    }

}