<?php

namespace App\Services;

use App\Models\Order;
use Carbon\Carbon;
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\DB;
use Symfony\Component\HttpFoundation\StreamedResponse;

class MonthlyOrderExcelExporter
{
    private const MONTHS = [
        1 => 'Januari',
        2 => 'Februari',
        3 => 'Maret',
        4 => 'April',
        5 => 'Mei',
        6 => 'Juni',
        7 => 'Juli',
        8 => 'Agustus',
        9 => 'September',
        10 => 'Oktober',
        11 => 'November',
        12 => 'Desember',
    ];

    public function monthOptions(): array
    {
        $options = [];

        foreach ($this->yearMonthsFromOrders() as $ym) {
            $date = Carbon::parse($ym.'-01')->startOfMonth();
            $options[$ym] = $this->monthLabel($date);
        }

        $current = now()->format('Y-m');
        if (! isset($options[$current])) {
            $options[$current] = $this->monthLabel(now()->startOfMonth());
        }

        krsort($options);

        return $options;
    }

    public function download(string $yearMonth): StreamedResponse
    {
        $period = Carbon::parse($yearMonth.'-01')->startOfMonth();
        $orders = Order::with(['user', 'orderItems.item'])
            ->whereBetween('created_at', [$period->copy()->startOfMonth(), $period->copy()->endOfMonth()])
            ->orderBy('created_at')
            ->get();

        $paid = $orders->filter(fn (Order $order) => $order->isPaid());
        $unpaid = $orders->reject(fn (Order $order) => $order->isPaid());

        $gross = (int) $paid->sum('subtotal');
        $tax = (int) $paid->sum('tax');
        $revenue = (int) $paid->sum('grand_total');

        $xml = $this->workbookXml([
            'Ringkasan' => $this->summaryRows($period, $orders, $paid, $unpaid, $gross, $tax, $revenue),
            'Pesanan' => $this->orderRows($orders),
            'Pendapatan' => $this->revenueRows($paid, $gross, $tax, $revenue),
            'Pelanggan' => $this->customerRows($orders),
        ]);

        $filename = 'laporan-kekupu-villa-jembrana-'.$yearMonth.'.xls';

        return response()->streamDownload(function () use ($xml) {
            echo $xml;
        }, $filename, [
            'Content-Type' => 'application/vnd.ms-excel; charset=UTF-8',
        ]);
    }

    public function monthLabel(Carbon $date): string
    {
        return self::MONTHS[(int) $date->month].' '.$date->year;
    }

    /**
     * @return list<string>
     */
    private function yearMonthsFromOrders(): array
    {
        $driver = DB::connection()->getDriverName();
        $expression = match ($driver) {
            'sqlite' => "strftime('%Y-%m', created_at)",
            'pgsql' => "to_char(created_at, 'YYYY-MM')",
            default => "DATE_FORMAT(created_at, '%Y-%m')",
        };

        return Order::query()
            ->selectRaw($expression.' as ym')
            ->whereNotNull('created_at')
            ->distinct()
            ->orderByDesc('ym')
            ->pluck('ym')
            ->filter()
            ->values()
            ->all();
    }

    /**
     * @param  array<string, list<list<array{0: string, 1: int|float|string}>>>  $sheets
     */
    private function workbookXml(array $sheets): string
    {
        $xml = '<?xml version="1.0" encoding="UTF-8"?>'.PHP_EOL;
        $xml .= '<?mso-application progid="Excel.Sheet"?>'.PHP_EOL;
        $xml .= '<Workbook xmlns="urn:schemas-microsoft-com:office:spreadsheet"';
        $xml .= ' xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet">';
        $xml .= '<Styles>';
        $xml .= '<Style ss:ID="header"><Font ss:Bold="1"/></Style>';
        $xml .= '<Style ss:ID="number"><NumberFormat ss:Format="#,##0"/></Style>';
        $xml .= '</Styles>';

        foreach ($sheets as $name => $rows) {
            $xml .= '<Worksheet ss:Name="'.$this->xml($name).'"><Table>';
            foreach ($rows as $index => $row) {
                $xml .= '<Row>';
                foreach ($row as $cell) {
                    [$type, $value] = $cell;
                    $style = $index === 0 ? ' ss:StyleID="header"' : ($type === 'Number' ? ' ss:StyleID="number"' : '');
                    $xml .= '<Cell'.$style.'><Data ss:Type="'.$type.'">'.$this->xml((string) $value).'</Data></Cell>';
                }
                $xml .= '</Row>';
            }
            $xml .= '</Table></Worksheet>';
        }

        $xml .= '</Workbook>';

        return $xml;
    }

    /**
     * @return list<list<array{0: string, 1: int|float|string}>>
     */
    private function summaryRows(Carbon $period, Collection $orders, Collection $paid, Collection $unpaid, int $gross, int $tax, int $revenue): array
    {
        return [
            $this->stringRow(['Laporan Bulanan '.config('app.name'), '']),
            $this->stringRow(['Periode', $this->monthLabel($period)]),
            $this->stringRow(['Dicetak', now()->format('d-m-Y H:i')]),
            $this->stringRow(['', '']),
            $this->mixedRow(['Uraian', 'Nilai'], true),
            $this->mixedRow(['Jumlah pesanan terdaftar', $orders->count()]),
            $this->mixedRow(['Pesanan sudah dibayar', $paid->count()]),
            $this->mixedRow(['Pesanan belum dibayar', $unpaid->count()]),
            $this->mixedRow(['Pendapatan kotor (subtotal lunas)', $gross]),
            $this->mixedRow(['Pajak', $tax]),
            $this->mixedRow(['Pendapatan (grand total lunas)', $revenue]),
            $this->mixedRow(['Nilai pesanan belum dibayar', (int) $unpaid->sum('grand_total')]),
        ];
    }

    /**
     * @return list<list<array{0: string, 1: int|float|string}>>
     */
    private function orderRows(Collection $orders): array
    {
        $rows = [
            $this->stringRow([
                'No',
                'Kode Pesanan',
                'Tanggal',
                'Nama Pelanggan',
                'Email',
                'Telepon',
                'No. Meja',
                'Metode Pembayaran',
                'Status Pembayaran',
                'Status Dapur',
                'Menu',
                'Subtotal',
                'Pajak',
                'Grand Total',
                'Catatan',
            ]),
        ];

        foreach ($orders as $index => $order) {
            $menu = $order->orderItems
                ->map(function ($orderItem) {
                    $name = $orderItem->item->name ?? 'Menu dihapus';
                    $addons = $orderItem->addonLabel();
                    if ($addons !== '') {
                        $name .= ' + '.$addons;
                    }

                    return $name.' x'.$orderItem->quantity;
                })
                ->implode(', ');

            $rows[] = $this->mixedRow([
                $index + 1,
                $order->order_code,
                $order->created_at->format('d-m-Y H:i'),
                $order->user->fullname ?? '-',
                $order->user->email ?? '-',
                $order->user->phone ?? '-',
                $order->table_number,
                $order->payment_method,
                $order->paymentStatusLabel(),
                $order->kitchenStatusLabel(),
                $menu !== '' ? $menu : '-',
                (int) $order->subtotal,
                (int) $order->tax,
                (int) $order->grand_total,
                $order->note ?: '-',
            ]);
        }

        return $rows;
    }

    /**
     * @return list<list<array{0: string, 1: int|float|string}>>
     */
    private function revenueRows(Collection $paid, int $gross, int $tax, int $revenue): array
    {
        $rows = [
            $this->mixedRow(['Uraian', 'Nilai'], true),
            $this->mixedRow(['Pendapatan kotor', $gross]),
            $this->mixedRow(['Pajak', $tax]),
            $this->mixedRow(['Pendapatan', $revenue]),
            $this->stringRow(['', '']),
            $this->stringRow(['Tanggal', 'Jumlah Pesanan Lunas', 'Pendapatan Kotor', 'Pajak', 'Pendapatan']),
        ];

        $byDay = $paid->groupBy(fn (Order $order) => $order->created_at->format('Y-m-d'));

        foreach ($byDay as $date => $dayOrders) {
            $rows[] = $this->mixedRow([
                Carbon::parse($date)->format('d-m-Y'),
                $dayOrders->count(),
                (int) $dayOrders->sum('subtotal'),
                (int) $dayOrders->sum('tax'),
                (int) $dayOrders->sum('grand_total'),
            ]);
        }

        return $rows;
    }

    /**
     * @return list<list<array{0: string, 1: int|float|string}>>
     */
    private function customerRows(Collection $orders): array
    {
        $rows = [
            $this->stringRow([
                'No',
                'Nama',
                'Email',
                'Telepon',
                'Jumlah Pesanan',
                'Pesanan Lunas',
                'Total Belanja',
                'Pendapatan Kotor',
                'Pesanan Pertama',
                'Pesanan Terakhir',
            ]),
        ];

        $grouped = $orders->groupBy('user_id')->values();

        foreach ($grouped as $index => $customerOrders) {
            $user = $customerOrders->first()?->user;
            $paid = $customerOrders->filter(fn (Order $order) => $order->isPaid());

            $rows[] = $this->mixedRow([
                $index + 1,
                $user?->fullname ?? '-',
                $user?->email ?? '-',
                $user?->phone ?? '-',
                $customerOrders->count(),
                $paid->count(),
                (int) $customerOrders->sum('grand_total'),
                (int) $paid->sum('subtotal'),
                $customerOrders->sortBy('created_at')->first()?->created_at?->format('d-m-Y H:i') ?? '-',
                $customerOrders->sortByDesc('created_at')->first()?->created_at?->format('d-m-Y H:i') ?? '-',
            ]);
        }

        return $rows;
    }

    /**
     * @param  list<string>  $values
     * @return list<array{0: string, 1: int|float|string}>
     */
    private function stringRow(array $values): array
    {
        return array_map(fn ($value) => ['String', $value], $values);
    }

    /**
     * @param  list<int|float|string>  $values
     * @return list<array{0: string, 1: int|float|string}>
     */
    private function mixedRow(array $values, bool $forceString = false): array
    {
        $row = [];
        foreach ($values as $value) {
            if (! $forceString && (is_int($value) || is_float($value))) {
                $row[] = ['Number', $value];
            } else {
                $row[] = ['String', $value];
            }
        }

        return $row;
    }

    private function xml(string $value): string
    {
        return htmlspecialchars($value, ENT_XML1 | ENT_QUOTES, 'UTF-8');
    }
}
