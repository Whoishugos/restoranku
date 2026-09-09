@extends('admin.layouts.master')
@section('title', 'Daftar Pesanan')

@section('css')
<link rel="stylesheet" href="{{ asset('assets/admin/extensions/simple-datatables/style.css') }}">
<link rel="stylesheet" href="{{ asset('assets/admin/compiled/css/table-datatable.css') }}">
@endsection

@section('content')
<div class="page-heading">
    <div class="page-title">
        <div class="row">
            <div class="col-12 col-md-6 order-md-1 order-last">
                <h3>{{ $filter === \App\Models\Order::LIST_FILTER_SERVED ? 'Sudah Dilayani' : 'Daftar Pesanan' }}</h3>
                <p class="text-subtitle text-muted">
                    @if ($filter === \App\Models\Order::LIST_FILTER_SERVED)
                        Pesanan yang sudah selesai tidak dapat diubah lagi
                    @else
                        Kasir dan koki dapat mengubah status: proses, sedang dimasak, siap disajikan, selesai
                    @endif
                </p>
            </div>
            @if ($canExportReport)
            <div class="col-12 col-md-6 order-md-2 order-first">
                <form action="{{ route('orders.exportExcel') }}" method="GET" class="d-flex gap-2 float-start float-lg-end mb-3">
                    <select name="month" class="form-select" required>
                        @foreach ($reportMonths as $value => $label)
                            <option value="{{ $value }}" @selected($value === $selectedMonth)>{{ $label }}</option>
                        @endforeach
                    </select>
                    <button type="submit" class="btn btn-success text-nowrap">
                        <i class="bi bi-file-earmark-excel"></i> Unduh Excel
                    </button>
                </form>
            </div>
            @endif
        </div>
    </div>
    <section class="section">
        <div class="card">
            <div class="card-body">
                @if (session('success'))
                    <div class="alert alert-success alert-dismissible fade show" role="alert">
                        <p><i class="bi bi-check-circle-fill"></i> {{ session('success') }}</p>
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                    </div>
                @endif
                @if (session('error'))
                    <div class="alert alert-danger alert-dismissible fade show" role="alert">
                        <p>{{ session('error') }}</p>
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                    </div>
                @endif
                <ul class="nav nav-pills mb-3">
                    <li class="nav-item">
                        <a class="nav-link {{ $filter === \App\Models\Order::LIST_FILTER_ACTIVE ? 'active' : '' }}" href="{{ route('orders.index') }}">
                            Sedang Dilayani
                            <span class="badge {{ $filter === \App\Models\Order::LIST_FILTER_ACTIVE ? 'bg-light text-primary' : 'bg-secondary' }}">{{ $activeCount }}</span>
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link {{ $filter === \App\Models\Order::LIST_FILTER_SERVED ? 'active' : '' }}" href="{{ route('orders.index', ['filter' => \App\Models\Order::LIST_FILTER_SERVED]) }}">
                            Sudah Dilayani
                            <span class="badge {{ $filter === \App\Models\Order::LIST_FILTER_SERVED ? 'bg-light text-primary' : 'bg-secondary' }}">{{ $servedCount }}</span>
                        </a>
                    </li>
                </ul>
                @if ($orders->isEmpty())
                    <div class="alert alert-light border">
                        {{ $filter === \App\Models\Order::LIST_FILTER_SERVED
                            ? 'Belum ada pesanan yang selesai.'
                            : 'Belum ada pesanan yang sedang dilayani.' }}
                    </div>
                @endif
                <table class="table table-striped" id="table1">
                    <thead>
                        <tr>
                            <th>No</th>
                            <th>Kode Pesanan</th>
                            <th>Nama Pelanggan</th>
                            <th>Total</th>
                            <th>Status</th>
                            <th>No. Meja</th>
                            <th>Metode Pembayaran</th>
                            <th>Catatan</th>
                            <th>Dibuat Pada</th>
                            <th>Aksi</th>
                            <th>Ubah Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        @foreach ($orders as $order)
                        <tr>
                            <td>{{ $loop->iteration }}</td>
                            <td>
                                <div class="fw-semibold">{{ $order->order_code }}</div>
                                @foreach ($order->orderItems as $orderItem)
                                    @php
                                        $menuName = $orderItem->item->name ?? 'Menu';
                                        $addonNames = collect($orderItem->addons ?? [])->pluck('name')->filter()->implode(', ');
                                    @endphp
                                    <div class="small text-muted" title="{{ trim($menuName.($addonNames ? ' + '.$addonNames : '')) }}">
                                        {{ Str::limit($menuName, 22) }} x{{ $orderItem->quantity }}
                                        @if ($addonNames !== '')
                                            <span>+ {{ Str::limit($addonNames, 42) }}</span>
                                        @endif
                                    </div>
                                @endforeach
                            </td>
                            <td>{{ $order->user->fullname ?? '-' }}</td>
                            <td>{{ 'Rp'. number_format($order->grand_total, 0, ',', '.') }}</td>
                            <td>
                                <span class="badge {{ $order->kitchenStatusBadgeClass() }}">
                                    {{ $order->kitchenStatusLabel() }}
                                </span>
                            </td>
                            <td>{{ $order->table_number }}</td>
                            <td>{{ $order->payment_method }}</td>
                            <td>{{ $order->note ?? '-' }}</td>
                            <td>{{ $order->created_at->format('d-m-Y H:i') }}</td>
                            <td>
                                <a href="{{ route('orders.show', $order->id) }}" class="btn btn-primary btn-sm">
                                    <i class="bi bi-eye"></i> Lihat
                                </a>
                            </td>
                            <td>
                                @include('admin.order._status_form', ['order' => $order, 'kitchenStatuses' => $kitchenStatuses])
                            </td>
                        </tr>
                        @endforeach
                    </tbody>
                </table>
            </div>
        </div>
    </section>
</div>
@endsection

@section('script')
<script src="{{ asset('assets/admin/extensions/simple-datatables/umd/simple-datatables.js') }}"></script>
<script src="{{ asset('assets/admin/static/js/pages/simple-datatables.js') }}"></script>
@endsection
