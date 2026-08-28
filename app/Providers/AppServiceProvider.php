<?php

namespace App\Providers;

use Illuminate\Support\Facades\Session;
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
        View::composer('customer.*', function ($view) {
            $view->with('tableNumber', Session::get('tableNumber'));
        });
    }
}
