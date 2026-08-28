@php
    $step = $order->progressStep();
    $steps = [
        ['label' => 'Menunggu pembayaran', 'icon' => 'fa-receipt'],
        ['label' => 'Proses', 'icon' => 'fa-utensils'],
        ['label' => 'Sedang dimasak', 'icon' => 'fa-fire'],
        ['label' => 'Siap disajikan', 'icon' => 'fa-bell'],
    ];
@endphp

<div class="order-progress mb-4">
    <p class="text-center mb-3">
        <span class="badge {{ $order->kitchenStatusBadgeClass() }} fs-6">{{ $order->kitchenStatusLabel() }}</span>
    </p>
    <div class="d-flex justify-content-between position-relative px-1 px-md-3">
        <div class="position-absolute start-0 end-0 top-50 translate-middle-y mx-4" style="height: 4px; background: #e9ecef; z-index: 0;"></div>
        <div class="position-absolute start-0 top-50 translate-middle-y mx-4" style="height: 4px; background: #81c408; z-index: 0; width: {{ $step * 33 }}%; max-width: calc(100% - 3rem);"></div>
        @foreach ($steps as $index => $item)
            <div class="text-center position-relative" style="z-index: 1; width: 25%;">
                <div class="rounded-circle d-inline-flex align-items-center justify-content-center mb-2 {{ $step >= $index ? 'bg-primary text-white' : 'bg-light text-muted border' }}"
                     style="width: 48px; height: 48px;">
                    <i class="fa {{ $item['icon'] }}"></i>
                </div>
                <div class="small {{ $step >= $index ? 'fw-bold text-primary' : 'text-muted' }}">{{ $item['label'] }}</div>
            </div>
        @endforeach
    </div>
</div>
