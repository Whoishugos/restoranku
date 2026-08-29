@extends('customer.layouts.master')

@section('content')
<!-- Single Page Header start -->
<div class="container-fluid page-header py-5">
    <h1 class="text-center text-white display-6">Keranjang</h1>
    <ol class="breadcrumb justify-content-center mb-0">
        <li class="breadcrumb-item active text-primary">Silakan periksa pesanan Anda</li>
    </ol>
</div>
<!-- Single Page Header End -->
<div class="container-fluid py-5">
    <div class="container py-5">
        @if (session('success'))
            <div class="alert alert-success alert-dismissible fade show" role="alert">
                {{ session('success') }}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        @endif
        @if (session('error'))
            <div class="alert alert-danger alert-dismissible fade show" role="alert">
                {{ session('error') }}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        @endif
        @if (empty($cart))
            <h4 class="text-center">Keranjang anda kosong</h4>
        @else
        <div class="table-responsive">
            <table class="table">
                <thead>
                  <tr>
                    <th scope="col">Gambar</th>
                    <th scope="col">Menu</th>
                    <th scope="col">Harga</th>
                    <th scope="col">Jumlah</th>
                    <th scope="col">Total</th>
                    <th scope="col">Aksi</th>
                  </tr>
                </thead>
                <tbody>
                    @php
                        $subTotal = 0;
                    @endphp
                    @foreach ($cart as $lineKey => $item)
                        @php
                            $cartKey = $item['key'] ?? $lineKey;
                            $itemTotal = \App\Support\CartLine::lineTotal($item);
                            $unitPrice = \App\Support\CartLine::unitPrice($item);
                            $subTotal += $itemTotal;
                            $addonLabel = \App\Support\CartLine::addonNames($item);
                        @endphp
                    <tr>
                        <th scope="row">
                            <div class="d-flex align-items-center">
                                <img src="{{ asset('img_item_upload/'. $item['image']) }}" class="img-fluid me-5 rounded-circle" style="width: 80px; height: 80px;" alt="" onerror="this.onerror=null;this.src='{{  $item['image'] }}';">
                            </div>
                        </th>
                        <td>
                            <p class="mb-0 mt-4">{{ $item['name'] }}</p>
                            @foreach ($item['addons'] ?? [] as $addon)
                                <span class="badge {{ \App\Models\AddonGroup::typeBadgeClass($addon['type'] ?? '') }} me-1">
                                    {{ $addon['type_label'] ?? 'Add-on' }}: {{ $addon['name'] }}
                                </span>
                            @endforeach
                        </td>
                        <td>
                            <p class="mb-0 mt-4">{{ 'Rp'. number_format($unitPrice, 0, ',','.') }}</p>
                        </td>
                        <td>
                            <div class="input-group quantity mt-4" style="width: 100px;">
                                <div class="input-group-btn">
                                    <button class="btn btn-sm btn-minus rounded-circle bg-light border" onclick="updateQuantity('{{ $cartKey }}', -1)">
                                        <i class="fa fa-minus"></i>
                                    </button>
                                </div>
                                <input id="qty-{{ $cartKey }}" type="text" class="form-control form-control-sm text-center border-0 bg-transparent" value="{{ $item['qty'] }}" readonly>
                                <div class="input-group-btn">
                                    <button class="btn btn-sm btn-plus rounded-circle bg-light border" onclick="updateQuantity('{{ $cartKey }}', 1)">
                                        <i class="fa fa-plus"></i>
                                    </button>
                                </div>
                            </div>
                        </td>
                        <td>
                            <p class="mb-0 mt-4">{{ 'Rp'. number_format($itemTotal, 0, ',','.') }}</p>
                        </td>
                        <td>
                            <button class="btn btn-md rounded-circle bg-light border mt-4" onclick="if(confirm('Apakah anda yakin ingin menghapus item ini?')) { removeItemFromCart('{{ $cartKey }}') }">
                                <i class="fa fa-times text-danger"></i>
                            </button>
                        </td>
                    </tr>
                    @endforeach
                </tbody>
            </table>
        </div>
        @php
            $tax = $subTotal * 0.1;
            $total = $subTotal + $tax;
        @endphp
        <div class="d-flex justify-content-end">
            <a href="{{ route('cart.clear') }}" class="btn btn-danger" onclick=" return confirm('Apakah Anda yakin ingin mengosongkan keranjang?')">Kosongkan Keranjang</a>
        </div>
        <div class="row g-4 justify-content-end mt-1">
            <div class="col-8"></div>
            <div class="col-sm-8 col-md-7 col-lg-6 col-xl-4">
                <div class="bg-light rounded">
                    <div class="p-4">
                        <h2 class="display-6 mb-4">Total <span class="fw-normal">Pesanan</span></h2>
                        <div class="d-flex justify-content-between mb-4">
                            <h5 class="mb-0 me-4">Subtotal</h5>
                            <p class="mb-0">Rp{{ number_format($subTotal, 0, ',','.') }}</p>
                        </div>
                        <div class="d-flex justify-content-between">
                            <p class="mb-0 me-4">Pajak (10%)</p>
                            <div class="">
                                <p class="mb-0">Rp{{ number_format($tax, 0, ',','.') }}</p>
                            </div>
                        </div>
                    </div>
                    <div class="py-4 mb-4 border-top d-flex justify-content-between">
                        <h4 class="mb-0 ps-4 me-4">Total</h4>
                        <h5 class="mb-0 pe-4">Rp{{ number_format($total, 0, ',','.') }}</h5>
                    </div>
                </div>
                <div class="d-flex justify-content-end">
                    <div class="mb-0 mb-3">
                        <a href="{{ route('checkout') }}" class="btn border-secondary py-3 text-primary text-uppercase mb-4">Lanjut ke Pembayaran</a>
                    </div>
                </div>
            </div>
        </div>
        @endif
    </div>
</div>
@endsection

@section('script')
    <script>
        function updateQuantity(itemId, change) {
            var qtyInput = document.getElementById('qty-' + itemId);
            var currentQty = parseInt(qtyInput.value, 10);
            var newQty = currentQty + change;

            fetch("{{ route('cart.update') }}", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'X-CSRF-TOKEN': '{{ csrf_token() }}'
                },
                body: JSON.stringify({ id: itemId, qty: newQty })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    alert(data.message || 'Gagal memperbarui keranjang');
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                alert('Terjadi kesalahan saat mengupdate keranjang');
            });
        }

        function saveAddons(itemId) {
            var boxes = document.querySelectorAll('.addon-input[data-item-id="' + itemId + '"]:checked');
            var addonIds = Array.from(boxes).map(function (box) {
                return parseInt(box.value, 10);
            });

            fetch("{{ route('cart.addons') }}", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'X-CSRF-TOKEN': '{{ csrf_token() }}'
                },
                body: JSON.stringify({ id: itemId, addon_ids: addonIds })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    alert(data.message || 'Gagal menyimpan add-ons');
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                alert('Terjadi kesalahan saat menyimpan add-ons');
            });
        }

        function removeItemFromCart(itemId) {
            fetch("{{ route('cart.remove') }}", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-TOKEN': '{{ csrf_token() }}'
                },
                body: JSON.stringify({ id: itemId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    alert(data.message);
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                alert('Terjadi kesalahan saat menghapus item dari keranjang');
            });
        }
    </script>
@endsection
