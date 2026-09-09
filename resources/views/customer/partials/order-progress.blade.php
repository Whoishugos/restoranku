@php
    $step = $order->progressStep();
    $steps = [
        ['label' => 'Menunggu pembayaran', 'short' => 'Bayar', 'icon' => 'fa-receipt'],
        ['label' => 'Proses', 'short' => 'Proses', 'icon' => 'fa-utensils'],
        ['label' => 'Sedang dimasak', 'short' => 'Masak', 'icon' => 'fa-fire'],
        ['label' => 'Siap disajikan', 'short' => 'Siap', 'icon' => 'fa-bell'],
    ];
@endphp

<div class="order-progress mb-4">
    <p class="text-center mb-3">
        <span class="badge {{ $order->kitchenStatusBadgeClass() }} fs-6">{{ $order->kitchenStatusLabel() }}</span>
    </p>
    <div class="d-flex justify-content-between position-relative px-1 px-md-3">
        <div class="position-absolute start-0 end-0 top-50 translate-middle-y mx-4 progress-track"></div>
        <div class="position-absolute start-0 top-50 translate-middle-y mx-4 progress-track-fill" style="width: {{ $step * 33 }}%;"></div>
        @foreach ($steps as $index => $item)
            <div class="text-center position-relative progress-step">
                <div class="rounded-circle d-inline-flex align-items-center justify-content-center mb-2 progress-step-icon {{ $step >= $index ? 'bg-primary text-white' : 'bg-light text-muted border' }}">
                    <i class="fa {{ $item['icon'] }}"></i>
                </div>
                <div class="small progress-step-label {{ $step >= $index ? 'fw-bold text-primary' : 'text-muted' }}">
                    <span class="d-none d-md-inline">{{ $item['label'] }}</span>
                    <span class="d-md-none">{{ $item['short'] }}</span>
                </div>
            </div>
        @endforeach
    </div>
</div>
