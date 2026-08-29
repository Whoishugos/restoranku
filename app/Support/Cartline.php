<?php

namespace App\Support;

class CartLine
{
    public static function isFood(array $item): bool
    {
        return strcasecmp((string) ($item['category'] ?? ''), 'Makanan') === 0;
    }

    public static function addonTotal(array $item): int
    {
        $total = 0;
        foreach ($item['addons'] ?? [] as $addon) {
            $total += (int) ($addon['price'] ?? 0);
        }

        return $total;
    }

    public static function unitPrice(array $item): int
    {
        return (int) ($item['price'] ?? 0) + self::addonTotal($item);
    }

    public static function lineTotal(array $item): int
    {
        return self::unitPrice($item) * (int) ($item['qty'] ?? 0);
    }

    public static function addonNames(array $item): string
    {
        $names = [];
        foreach ($item['addons'] ?? [] as $addon) {
            if (! empty($addon['name'])) {
                $names[] = $addon['name'];
            }
        }

        return implode(', ', $names);
    }

    public static function hasAddon(array $item, int $addonId): bool
    {
        foreach ($item['addons'] ?? [] as $addon) {
            if ((int) ($addon['id'] ?? 0) === $addonId) {
                return true;
            }
        }

        return false;
    }
}
