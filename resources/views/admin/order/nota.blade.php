<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nota {{ $order->order_code }}</title>
    <style>
        * { box-sizing: border-box; }
        body {
            margin: 0;
            background: #f3f4f6;
            font-family: "Segoe UI", Tahoma, sans-serif;
            color: #111;
        }
        .toolbar {
            display: flex;
            justify-content: center;
            gap: 8px;
            padding: 16px;
        }
        .toolbar a, .toolbar button {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 8px 14px;
            border: 1px solid #111;
            background: #111;
            color: #fff;
            text-decoration: none;
            font-size: 14px;
            border-radius: 6px;
            cursor: pointer;
        }
        .toolbar a.secondary {
            background: #fff;
            color: #111;
        }
        .nota {
            width: 80mm;
            margin: 0 auto 32px;
            background: #fff;
            padding: 12px 14px 18px;
            box-shadow: 0 8px 24px rgba(0,0,0,.08);
        }
        .nota-header { text-align: center; }
        .nota-header img { width: 52px; height: 52px; object-fit: contain; }
        .nota-header h1 { font-size: 14px; margin: 6px 0 2px; }
        .nota-header p { margin: 0; font-size: 11px; color: #444; }
        .divider {
            border: 0;
            border-top: 1px dashed #999;
            margin: 10px 0;
        }
        table { width: 100%; border-collapse: collapse; font-size: 12px; }
        td { vertical-align: top; padding: 2px 0; }
        .muted { color: #555; font-size: 11px; }
        .meta td:first-child { color: #555; width: 42%; }
        .totals td { padding-top: 3px; }
        .totals .label { text-align: right; padding-right: 8px; }
        .totals .grand { font-weight: 700; font-size: 13px; }
        .thanks { text-align: center; font-size: 11px; margin: 8px 0 0; }
        .item-name { font-weight: 600; }
        .addon { display: block; font-size: 11px; color: #555; }
        .qty { white-space: nowrap; padding-right: 6px; }
        .price { text-align: right; white-space: nowrap; }
        @media print {
            body { background: #fff; }
            .toolbar { display: none !important; }
            .nota {
                width: 80mm;
                margin: 0;
                box-shadow: none;
                padding: 0;
            }
            @page { size: 80mm auto; margin: 4mm; }
        }
    </style>
</head>
<body>
    <div class="toolbar">
        <button type="button" onclick="window.print()">Cetak Nota</button>
        <a class="secondary" href="{{ route('orders.show', $order->id) }}">Kembali</a>
    </div>

    <div class="nota">
        <div class="nota-header">
            <img src="{{ asset('img/logo-kekupu.png') }}" alt="Logo Kekupu">
            <h1>{{ config('app.name') }}</h1>
            <p>Nota pesanan</p>
        </div>

        <hr class="divider">

        <table class="meta">
            <tr>
                <td>Kode</td>
                <td>{{ $order->order_code }}</td>
            </tr>
            <tr>
                <td>Tanggal</td>
                <td>{{ $order->created_at->format('d-m-Y H:i') }}</td>
            </tr>
            <tr>
                <td>Pelanggan</td>
                <td>{{ $order->user->fullname ?? '-' }}</td>
            </tr>
            <tr>
                <td>Meja</td>
                <td>{{ $order->table_number }}</td>
            </tr>
            <tr>
                <td>Pembayaran</td>
                <td>{{ strtoupper($order->payment_method) }} · {{ $order->paymentStatusLabel() }}</td>
            </tr>
            @if ($order->note)
            <tr>
                <td>Catatan</td>
                <td>{{ $order->note }}</td>
            </tr>
            @endif
        </table>

        <hr class="divider">

        <table>
            @foreach ($orderItems as $menu)
                <tr>
                    <td class="qty">{{ $menu->quantity }}x</td>
                    <td>
                        <span class="item-name">{{ $menu->item->name ?? 'Menu dihapus' }}</span>
                        @foreach ($menu->addons ?? [] as $addon)
                            <span class="addon">+ {{ $addon['name'] ?? '' }}</span>
                        @endforeach
                    </td>
                    <td class="price">{{ 'Rp'. number_format($menu->price ?? 0, 0, ',', '.') }}</td>
                </tr>
            @endforeach
        </table>

        <hr class="divider">

        <table class="totals">
            <tr>
                <td class="label">Subtotal</td>
                <td class="price">{{ 'Rp'. number_format($order->subtotal, 0, ',', '.') }}</td>
            </tr>
            <tr>
                <td class="label">Pajak</td>
                <td class="price">{{ 'Rp'. number_format($order->tax, 0, ',', '.') }}</td>
            </tr>
            <tr>
                <td class="label grand">Grand Total</td>
                <td class="price grand">{{ 'Rp'. number_format($order->grand_total, 0, ',', '.') }}</td>
            </tr>
        </table>

        <hr class="divider">
        <p class="thanks">Terima kasih telah berkunjung.<br>Selamat menikmati.</p>
    </div>

    <script>
        window.addEventListener('load', function () {
            window.print();
        });
    </script>
</body>
</html>
