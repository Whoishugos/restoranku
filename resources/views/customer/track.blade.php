@extends('customer.layouts.master')

@section('title', 'Lacak Pesanan')

@section('content')
<div class="container-fluid page-header py-5">
    <h1 class="text-center text-white display-6">Proses Pesanan</h1>
    <ol class="breadcrumb justify-content-center mb-0">
        <li class="breadcrumb-item active text-primary">{{ $order->order_code }}</li>
    </ol>
</div>

<div class="container py-5">
    <div class="row justify-content-center">
        <div class="col-lg-8">
            <div class="bg-white border rounded shadow-sm p-4">
                <div class="d-flex justify-content-between flex-wrap gap-2 mb-3">
                    <div>
                        <h4 class="mb-1">Meja {{ $order->table_number }}</h4>
                        <p class="text-muted mb-0">{{ $order->created_at->format('d-m-Y H:i') }}</p>
                    </div>
                    <div class="text-end">
                        <div class="small text-muted">Pembayaran</div>
                        <div>{{ $order->paymentStatusLabel() }} ({{ $order->payment_method }})</div>
                    </div>
                </div>

                <div id="order-progress">
                    @include('customer.partials.order-progress', ['order' => $order])
                </div>

                <h5 class="mt-4">Menu yang dipesan</h5>
                <table class="table">
                    <tbody>
                        @foreach ($orderItems as $orderItem)
                            <tr>
                                <td>{{ $orderItem->item->name ?? 'Menu' }} × {{ $orderItem->quantity }}</td>
                                <td class="text-end">{{ 'Rp'. number_format($orderItem->price, 0, ',', '.') }}</td>
                            </tr>
                        @endforeach
                        <tr>
                            <th>Total</th>
                            <th class="text-end">{{ 'Rp'. number_format($order->grand_total, 0, ',', '.') }}</th>
                        </tr>
                    </tbody>
                </table>

                <p class="small text-muted mb-3">Halaman ini diperbarui otomatis saat kasir atau koki mengubah status.</p>
                <a href="{{ route('customer.orders') }}" class="btn btn-outline-secondary">Semua pesanan</a>
                <a href="{{ route('menu') }}" class="btn btn-primary">Kembali ke menu</a>
            </div>
        </div>
    </div>
</div>
@endsection

@section('script')
<script>
    const statusUrl = @json(route('customer.orders.status', $order->order_code));
    let lastStep = {{ $order->progressStep() }};

    function refreshStatus() {
        fetch(statusUrl, { headers: { 'Accept': 'application/json' } })
            .then(response => response.json())
            .then(data => {
                if (data.status !== 'success') {
                    return;
                }
                if (data.progress_step !== lastStep) {
                    window.location.reload();
                }
            })
            .catch(() => {});
    }

    setInterval(refreshStatus, 8000);
</script>
@endsection
