<?php

namespace App\Providers;

use Illuminate\Support\Facades\Session;
use Illuminate\Support\Facades\URL;
use Illuminate\Support\Facades\View;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    public function register(): void
    {
        $this->app['config']->set('cache.default', 'file');
        $this->app['config']->set('session.driver', 'file');
        $this->app['config']->set('queue.default', 'sync');
    }

    public function boot(): void
    {
        if (str_starts_with((string) config('app.url'), 'https://')) {
            URL::forceScheme('https');
        }

        View::composer('customer.*', function ($view) {
            $cart = Session::get('cart', []);
            $view->with([
                'tableNumber' => Session::get('tableNumber'),
                'cartCount' => collect($cart)->sum(fn ($line) => (int) ($line['qty'] ?? 0)),
            ]);
        });
    }
}
