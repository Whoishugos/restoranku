<?php

namespace App\Http\Controllers;

use App\Models\Order;
use App\Services\MidtransService;
use App\Services\MonthlyOrderExcelExporter;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class OrderController extends Controller
{
    public function index(MonthlyOrderExcelExporter $exporter, MidtransService $midtrans)
    {
        $this->syncPendingQrisPayments($midtrans);

        $orders = Order::with(['user', 'orderItems.item'])->latest()->get();
        $kitchenStatuses = Order::kitchenStatusOptions();
        $reportMonths = $exporter->monthOptions();
        $selectedMonth = now()->format('Y-m');
        $canExportReport = in_array(Auth::user()->role->role_name ?? '', ['admin', 'cashier'], true);

        return view('admin.order.index', compact(
            'orders',
            'kitchenStatuses',
            'reportMonths',
            'selectedMonth',
            'canExportReport'
        ));
    }

    public function exportExcel(Request $request, MonthlyOrderExcelExporter $exporter)
    {
        if (! in_array(Auth::user()->role->role_name ?? '', ['admin', 'cashier'], true)) {
            abort(403);
        }

        $validated = $request->validate([
            'month' => ['required', 'date_format:Y-m'],
        ]);

        return $exporter->download($validated['month']);
    }

    public function show($id, MidtransService $midtrans)
    {
        $order = Order::with(['user', 'orderItems.item'])->findOrFail($id);
        $this->syncPendingQrisPayments($midtrans, $order);
        $order->refresh()->load(['user', 'orderItems.item']);
        $orderItems = $order->orderItems;
        $kitchenStatuses = Order::kitchenStatusOptions();

        return view('admin.order.show', compact('order', 'orderItems', 'kitchenStatuses'));
    }

    public function nota($id)
    {
        $order = Order::with(['user', 'orderItems.item'])->findOrFail($id);
        $orderItems = $order->orderItems;

        return view('admin.order.nota', compact('order', 'orderItems'));
    }

    public function confirmPayment($id)
    {
        $role = Auth::user()->role->role_name ?? null;
        if (! in_array($role, ['admin', 'cashier'], true)) {
            abort(403);
        }

        $order = Order::findOrFail($id);

        if ($order->payment_method !== 'tunai' || $order->isPaid()) {
            return redirect()->route('orders.index')->with('error', 'Pesanan ini tidak menunggu pembayaran tunai.');
        }

        $order->markAsPaid();

        return redirect()->route('orders.index')->with('success', 'Pembayaran diterima. Pesanan masuk ke proses.');
    }

    public function updateKitchenStatus(Request $request, $id)
    {
        $role = Auth::user()->role->role_name ?? null;
        if (! in_array($role, ['admin', 'cashier', 'chef'], true)) {
            abort(403);
        }

        $validated = $request->validate([
            'kitchen_status' => 'required|in:processing,cooking,ready',
        ]);

        $order = Order::findOrFail($id);

        if (! $order->isPaid()) {
            return redirect()->back()->with('error', 'Konfirmasi pembayaran terlebih dahulu sebelum mengubah status dapur.');
        }

        $order->kitchen_status = $validated['kitchen_status'];
        if ($order->status === 'cooked') {
            $order->status = 'settlement';
        }
        $order->save();

        return redirect()->back()->with('success', 'Status pesanan diperbarui menjadi '.$order->kitchenStatusLabel().'.');
    }

    private function syncPendingQrisPayments(MidtransService $midtrans, ?Order $only = null): void
    {
        if (! $midtrans->isConfigured()) {
            return;
        }

        $orders = $only
            ? collect($only->payment_method === 'qris' && ! $only->isPaid() ? [$only] : [])
            : Order::query()
                ->where('payment_method', 'qris')
                ->where('status', 'pending')
                ->latest()
                ->limit(25)
                ->get();

        foreach ($orders as $order) {
            try {
                $status = $midtrans->transactionStatus($order->order_code);
                $transactionStatus = is_object($status) ? (string) ($status->transaction_status ?? '') : '';
                $transactionTime = is_object($status) ? ($status->transaction_time ?? null) : null;
                $fraudStatus = is_object($status) ? ($status->fraud_status ?? null) : null;
                $paymentType = is_object($status) ? ($status->payment_type ?? null) : null;
                $order->applyGatewayTransaction($transactionStatus, $fraudStatus, $paymentType, $transactionTime);
            } catch (\Throwable) {
                // Webhook Midtrans tetap menjadi sumber utama.
            }
        }
    }
}
