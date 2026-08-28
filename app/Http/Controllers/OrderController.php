<?php

namespace App\Http\Controllers;

use App\Models\Order;
use App\Models\OrderItem;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class OrderController extends Controller
{
    public function index()
    {
        $orders = Order::with('user')->latest()->get();
        $kitchenStatuses = Order::kitchenStatusOptions();

        return view('admin.order.index', compact('orders', 'kitchenStatuses'));
    }

    public function show($id)
    {
        $order = Order::with(['user', 'orderItems.item'])->findOrFail($id);
        $orderItems = $order->orderItems;
        $kitchenStatuses = Order::kitchenStatusOptions();

        return view('admin.order.show', compact('order', 'orderItems', 'kitchenStatuses'));
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
}
