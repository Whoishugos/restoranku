<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class AddonGroup extends Model
{
    public const TYPE_SIZE = 'size';
    public const TYPE_ADD = 'ingredient_add';
    public const TYPE_REMOVE = 'ingredient_remove';
    public const TYPE_COMPANION = 'companion';

    protected $fillable = [
        'name',
        'type',
        'category_id',
        'min_select',
        'max_select',
        'is_active',
    ];

    protected function casts(): array
    {
        return [
            'min_select' => 'integer',
            'max_select' => 'integer',
            'is_active' => 'boolean',
        ];
    }

    public static function typeLabels(): array
    {
        return [
            self::TYPE_SIZE => 'Upgrade ukuran',
            self::TYPE_ADD => 'Tambah bahan',
            self::TYPE_REMOVE => 'Kurangi / tanpa bahan',
            self::TYPE_COMPANION => 'Menu pendamping',
        ];
    }

    public static function typeBadgeClass(string $type): string
    {
        return match ($type) {
            self::TYPE_SIZE => 'bg-primary',
            self::TYPE_ADD => 'bg-success',
            self::TYPE_REMOVE => 'bg-danger',
            self::TYPE_COMPANION => 'bg-warning text-dark',
            default => 'bg-secondary',
        };
    }

    public function typeLabel(): string
    {
        return self::typeLabels()[$this->type] ?? $this->type;
    }

    public function isRequired(): bool
    {
        return $this->min_select > 0;
    }

    public function isSingle(): bool
    {
        return $this->max_select <= 1;
    }

    public function category()
    {
        return $this->belongsTo(Category::class);
    }

    public function addons()
    {
        return $this->hasMany(Addon::class)->orderBy('name');
    }

    public function items()
    {
        return $this->belongsToMany(Item::class, 'addon_group_item');
    }
}
