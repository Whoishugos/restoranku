<?php

namespace App\Models;

use Carbon\Carbon;
use DateTimeInterface;
use Illuminate\Database\Eloquent\Model;

class Order extends Model
{
    public const KITCHEN_WAITING = 'waiting';
    public const KITCHEN_PROCESSING = 'processing';
    public const KITCHEN_COOKING = 'cooking';
    public const KITCHEN_READY = 'ready';

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
        'paid_at',
        'note',
        'created_at',
        'updated_at',
    ];

    protected $dates = ['deleted_at'];

    protected function casts(): array
    {
        return [
            'paid_at' => 'datetime',
        ];
    }

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

    public function markAsPaid(DateTimeInterface|string|null $paidAt = null): void
    {
        if (! $this->isPaid()) {
            $this->status = 'settlement';
        }

        if ($this->paid_at === null) {
            $this->paid_at = $this->parsePaidAt($paidAt) ?? now();
        }

        if ($this->kitchen_status === self::KITCHEN_WAITING || $this->kitchen_status === null) {
            $this->kitchen_status = self::KITCHEN_PROCESSING;
        }

        if ($this->isDirty()) {
            $this->save();
        }
    }

    public function applyGatewayTransaction(
        string $transactionStatus,
        ?string $fraudStatus = null,
        ?string $paymentType = null,
        DateTimeInterface|string|null $transactionTime = null,
    ): void {
        if ($this->isPaid() && in_array($this->kitchenStatus(), [self::KITCHEN_COOKING, self::KITCHEN_READY], true)) {
            return;
        }

        if ($transactionStatus === 'capture' && $paymentType === 'credit_card' && $fraudStatus === 'challenge') {
            return;
        }

        if (in_array($transactionStatus, ['settlement', 'capture'], true)) {
            $this->markAsPaid($transactionTime);
        }
    }

    public function paidAtLabel(): string
    {
        return $this->paid_at?->format('d-m-Y H:i') ?? '-';
    }

    public function paymentMethodLabel(): string
    {
        return match ($this->payment_method) {
            'qris' => 'QRIS',
            'tunai' => 'Tunai',
            default => $this->payment_method ?: '-',
        };
    }

    public function paymentStatusBadgeClass(): string
    {
        return $this->isPaid() ? 'bg-success' : 'bg-warning';
    }

    private function parsePaidAt(DateTimeInterface|string|null $paidAt): ?Carbon
    {
        if ($paidAt === null || $paidAt === '') {
            return null;
        }

        try {
            return Carbon::parse($paidAt);
        } catch (\Throwable) {
            return null;
        }
    }

    public function kitchenStatus(): string
    {
        $status = $this->kitchen_status ?: self::KITCHEN_WAITING;

        if ($this->status === 'cooked') {
            return self::KITCHEN_READY;
        }

        if ($this->isPaid() && $status === self::KITCHEN_WAITING) {
            return self::KITCHEN_PROCESSING;
        }

        return $status;
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
            default => 'bg-primary',
        };
    }

    /**
     * 0 menunggu pembayaran, 1 proses, 2 sedang dimasak, 3 siap disajikan
     */
    public function progressStep(): int
    {
        if (! $this->isPaid()) {
            return 0;
        }

        return match ($this->kitchenStatus()) {
            self::KITCHEN_COOKING => 2,
            self::KITCHEN_READY => 3,
            default => 1,
        };
    }

    public static function kitchenStatusOptions(): array
    {
        return [
            self::KITCHEN_PROCESSING => 'Proses',
            self::KITCHEN_COOKING => 'Sedang dimasak',
            self::KITCHEN_READY => 'Siap disajikan',
        ];
    }
}
