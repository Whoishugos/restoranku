@php
    $orders = $orders ?? collect();
    $emptyText = $emptyText ?? 'Belum ada pesanan.';
@endphp
<div class="card h-100">
    <div class="card-header">
        <h4 class="mb-0">{{ $title }}</h4>
        <p class="text-muted small mb-0">{{ $subtitle }}</p>
    </div>
    <div class="card-body p-0">
        @if ($orders->isEmpty())
            <p class="text-muted text-center py-4 mb-0">{{ $emptyText }}</p>
        @else
            <div class="list-group list-group-flush">
                @foreach ($orders as $order)
                    <a href="{{ route('orders.show', $order->id) }}" class="list-group-item list-group-item-action">
                        <div class="d-flex justify-content-between align-items-start gap-2">
                            <div>
                                <div class="fw-semibold">{{ $order->order_code }}</div>
                                <div class="small text-muted">
                                    Meja {{ $order->table_number }}
                                    · {{ $order->user->fullname ?? '-' }}
                                    · {{ 'Rp'. number_format($order->grand_total, 0, ',', '.') }}
                                </div>
                            </div>
                            <span class="badge {{ $order->kitchenStatusBadgeClass() }}">{{ $order->kitchenStatusLabel() }}</span>
                        </div>
                        <div class="small text-muted mt-1">{{ $order->created_at->format('d-m-Y H:i') }}</div>
                    </a>
                @endforeach
            </div>
        @endif
    </div>
</div>
