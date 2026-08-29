<?php

namespace App\Http\Controllers;

use App\Models\Addon;
use App\Models\Item;
use App\Models\Order;
use App\Models\OrderItem;
use App\Models\Role;
use App\Models\User;
use App\Services\AddonCatalog;
use App\Services\MidtransService;
use App\Support\CartLine;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Session;
use Illuminate\Support\Facades\Validator;
use Illuminate\Support\Str;

class MenuController extends Controller
{
    private const MAX_TABLE = 99;

    public function index(Request $request)
    {
        $this->captureTableNumber($request->query('meja'));

        $items = Item::with('category')->available()->orderBy('name', 'asc')->get();
        $foods = $items->filter(fn (Item $item) => strcasecmp((string) $item->category?->cat_name, 'Makanan') === 0)->values();
        $drinks = $items->filter(fn (Item $item) => strcasecmp((string) $item->category?->cat_name, 'Minuman') === 0)->values();
        $tableNumber = Session::get('tableNumber');

        return view('customer.menu', compact('foods', 'drinks', 'tableNumber'));
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
        $cart = Session::get('cart', []);
        $tableNumber = Session::get('tableNumber');

        return view('customer.cart', compact('cart', 'tableNumber'));
    }

    public function customize(Item $item, AddonCatalog $catalog)
    {
        if (! $item->isAvailable()) {
            return response()->json(['status' => 'error', 'message' => 'Menu sedang habis.'], 422);
        }

        return response()->json([
            'status' => 'success',
            'data' => $catalog->payloadForItem($item),
        ]);
    }

    public function addToCart(Request $request, AddonCatalog $catalog)
    {
        $menuId = $request->input('id');
        $menu = Item::with('category')->find($menuId);

        if (! $menu || ! $menu->isAvailable()) {
            return response()->json([
                'status' => 'error',
                'message' => 'Menu tidak tersedia atau stok habis.',
            ], 422);
        }

        try {
            $addons = $catalog->validateAndSnapshot($menu, $request->input('addon_ids', []));
        } catch (\Illuminate\Validation\ValidationException $e) {
            return response()->json([
                'status' => 'error',
                'message' => $e->validator->errors()->first(),
            ], 422);
        }

        $addonIds = collect($addons)->pluck('id')->sort()->values()->all();
        $lineKey = $menu->id.':'.md5(json_encode($addonIds));
        $cart = Session::get('cart', []);

        if (isset($cart[$lineKey])) {
            $cart[$lineKey]['qty'] += 1;
        } else {
            $cart[$lineKey] = [
                'key' => $lineKey,
                'id' => $menu->id,
                'name' => $menu->name,
                'price' => (int) $menu->price,
                'image' => $menu->img,
                'category' => $menu->category?->cat_name,
                'qty' => 1,
                'addons' => $addons,
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
        $newQty = (int) $request->input('qty');
        $cart = Session::get('cart', []);

        if (! isset($cart[$itemId])) {
            return response()->json(['success' => false, 'message' => 'Item tidak ditemukan']);
        }

        if ($newQty <= 0) {
            unset($cart[$itemId]);
            Session::put('cart', $cart);

            return response()->json([
                'success' => true,
                'removed' => true,
                'empty' => $cart === [],
            ]);
        }

        $cart[$itemId]['qty'] = $newQty;
        Session::put('cart', $cart);

        return response()->json([
            'success' => true,
            'removed' => false,
            'qty' => $newQty,
        ]);
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

    public function updateAddons(Request $request)
    {
        $itemId = $request->input('id');
        $addonIds = collect($request->input('addon_ids', []))
            ->map(fn ($id) => (int) $id)
            ->filter()
            ->unique()
            ->values();

        $cart = Session::get('cart', []);

        if (! isset($cart[$itemId])) {
            return response()->json(['success' => false, 'message' => 'Item tidak ditemukan']);
        }

        if (! CartLine::isFood($cart[$itemId])) {
            return response()->json(['success' => false, 'message' => 'Add-ons hanya untuk makanan']);
        }

        $addons = Addon::where('is_active', 1)->whereIn('id', $addonIds)->get();

        $cart[$itemId]['addons'] = $addons->map(fn (Addon $addon) => [
            'id' => $addon->id,
            'name' => $addon->name,
            'price' => (int) $addon->price,
        ])->values()->all();

        Session::put('cart', $cart);

        return response()->json(['success' => true]);
    }

    public function clearCart()
    {
        Session::forget('cart');

        return redirect()->route('cart')->with('success', 'Keranjang berhasil dikosongkan');
    }

    public function checkout(MidtransService $midtrans)
    {
        $cart = Session::get('cart');
        if (empty($cart)) {
            return redirect()->route('cart')->with('error', 'Keranjang masih kosong');
        }

        return view('customer.checkout', [
            'cart' => $cart,
            'tableNumber' => Session::get('tableNumber'),
            'midtransConfigured' => $midtrans->isConfigured(),
        ]);
    }

    public function storeOrder(Request $request, MidtransService $midtrans)
    {
        $cart = Session::get('cart');
        $wantsJson = $request->ajax() || $request->expectsJson() || $request->payment_method === 'qris';

        if (empty($cart)) {
            if ($wantsJson) {
                return response()->json(['status' => 'error', 'message' => 'Keranjang masih kosong'], 422);
            }

            return redirect()->route('cart')->with('error', 'Keranjang masih kosong');
        }

        $tableNumber = $this->resolveTableNumber($request->input('table_number'));
        if (! $tableNumber) {
            if ($wantsJson) {
                return response()->json(['status' => 'error', 'message' => 'Isi nomor meja terlebih dahulu.'], 422);
            }

            return redirect()->route('checkout')->with('error', 'Isi nomor meja terlebih dahulu.');
        }

        $validator = Validator::make($request->all(), [
            'fullname' => 'required|string|max:255',
            'phone' => 'required|string|max:15',
            'table_number' => 'nullable|integer|min:1|max:99',
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
            $unitPrice = CartLine::unitPrice($item);
            $lineTotal = CartLine::lineTotal($item);
            $totalAmount += $lineTotal;
            $addonLabel = CartLine::addonNames($item);
            $itemName = $item['name'].($addonLabel !== '' ? ' + '.$addonLabel : '');
            $itemDetails[] = [
                'id' => (string) $item['id'],
                'price' => $unitPrice,
                'quantity' => (int) $item['qty'],
                'name' => substr($itemName, 0, 50),
            ];
        }

        $tax = (int) round(0.1 * $totalAmount);
        $grandTotal = $totalAmount + $tax;

        foreach ($cart as $item) {
            $menu = Item::find($item['id']);
            $qty = (int) $item['qty'];
            if (! $menu || $menu->stock < $qty) {
                $message = 'Stok habis untuk '.($item['name'] ?? 'menu').'. Menu disembunyikan jika gudang kosong.';
                if ($wantsJson) {
                    return response()->json(['status' => 'error', 'message' => $message], 422);
                }

                return redirect()->route('cart')->with('error', $message);
            }
        }

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
            'order_code' => 'ORD-'.$tableNumber.'-'.now()->format('YmdHis').strtoupper(Str::random(4)),
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
            $lineTotal = CartLine::lineTotal($item);
            $taxLine = (int) round(0.1 * $lineTotal);
            $qty = (int) $item['qty'];
            $menu = Item::find($item['id']);
            if ($menu) {
                $menu->decrement('stock', $qty);
            }

            foreach ($item['addons'] ?? [] as $addonData) {
                $addon = Addon::find($addonData['id'] ?? 0);
                if ($addon && $addon->stock > 0) {
                    $addon->decrement('stock', min($addon->stock, $qty));
                }
            }

            OrderItem::create([
                'order_id' => $order->id,
                'item_id' => $item['id'],
                'quantity' => $qty,
                'price' => $lineTotal,
                'tax' => $taxLine,
                'total_price' => $lineTotal + $taxLine,
                'addons' => array_values($item['addons'] ?? []),
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
            'enabled_payments' => ['gopay', 'other_qris', 'shopeepay', 'bank_transfer'],
            'callbacks' => [
                'finish' => route('checkout.success', $order->order_code),
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

    private function resolveTableNumber(mixed $tableNumber): ?int
    {
        if ($this->storeTableNumber($tableNumber)) {
            return (int) Session::get('tableNumber');
        }

        $existing = Session::get('tableNumber');

        return $existing ? (int) $existing : null;
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
