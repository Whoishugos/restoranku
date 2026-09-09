<?php

namespace App\Http\Controllers;

use App\Models\Order;
use App\Services\MidtransService;
use Illuminate\Http\Request;
use Illuminate\Http\Response;

class MidtransController extends Controller
{
    public function notification(Request $request, MidtransService $midtrans): Response
    {
        if (! $midtrans->isConfigured()) {
            return response('Midtrans is not configured', 503);
        }

        $notif = $midtrans->notification();
        $order = Order::where('order_code', $notif->order_id)->first();

        if (! $order) {
            return response('Order not found', 404);
        }

        $order->applyGatewayTransaction(
            (string) ($notif->transaction_status ?? ''),
            $notif->fraud_status ?? null,
            $notif->payment_type ?? null,
            $notif->transaction_time ?? null,
        );

        return response('OK', 200);
    }
}
