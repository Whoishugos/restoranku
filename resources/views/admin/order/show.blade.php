@extends('admin.layouts.master')
@section('title', 'Detail Pesanan')

@section('css')
<link rel="stylesheet" href="{{ asset('assets/admin/extensions/simple-datatables/style.css') }}">
<link rel="stylesheet" href="{{ asset('assets/admin/compiled/css/table-datatable.css') }}">
@endsection

@section('content')
<div class="page-heading">
    <div class="page-title">
        <div class="row">
            <div class="col-12 col-md-6 order-md-1 order-last">
                <h3>Detail Pesanan</h3>
                <p class="text-subtitle text-muted">Informasi Detail Pesanan yang Masuk</p>
            </div>
            {{-- <div class="col-12 col-md-6 order-md-2 order-first">
                <a href="{{ route('items.create') }}" class="btn btn-primary float-start float-lg-end">
                    <i class="bi bi-plus"></i>
                    Tambah Menu
                </a>
            </div> --}}
        </div>
    </div>
    <section class="section">
        <div class="card">
            <div class="card-header">
                <h4>Kode Pesanan: {{ $order->order_code }}</h4>
            </div>
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
                <div class="row">
                    <div class="col-md-6">
                        <p>Dibuat Pada: {{ $order->created_at->format('d-m-Y H:i') }}</p>
                        <p>Nama Pelanggan: {{ $order->user->fullname }}</p>
                        <p>Pembayaran: {{ $order->paymentStatusLabel() }}</p>
                        <p>Status dapur:
                            <span class="badge {{ $order->kitchenStatusBadgeClass() }}">
                                {{ $order->kitchenStatusLabel() }}
                            </span>
                        </p>
                        @include('admin.order._status_form', ['order' => $order, 'kitchenStatuses' => $kitchenStatuses])
                    </div>
                    <div class="col-md-6">
                        <p>No. Meja: {{ $order->table_number }}</p>
                        <p>Metode Pembayaran: {{ $order->payment_method }}</p>
                        <p>Catatan: {{ $order->note ?? '-' }}</p>
                    </div>
                </div>
            </div>
        </div>

    </section>

    <section class="section">
        <div class="card">
            <div class="card-header">
                <h4>Daftar Menu yang Dipesan</h4>
            </div>
            <div class="card-body">
                <table class="table table-striped" id="table1">
                    <thead>
                        <tr>
                            <th>No</th>
                            <th>Gambar</th>
                            <th>Nama Menu</th>
                            <th>Jumlah</th>
                            <th>Harga</th>
                        </tr>
                    </thead>
                    <tbody>
                        @foreach ($orderItems as $menu)
                        <tr>

                            <td>{{ $loop->iteration }}</td>
                            <td>
                                <img src="{{ asset('img_item_upload/'. $menu->item->img) }}" width="60" class="img-fluid rounded-top" alt="" onerror="this.onerror=null;this.src='{{  $menu->item->img }}';">
                            </td>
                            <td>{{ $menu->item->name }}</td>
                            <td>{{ $menu->quantity }}</td>
                            <td>{{ 'Rp'. number_format($menu->item->price, 0, ',','.') }}</td>
                        </tr>

                        @endforeach
                    </tbody>

                        <tr>
                            <th colspan="4" class="text-end">Total</th>
                            <th>{{ 'Rp'. number_format($order->subtotal, 0, ',','.') }}</th>
                        </tr>
                        <tr>
                            <th colspan="4" class="text-end">Pajak</th>
                            <th>{{ 'Rp'. number_format($order->tax, 0, ',','.') }}</th>
                        </tr>
                        <tr>
                            <th colspan="4" class="text-end">Grand Total</th>
                            <th>{{ 'Rp'. number_format($order->grand_total, 0, ',','.') }}</th>
                        </tr>
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
