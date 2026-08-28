@extends('customer.layouts.master')

@section('title', 'Pesanan Saya')

@section('content')
<div class="container-fluid page-header py-5">
    <h1 class="text-center text-white display-6">Pesanan Saya</h1>
    <ol class="breadcrumb justify-content-center mb-0">
        <li class="breadcrumb-item active text-primary">Lacak proses menu Anda</li>
    </ol>
</div>

<div class="container py-5">
    @if (session('error'))
        <div class="alert alert-danger">{{ session('error') }}</div>
    @endif

    <div class="card border-0 shadow-sm mb-4">
        <div class="card-body">
            <h5 class="mb-3">Cari pesanan dengan kode</h5>
            <form class="row g-2" method="GET" action="{{ route('customer.orders') }}">
                <div class="col-md-8">
                    <input type="text" name="kode" class="form-control" placeholder="Contoh: ORD-12-1710000000" required>
                </div>
                <div class="col-md-4">
                    <button type="submit" class="btn btn-primary w-100">Lacak</button>
                </div>
            </form>
        </div>
    </div>

    @if ($orders->isEmpty())
        <p class="text-center text-muted">Belum ada pesanan di perangkat ini. Setelah checkout, status akan muncul di sini.</p>
    @else
        <div class="row g-4">
            @foreach ($orders as $order)
                <div class="col-md-6">
                    <div class="border rounded p-3 h-100">
                        <div class="d-flex justify-content-between align-items-start mb-2">
                            <div>
                                <div class="fw-bold">{{ $order->order_code }}</div>
                                <div class="small text-muted">Meja {{ $order->table_number }} · {{ $order->created_at->format('d-m-Y H:i') }}</div>
                            </div>
                            <span class="badge {{ $order->kitchenStatusBadgeClass() }}">{{ $order->kitchenStatusLabel() }}</span>
                        </div>
                        @include('customer.partials.order-progress', ['order' => $order])
                        <a href="{{ route('customer.orders.show', $order->order_code) }}" class="btn btn-outline-primary w-100">Lihat detail</a>
                    </div>
                </div>
            @endforeach
        </div>
    @endif
</div>
@endsection
