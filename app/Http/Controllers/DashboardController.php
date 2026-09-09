<?php

namespace App\Http\Controllers;

use App\Models\Order;
use Illuminate\Http\Request;

class DashboardController extends Controller
{
    private const FEED_LIMIT = 8;

    public function index()
    {
        $totalOrders = Order::count();
        $totalRevenue = Order::sum('grand_total');

        $todayOrders = Order::whereDate('created_at', now())->count();
        $todayRevenue = Order::whereDate('created_at', now())->sum('grand_total');

        $latestOrders = Order::with('user')->latest()->limit(self::FEED_LIMIT)->get();
        $oldestOrders = Order::with('user')->notServed()->oldest()->limit(self::FEED_LIMIT)->get();
        $paidOrders = Order::with('user')->paid()->latest()->limit(self::FEED_LIMIT)->get();
        $newOrdersCount = Order::query()->notServed()->count();
        $latestOrderId = (int) Order::query()->max('id');

        return view('admin.dashboard', compact(
            'totalOrders',
            'totalRevenue',
            'todayOrders',
            'todayRevenue',
            'latestOrders',
            'oldestOrders',
            'paidOrders',
            'newOrdersCount',
            'latestOrderId'
        ));
    }

    public function notifications(Request $request)
    {
        $sinceId = max(0, $request->integer('since_id'));

        $latestId = (int) Order::query()->max('id');

        $newOrders = Order::with('user')
            ->newerThan($sinceId)
            ->latest('id')
            ->limit(20)
            ->get();

        $recentOrders = Order::with('user')
            ->latest('id')
            ->limit(self::FEED_LIMIT)
            ->get();

        return response()->json([
            'latest_id' => $latestId,
            'new_count' => $newOrders->count(),
            'pending_count' => Order::query()->notServed()->count(),
            'new_orders' => $newOrders->map->toFeedArray()->values(),
            'recent_orders' => $recentOrders->map->toFeedArray()->values(),
        ]);
    }
}
