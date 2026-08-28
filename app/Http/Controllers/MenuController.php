<?php

namespace App\Http\Controllers;

use App\Models\Item;
use App\Models\Order;
use App\Models\OrderItem;
use App\Models\Role;
use App\Models\User;
use App\Services\MidtransService;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Session;
use Illuminate\Support\Facades\Validator;

class MenuController extends Controller
{
    private const MAX_TABLE = 99;

    public function index(Request $request)
    {
        $this->captureTableNumber($request->query('meja'));

        $items = Item::where('is_active', 1)->orderBy('name', 'asc')->get();
        $tableNumber = Session::get('tableNumber');

        return view('customer.menu', compact('items', 'tableNumber'));
    }

    public function scanTable(int $tableNumber)
    {
        if (! $this->storeTableNumber($tableNumber)) {
            return redirect()->route('menu')->with('error', 'Nomor meja tidak valid.');
        }

        return redirect()->route('menu');
    }

    public function cart()
    {
        $cart = Session::get('cart');
        $tableNumber = Session::get('tableNumber');

        return view('customer.cart', compact('cart', 'tableNumber'));
    }

    public function addToCart(Request $request)
    {
        $menuId = $request->input('id');
        $menu = Item::find($menuId);

        if (! $menu) {
            return response()->json([
                'status' => 'error',
                'message' => 'Menu tidak ditemukan',
            ]);
        }

        $cart = Session::get('cart', []);

        if (isset($cart[$menuId])) {
            $cart[$menuId]['qty'] += 1;
        } else {
            $cart[$menuId] = [
                'id' => $menu->id,
                'name' => $menu->name,
                'price' => $menu->price,
                'image' => $menu->img,
                'qty' => 1,
            ];
        }

        Session::put('cart', $cart);

        return response()->json([
            'status' => 'success',
            'message' => 'Berhasil ditambahkan ke keranjang',
            'cart' => $cart,
        ]);
    }

    public function updateCart(Request $request)
    {
        $itemId = $request->input('id');
        $newQty = $request->input('qty');

        if ($newQty <= 0) {
            return response()->json(['success' => false]);
        }

        $cart = Session::get('cart', []);
        if (isset($cart[$itemId])) {
            $cart[$itemId]['qty'] = $newQty;
            Session::put('cart', $cart);
            Session::flash('success', 'Jumlah item berhasil diperbarui');

            return response()->json(['success' => true]);
        }

        return response()->json(['success' => false]);
    }

    public function removeCart(Request $request)
    {
        $itemId = $request->input('id');
        $cart = Session::get('cart', []);

        if (isset($cart[$itemId])) {
            unset($cart[$itemId]);
            Session::put('cart', $cart);
            Session::flash('success', 'Item berhasil dihapus dari keranjang');

            return response()->json(['success' => true]);
        }

        return response()->json(['success' => false]);
    }

    public function clearCart()
    {
        Session::forget('cart');

        return redirect()->route('cart')->with('success', 'Keranjang berhasil dikosongkan');
    }

    public function checkout()
    {
        $cart = Session::get('cart');
        if (empty($cart)) {
            return redirect()->route('cart')->with('error', 'Keranjang masih kosong');
        }

        $tableNumber = Session::get('tableNumber');
        if (! $tableNumber) {
            return redirect()->route('menu')->with('error', 'Scan QR meja terlebih dahulu agar nomor meja terisi otomatis.');
        }

        return view('customer.checkout', compact('cart', 'tableNumber'));
    }

    public function storeOrder(Request $request, MidtransService $midtrans)
    {
        $cart = Session::get('cart');
        $tableNumber = Session::get('tableNumber');
        $wantsJson = $request->ajax() || $request->expectsJson() || $request->payment_method === 'qris';

        if (empty($cart)) {
            if ($wantsJson) {
                return response()->json(['status' => 'error', 'message' => 'Keranjang masih kosong'], 422);
            }

            return redirect()->route('cart')->with('error', 'Keranjang masih kosong');
        }

        if (! $tableNumber) {
            if ($wantsJson) {
                return response()->json(['status' => 'error', 'message' => 'Nomor meja belum terdeteksi. Scan QR meja terlebih dahulu.'], 422);
            }

            return redirect()->route('menu')->with('error', 'Scan QR meja terlebih dahulu agar nomor meja terisi otomatis.');
        }

        $validator = Validator::make($request->all(), [
            'fullname' => 'required|string|max:255',
            'phone' => 'required|string|max:15',
            'payment_method' => 'required|in:tunai,qris',
            'note' => 'nullable|string|max:1000',
        ]);

        if ($validator->fails()) {
            if ($wantsJson) {
                return response()->json([
                    'status' => 'error',
                    'message' => $validator->errors()->first(),
                ], 422);
            }

            return redirect()->route('checkout')->withErrors($validator);
        }

        $totalAmount = 0;
        $itemDetails = [];
        foreach ($cart as $item) {
            $totalAmount += $item['qty'] * $item['price'];
            $itemDetails[] = [
                'id' => (string) $item['id'],
                'price' => (int) $item['price'],
                'quantity' => (int) $item['qty'],
                'name' => substr($item['name'], 0, 50),
            ];
        }

        $tax = (int) round(0.1 * $totalAmount);
        $grandTotal = $totalAmount + $tax;

        $itemDetails[] = [
            'id' => 'TAX',
            'price' => $tax,
            'quantity' => 1,
            'name' => 'Pajak 10%',
        ];

        $customerRoleId = Role::where('role_name', 'customer')->value('id') ?? 4;

        $user = User::firstOrCreate(
            [
                'phone' => $request->input('phone'),
                'role_id' => $customerRoleId,
            ],
            [
                'fullname' => $request->input('fullname'),
                'username' => null,
                'email' => null,
                'password' => null,
            ]
        );

        if ($user->fullname !== $request->input('fullname')) {
            $user->update(['fullname' => $request->input('fullname')]);
        }

        $order = Order::create([
            'order_code' => 'ORD-'.$tableNumber.'-'.time(),
            'user_id' => $user->id,
            'subtotal' => $totalAmount,
            'tax' => $tax,
            'grand_total' => $grandTotal,
            'status' => 'pending',
            'kitchen_status' => Order::KITCHEN_WAITING,
            'table_number' => $tableNumber,
            'payment_method' => $request->payment_method,
            'note' => $request->note,
        ]);

        $this->rememberCustomerOrder($order->order_code);

        foreach ($cart as $item) {
            OrderItem::create([
                'order_id' => $order->id,
                'item_id' => $item['id'],
                'quantity' => $item['qty'],
                'price' => $item['price'] * $item['qty'],
                'tax' => (int) round(0.1 * $item['price'] * $item['qty']),
                'total_price' => ($item['price'] * $item['qty']) + (int) round(0.1 * $item['price'] * $item['qty']),
            ]);
        }

        Session::forget('cart');

        if ($request->payment_method === 'tunai') {
            return redirect()->route('checkout.success', ['orderId' => $order->order_code])->with('success', 'Pesanan berhasil dibuat');
        }

        if (! $midtrans->isConfigured()) {
            return response()->json([
                'status' => 'error',
                'message' => 'Pembayaran QRIS belum dikonfigurasi. Isi kunci Midtrans di file .env.',
            ], 500);
        }

        $params = [
            'transaction_details' => [
                'order_id' => $order->order_code,
                'gross_amount' => (int) $order->grand_total,
            ],
            'item_details' => $itemDetails,
            'customer_details' => [
                'first_name' => $user->fullname ?? 'Guest',
                'phone' => $user->phone,
            ],
        ];

        try {
            $snapToken = $midtrans->getSnapToken($params);

            return response()->json([
                'status' => 'success',
                'snap_token' => $snapToken,
                'order_code' => $order->order_code,
            ]);
        } catch (\Exception $e) {
            return response()->json([
                'status' => 'error',
                'message' => 'Gagal membuat pembayaran Midtrans. Periksa Server Key dan coba lagi.',
            ], 500);
        }
    }

    public function checkoutSuccess($orderId, MidtransService $midtrans)
    {
        $order = Order::where('order_code', $orderId)->first();

        if (! $order) {
            return redirect()->route('menu')->with('error', 'Pesanan tidak ditemukan');
        }

        $this->rememberCustomerOrder($order->order_code);
        $orderItems = OrderItem::where('order_id', $order->id)->get();

        if ($order->payment_method === 'qris' && $order->status === 'pending' && $midtrans->isConfigured()) {
            try {
                $status = $midtrans->transactionStatus($order->order_code);
                $transactionStatus = is_object($status) ? ($status->transaction_status ?? null) : null;
                if (in_array($transactionStatus, ['settlement', 'capture'], true)) {
                    $order->status = 'settlement';
                    if ($order->kitchen_status === Order::KITCHEN_WAITING || $order->kitchen_status === null) {
                        $order->kitchen_status = Order::KITCHEN_PROCESSING;
                    }
                    $order->save();
                }
            } catch (\Exception $e) {
                // Biarkan status pending; webhook Midtrans akan memperbarui.
            }
        }

        return view('customer.success', compact('order', 'orderItems'));
    }

    private function captureTableNumber(mixed $tableNumber): void
    {
        if ($tableNumber === null || $tableNumber === '') {
            return;
        }

        $this->storeTableNumber($tableNumber);
    }

    private function storeTableNumber(mixed $tableNumber): bool
    {
        $number = (int) $tableNumber;
        if ($number < 1 || $number > self::MAX_TABLE) {
            return false;
        }

        Session::put('tableNumber', $number);

        return true;
    }

    public function trackOrders(Request $request)
    {
        if ($request->filled('kode')) {
            return redirect()->route('customer.orders.show', $request->string('kode')->trim());
        }
        $codes = Session::get('customer_order_codes', []);
        $orders = empty($codes)
            ? collect()
            : Order::with('orderItems.item')
                ->whereIn('order_code', $codes)
                ->latest()
                ->get();

        return view('customer.orders', compact('orders'));
    }

    public function trackOrder(string $orderCode)
    {
        $order = Order::with('orderItems.item')->where('order_code', $orderCode)->first();

        if (! $order) {
            return redirect()->route('customer.orders')->with('error', 'Pesanan tidak ditemukan');
        }

        $this->rememberCustomerOrder($order->order_code);
        $orderItems = $order->orderItems;

        return view('customer.track', compact('order', 'orderItems'));
    }

    public function trackOrderStatus(string $orderCode)
    {
        $order = Order::where('order_code', $orderCode)->first();

        if (! $order) {
            return response()->json(['status' => 'error', 'message' => 'Pesanan tidak ditemukan'], 404);
        }

        return response()->json([
            'status' => 'success',
            'paid' => $order->isPaid(),
            'kitchen_status' => $order->kitchenStatus(),
            'kitchen_label' => $order->kitchenStatusLabel(),
            'payment_label' => $order->paymentStatusLabel(),
            'progress_step' => $order->progressStep(),
        ]);
    }

    private function rememberCustomerOrder(string $orderCode): void
    {
        $codes = Session::get('customer_order_codes', []);
        if (! in_array($orderCode, $codes, true)) {
            $codes[] = $orderCode;
            Session::put('customer_order_codes', $codes);
        }
    }
}
