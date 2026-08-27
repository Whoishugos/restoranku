<?php
namespace App\Services;
use Midtrans\Config;
use Midtrans\Notification;
use Midtrans\Snap;
use Midtrans\Transaction;
class MidtransService
{
    public function __construct()
    {
        Config::$serverKey = config('midtrans.server_key');
        Config::$isProduction = (bool) config('midtrans.is_production');
        Config::$isSanitized = true;
        Config::$is3ds = true;
    }
    public function isConfigured(): bool
    {
        return filled(config('midtrans.server_key')) && filled(config('midtrans.client_key'));
    }
    public function getSnapToken(array $params): string
    {
        return Snap::getSnapToken($params);
    }
    public function notification(): Notification
    {
        return new Notification();
    }
    public function transactionStatus(string $orderCode): object
    {
        return Transaction::status($orderCode);
    }
}