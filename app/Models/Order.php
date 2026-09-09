<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Order extends Model
{
    public const KITCHEN_WAITING = 'waiting';
    public const KITCHEN_PROCESSING = 'processing';
    public const KITCHEN_COOKING = 'cooking';
    public const KITCHEN_READY = 'ready';
    public const KITCHEN_DONE = 'done';

    public const LIST_FILTER_ACTIVE = 'active';
    public const LIST_FILTER_SERVED = 'served';

    protected $fillable = [
        'order_code',
        'user_id',
        'subtotal',
        'tax',
        'grand_total',
        'status',
        'kitchen_status',
        'table_number',
        'payment_method',
        'note',
        'created_at',
        'updated_at',
    ];

    protected $dates = ['deleted_at'];

    public function user()
    {
        return $this->belongsTo(User::class)->withTrashed();
    }

    public function orderItems()
    {
        return $this->hasMany(OrderItem::class);
    }

    public function isPaid(): bool
    {
        return in_array($this->status, ['settlement', 'cooked'], true);
    }

    public function kitchenStatus(): string
    {
        $status = $this->kitchen_status ?: self::KITCHEN_WAITING;

        if ($status === self::KITCHEN_DONE) {
            return self::KITCHEN_DONE;
        }

        if ($this->status === 'cooked') {
            return self::KITCHEN_READY;
        }

        if ($this->isPaid() && $status === self::KITCHEN_WAITING) {
            return self::KITCHEN_PROCESSING;
        }

        return $status;
    }

    public function isServed(): bool
    {
        return $this->kitchenStatus() === self::KITCHEN_DONE;
    }

    public function canUpdateKitchenStatus(): bool
    {
        return $this->isPaid() && ! $this->isServed();
    }

    public function scopeServed($query)
    {
        return $query->where('kitchen_status', self::KITCHEN_DONE);
    }

    public function scopeNotServed($query)
    {
        return $query->where(function ($q) {
            $q->whereNull('kitchen_status')
                ->orWhere('kitchen_status', '!=', self::KITCHEN_DONE);
        });
    }

    public function paymentStatusLabel(): string
    {
        if ($this->isPaid()) {
            return 'Pembayaran diterima';
        }

        return $this->payment_method === 'qris'
            ? 'Menunggu konfirmasi pembayaran'
            : 'Menunggu pembayaran';
    }

    public function kitchenStatusLabel(): string
    {
        if (! $this->isPaid()) {
            return $this->paymentStatusLabel();
        }

        return match ($this->kitchenStatus()) {
            self::KITCHEN_COOKING => 'Sedang dimasak',
            self::KITCHEN_READY => 'Siap disajikan',
            self::KITCHEN_DONE => 'Selesai',
            default => 'Proses',
        };
    }

    public function kitchenStatusBadgeClass(): string
    {
        if (! $this->isPaid()) {
            return 'bg-warning';
        }

        return match ($this->kitchenStatus()) {
            self::KITCHEN_COOKING => 'bg-info',
            self::KITCHEN_READY => 'bg-success',
            self::KITCHEN_DONE => 'bg-dark',
            default => 'bg-primary',
        };
    }

    /**
     * 0 menunggu pembayaran, 1 proses, 2 sedang dimasak, 3 siap disajikan, 4 selesai
     */
    public function progressStep(): int
    {
        if (! $this->isPaid()) {
            return 0;
        }

        return match ($this->kitchenStatus()) {
            self::KITCHEN_COOKING => 2,
            self::KITCHEN_READY => 3,
            self::KITCHEN_DONE => 4,
            default => 1,
        };
    }

    public static function kitchenStatusOptions(): array
    {
        return [
            self::KITCHEN_PROCESSING => 'Proses',
            self::KITCHEN_COOKING => 'Sedang dimasak',
            self::KITCHEN_READY => 'Siap disajikan',
            self::KITCHEN_DONE => 'Selesai',
        ];
    }

    public static function listFilters(): array
    {
        return [
            self::LIST_FILTER_ACTIVE => 'Sedang Dilayani',
            self::LIST_FILTER_SERVED => 'Sudah Dilayani',
        ];
    }
}
