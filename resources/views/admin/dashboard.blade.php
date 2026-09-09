@extends('admin.layouts.master')
@section('title', 'Dashboard')

@section('css')

@endsection

@section('content')
    <div class="page-heading">
        <h3>Selamat Datang, {{ Auth::user()->fullname }}!</h3>
        <p class="text-subtitle text-muted">Ringkasan pesanan terbaru, yang menunggu paling lama, dan yang sudah dibayar.</p>
    </div>
    <div class="page-content">
        <section class="row">
            <div class="col-12 col-lg-12">
                <div class="row">
                    <div class="col-6 col-lg-3 col-md-6">
                        <div class="card">
                            <div class="card-body px-4 py-4-5">
                                <div class="row">
                                    <div class="col-md-4 col-lg-12 col-xl-12 col-xxl-5 d-flex justify-content-start ">
                                        <div class="stats-icon purple mb-2">
                                            <i class="iconly-boldWallet"></i>
                                        </div>
                                    </div>
                                    <div class="col-md-8 col-lg-12 col-xl-12 col-xxl-7">
                                        <h6 class="text-muted font-semibold">Pesanan Hari Ini</h6>
                                        <h6 class="font-extrabold mb-0">{{ $todayOrders }}</h6>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-6 col-lg-3 col-md-6">
                        <div class="card">
                            <div class="card-body px-4 py-4-5">
                                <div class="row">
                                    <div class="col-md-4 col-lg-12 col-xl-12 col-xxl-5 d-flex justify-content-start ">
                                        <div class="stats-icon blue">
                                            <i class="iconly-boldBuy"></i>
                                        </div>
                                    </div>
                                    <div class="col-md-8 col-lg-12 col-xl-12 col-xxl-7">
                                        <h6 class="text-muted font-semibold">Pendapatan Hari Ini</h6>
                                        <h6 class="font-extrabold mb-0">{{ 'Rp'. number_format($todayRevenue, 0, ',','.') }}</h6>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-6 col-lg-3 col-md-6">
                        <div class="card">
                            <div class="card-body px-4 py-4-5">
                                <div class="row">
                                    <div class="col-md-4 col-lg-12 col-xl-12 col-xxl-5 d-flex justify-content-start ">
                                        <div class="stats-icon green mb-2">
                                            <i class="iconly-boldFolder"></i>
                                        </div>
                                    </div>
                                    <div class="col-md-8 col-lg-12 col-xl-12 col-xxl-7">
                                        <h6 class="text-muted font-semibold">Total Pesanan</h6>
                                        <h6 class="font-extrabold mb-0">{{ $totalOrders }}</h6>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-6 col-lg-3 col-md-6">
                        <div class="card">
                            <div class="card-body px-4 py-4-5">
                                <div class="row">
                                    <div class="col-md-4 col-lg-12 col-xl-12 col-xxl-5 d-flex justify-content-start ">
                                        <div class="stats-icon blue mb-2">
                                            <i class="iconly-boldProfile"></i>
                                        </div>
                                    </div>
                                    <div class="col-md-8 col-lg-12 col-xl-12 col-xxl-7">
                                        <h6 class="text-muted font-semibold">Total Pendapatan</h6>
                                        <h6 class="font-extrabold mb-0">{{ 'Rp'. number_format($totalRevenue, 0, ',','.') }}</h6>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                @if ($newOrdersCount > 0)
                    <div class="alert alert-warning d-flex justify-content-between align-items-center" role="alert">
                        <div>
                            <i class="bi bi-bell-fill"></i>
                            Ada <strong>{{ $newOrdersCount }}</strong> pesanan yang masih perlu dilayani.
                        </div>
                        <a href="{{ route('orders.index') }}" class="btn btn-sm btn-outline-warning">Lihat daftar</a>
                    </div>
                @endif

                <div class="row" id="dashboard-order-lists" data-latest-order-id="{{ $latestOrderId }}">
                    <div class="col-12 col-lg-4 mb-4">
                        @include('admin.dashboard._order_list', [
                            'title' => 'Pesanan Terbaru',
                            'subtitle' => 'Masuk paling baru',
                            'orders' => $latestOrders,
                            'emptyText' => 'Belum ada pesanan terbaru.',
                        ])
                    </div>
                    <div class="col-12 col-lg-4 mb-4">
                        @include('admin.dashboard._order_list', [
                            'title' => 'Pesanan Terlama',
                            'subtitle' => 'Menunggu paling lama',
                            'orders' => $oldestOrders,
                            'emptyText' => 'Tidak ada pesanan yang menunggu.',
                        ])
                    </div>
                    <div class="col-12 col-lg-4 mb-4">
                        @include('admin.dashboard._order_list', [
                            'title' => 'Sudah Dibayarkan',
                            'subtitle' => 'Pembayaran sudah diterima',
                            'orders' => $paidOrders,
                            'emptyText' => 'Belum ada pesanan yang dibayar.',
                        ])
                    </div>
                </div>
            </div>
        </section>
    </div>
@endsection

@section('script')

@endsection
