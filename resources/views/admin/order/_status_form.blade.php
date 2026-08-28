@php
    $currentKitchen = $order->kitchenStatus();
    $canUpdateKitchen = in_array(Auth::user()->role->role_name ?? '', ['admin', 'cashier', 'chef'], true);
    $canConfirmPayment = in_array(Auth::user()->role->role_name ?? '', ['admin', 'cashier'], true);
@endphp
@if ($canConfirmPayment && ! $order->isPaid() && $order->payment_method === 'tunai')
    <form action="{{ route('orders.confirmPayment', $order->id) }}" method="POST" class="mb-2">
        @csrf
        <button type="submit" class="btn btn-success btn-sm">
            <i class="bi bi-check-circle"></i> Terima Pembayaran
        </button>
    </form>
@endif
@if ($canUpdateKitchen && $order->isPaid())
    <form action="{{ route('orders.updateKitchenStatus', $order->id) }}" method="POST" class="d-flex gap-1 align-items-center">
        @csrf
        <select name="kitchen_status" class="form-select form-select-sm" style="min-width: 160px;">
            @foreach ($kitchenStatuses as $value => $label)
                <option value="{{ $value }}" @selected($currentKitchen === $value)>{{ $label }}</option>
            @endforeach
        </select>
        <button type="submit" class="btn btn-primary btn-sm">
            Ubah
        </button>
    </form>
@endif