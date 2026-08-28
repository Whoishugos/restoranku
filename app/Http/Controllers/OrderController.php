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

        if (in_array($order->kitchen_status, ['cooking', 'ready'], true) || $order->status === 'cooked') {
            return response('OK', 200);
        }

        $transaction = $notif->transaction_status;
        $fraud = $notif->fraud_status ?? null;
        $type = $notif->payment_type ?? null;

        if ($transaction === 'capture') {
            if ($type === 'credit_card' && $fraud === 'challenge') {
                $order->status = 'pending';
            } else {
                $order->status = 'settlement';
            }
        } elseif ($transaction === 'settlement') {
            $order->status = 'settlement';
        } elseif ($transaction === 'pending') {
            $order->status = 'pending';
        } elseif (in_array($transaction, ['deny', 'expire', 'cancel'], true)) {
            $order->status = 'pending';
        }

        if ($order->status === 'settlement' && ($order->kitchen_status === 'waiting' || $order->kitchen_status === null)) {
            $order->kitchen_status = 'processing';
        }

        $order->save();

        return response('OK', 200);
    }
}
