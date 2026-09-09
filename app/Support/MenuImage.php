<?php

namespace App\Support;

class MenuImage
{
    public static function url(?string $img): string
    {
        $img = trim((string) $img);
        if ($img === '') {
            return asset('img_item_upload/default.jpg');
        }

        if (str_starts_with($img, 'http://') || str_starts_with($img, 'https://')) {
            return $img;
        }

        $relative = 'img_item_upload/'.$img;
        if (is_file(public_path($relative))) {
            return asset($relative);
        }

        return asset('img_item_upload/default.jpg');
    }
}
