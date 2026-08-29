@extends('customer.layouts.master')

@section('content')
<!-- Single Page Header start -->
<div class="container-fluid page-header py-5">
    <h1 class="text-center text-white display-6">Checkout</h1>
    <ol class="breadcrumb justify-content-center mb-0">
        <li class="breadcrumb-item active text-primary">Silakan isi detail pemesanan Anda</li>
    </ol>
</div>
<!-- Single Page Header End -->
<div class="container-fluid py-5">
    <div class="container py-5">
        <h1 class="mb-4">Detail Pembayaran</h1>
        @if (session('error'))
            <div class="alert alert-danger">{{ session('error') }}</div>
        @endif
        @if ($errors->any())
            <div class="alert alert-danger">{{ $errors->first() }}</div>
        @endif
        <form id="checkout-form" action="{{ route('checkout.store') }}" method="POST">
            @csrf
            <div class="row g-5">
                <div class="col-md-12 col-lg-6 col-xl-6">
                    <div class="row">
                        <div class="col-md-12 col-lg-4">                            <div class="form-item w-100">
                                <label class="form-label my-3">Nama Lengkap<sup>*</sup></label>
                                <input type="text" name="fullname" class="form-control" placeholder="Masukka nama Anda" required>
                            </div>
                        </div>
                        <div class="col-md-12 col-lg-4">
                            <div class="form-item w-100">
                                <label class="form-label my-3">Nomor WhatsApp<sup>*</sup></label>
                                <input type="text" name="phone" class="form-control" placeholder="Masukkan Nomor WhatsApp Anda" required>
                            </div>
                        </div>
                        <div class="col-md-12 col-lg-4">
                            <div class="form-item w-100">
                                <label class="form-label my-3">Nomor Meja<sup>*</sup></label>
                                <input type="number" name="table_number" class="form-control" min="1" max="99" placeholder="Contoh: 5" value="{{ old('table_number', $tableNumber) }}" required>
                            </div>
                        </div>
                    </div>
                    <br>
                    <div class="row">
                        <div class="col-md-12 col-lg-12">
                            <div class="form-item">
                                <textarea name="note" class="form-control" spellcheck="false" cols="30" rows="5" placeholder="Catatan pesanan (Opsional)"></textarea>
                            </div>
                        </div>
                    </div>
                    <div class="row">
                        <div class="table-responsive">
                            <br><br>
                            <h4 class="mb-4">Detail Pesanan</h4>
                            <table class="table">
                                <thead>
                                    <tr>
                                        <th scope="col">Gambar</th>
                                        <th scope="col">Menu</th>
                                        <th scope="col">Harga</th>
                                        <th scope="col">Jumlah</th>
                                        <th scope="col">Total</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    @php
                                        $subTotal = 0;
                                    @endphp
                                    @foreach (session('cart') as $item)
                                        @php
                                            $itemTotal = \App\Support\CartLine::lineTotal($item);
                                            $unitPrice = \App\Support\CartLine::unitPrice($item);
                                            $addonLabel = \App\Support\CartLine::addonNames($item);
                                            $subTotal += $itemTotal;
                                        @endphp
                                    <tr>
                                        <th scope="row">
                                            <div class="d-flex align-items-center mt-2">
                                                <img src="{{ asset('img_item_upload/'. $item['image']) }}" class="img-fluid me-5 rounded-circle" style="width: 80px; height: 80px;" alt="" onerror="this.onerror=null;this.src='{{  $item['image'] }}';">
                                            </div>
                                        </th>
                                        <td class="py-5">
                                            {{ $item['name'] }}
                                            @foreach ($item['addons'] ?? [] as $addon)
                                                <div class="small">
                                                    <span class="badge {{ \App\Models\AddonGroup::typeBadgeClass($addon['type'] ?? '') }}">{{ $addon['type_label'] ?? 'Add-on' }}: {{ $addon['name'] }}</span>
                                                </div>
                                            @endforeach
                                        </td>
                                        <td class="py-5">{{ 'Rp'. number_format($unitPrice, 0, ',','.') }}</td>
                                        <td class="py-5">{{ $item['qty'] }}</td>
                                        <td class="py-5">{{ 'Rp'. number_format($itemTotal, 0, ',','.') }}</td>
                                    </tr>
                                    @endforeach
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
                @php
                    $tax = $subTotal * 0.1;
                    $total = $subTotal + $tax;
                @endphp
                <div class="col-md-12 col-lg-6 col-xl-6">
                    <div class="row g-4 align-items-center py-3">
                        <div class="col-lg-12">
                            <div class="bg-light rounded">
                                <div class="p-4">
                                    <h3 class="display-6 mb-4">Total <span class="fw-normal">Pesanan</span></h3>
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
                                <div class="py-4 mb-4 border-top border-bottom d-flex justify-content-between">
                                    <h4 class="mb-0 ps-4 me-4">Total</h4>
                                    <h5 class="mb-0 pe-4">Rp{{ number_format($total, 0, ',','.') }}</h5>
                                </div>

                                <div class="py-4 mb-4 d-flex justify-content-between">
                                    <h5 class="mb-0 ps-4 me-4">Metode Pembayaran</h5>
                                    <div class="mb-0 pe-4 mb-3 pe-5">
                                        <div class="form-check">
                                            <input type="radio" class="form-check-input bg-primary border-0" id="qris" name="payment_method" value="qris" checked>
                                            <label class="form-check-label" for="qris">QRIS (Midtrans)</label>
                                        </div>
                                        <div class="form-check">
                                            <input type="radio" class="form-check-input bg-primary border-0" id="cash" name="payment_method" value="tunai">
                                            <label class="form-check-label" for="cash">Tunai di kasir</label>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            @if (! $midtransConfigured)
                                <p class="text-danger small mt-2">QRIS belum siap: isi MIDTRANS_SERVER_KEY dan MIDTRANS_CLIENT_KEY di file .env.</p>
                            @endif
                            <div class="d-flex justify-content-end">
                                <button type="button" id="pay-button" class="btn border-secondary py-3 text-uppercase text-primary">Bayar Sekarang</button>
                            </div>

                        </div>
                    </div>
                </div>
            </div>
        </form>
    </div>
</div>
@endsection

@section('script')
@if ($midtransConfigured)
<script src="{{ config('midtrans.snap_url') }}" data-client-key="{{ config('midtrans.client_key') }}"></script>
@endif
<script>
    document.addEventListener("DOMContentLoaded", function () {
        const payButton = document.getElementById("pay-button");
        const form = document.getElementById("checkout-form");
        const successUrlTemplate = @json(route('checkout.success', ['orderId' => '__ORDER__']));

        payButton.addEventListener("click", function () {
            let paymentMethod = document.querySelector('input[name="payment_method"]:checked');

            if (!paymentMethod) {
                alert("Pilih metode pembayaran terlebih dahulu.");
                return;
            }

            if (!form.reportValidity()) {
                return;
            }

            paymentMethod = paymentMethod.value;
            payButton.disabled = true;

            if (paymentMethod === "tunai") {
                form.submit();
                return;
            }

            if (typeof snap === "undefined") {
                payButton.disabled = false;
                alert("Midtrans belum siap. Periksa Client Key di .env.");
                return;
            }

            const formData = new FormData(form);

            fetch("{{ route('checkout.store') }}", {
                method: "POST",
                body: formData,
                headers: {
                    "Accept": "application/json",
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRF-TOKEN": "{{ csrf_token() }}"
                }
            })
            .then(async (response) => {
                const data = await response.json().catch(() => ({}));
                if (!response.ok) {
                    throw new Error(data.message || "Gagal membuat pembayaran.");
                }
                return data;
            })
            .then((data) => {
                if (!data.snap_token) {
                    throw new Error(data.message || "Token pembayaran tidak tersedia.");
                }

                const successUrl = successUrlTemplate.replace("__ORDER__", encodeURIComponent(data.order_code));

                snap.pay(data.snap_token, {
                    onSuccess: function () {
                        window.location.href = successUrl;
                    },
                    onPending: function () {
                        window.location.href = successUrl;
                    },
                    onError: function () {
                        payButton.disabled = false;
                        alert("Pembayaran gagal. Silakan coba lagi.");
                    },
                    onClose: function () {
                        window.location.href = successUrl;
                    }
                });
            })
            .catch((error) => {
                payButton.disabled = false;
                alert(error.message || "Terjadi kesalahan, silakan coba lagi.");
            });
        });
    });
</script>
@endsection

