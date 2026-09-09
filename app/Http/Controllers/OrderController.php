<?php

namespace App\Http\Controllers;

use App\Models\Order;
use App\Services\MonthlyOrderExcelExporter;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Validation\Rule;

class OrderController extends Controller
{
    public function index(Request $request, MonthlyOrderExcelExporter $exporter)
    {
        $filter = $request->query('filter', Order::LIST_FILTER_ACTIVE);
        if (! array_key_exists($filter, Order::listFilters())) {
            $filter = Order::LIST_FILTER_ACTIVE;
        }

        $ordersQuery = Order::with(['user', 'orderItems.item'])->latest();
        if ($filter === Order::LIST_FILTER_SERVED) {
            $ordersQuery->served();
        } else {
            $ordersQuery->notServed();
        }

        $orders = $ordersQuery->get();
        $kitchenStatuses = Order::kitchenStatusOptions();
        $reportMonths = $exporter->monthOptions();
        $selectedMonth = now()->format('Y-m');
        $canExportReport = in_array(Auth::user()->role->role_name ?? '', ['admin', 'cashier'], true);
        $activeCount = Order::query()->notServed()->count();
        $servedCount = Order::query()->served()->count();

        return view('admin.order.index', compact(
            'orders',
            'kitchenStatuses',
            'reportMonths',
            'selectedMonth',
            'canExportReport',
            'filter',
            'activeCount',
            'servedCount'
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

    public function show($id)
    {
        $order = Order::with(['user', 'orderItems.item'])->findOrFail($id);
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

        $order->status = 'settlement';
        if ($order->kitchen_status === Order::KITCHEN_WAITING || $order->kitchen_status === null) {
            $order->kitchen_status = Order::KITCHEN_PROCESSING;
        }
        $order->save();

        return redirect()->route('orders.index')->with('success', 'Pembayaran diterima. Pesanan masuk ke proses.');
    }

    public function updateKitchenStatus(Request $request, $id)
    {
        $role = Auth::user()->role->role_name ?? null;
        if (! in_array($role, ['admin', 'cashier', 'chef'], true)) {
            abort(403);
        }

        $validated = $request->validate([
            'kitchen_status' => ['required', Rule::in(array_keys(Order::kitchenStatusOptions()))],
        ]);

        $order = Order::findOrFail($id);

        if (! $order->isPaid()) {
            return redirect()->back()->with('error', 'Konfirmasi pembayaran terlebih dahulu sebelum mengubah status dapur.');
        }

        if ($order->isServed()) {
            return redirect()->back()->with('error', 'Pesanan yang sudah selesai tidak dapat diubah lagi.');
        }

        $order->kitchen_status = $validated['kitchen_status'];
        if ($order->status === 'cooked') {
            $order->status = 'settlement';
        }
        $order->save();

        $message = 'Status pesanan diperbarui menjadi '.$order->kitchenStatusLabel().'.';

        if ($order->isServed()) {
            $message = 'Pesanan ditandai selesai dan dipindahkan ke daftar sudah dilayani.';
            $fromShow = str_contains((string) url()->previous(), '/orders/'.$order->id);

            if (! $fromShow) {
                return redirect()
                    ->route('orders.index', ['filter' => Order::LIST_FILTER_SERVED])
                    ->with('success', $message);
            }
        }

        return redirect()->back()->with('success', $message);
    }
}
