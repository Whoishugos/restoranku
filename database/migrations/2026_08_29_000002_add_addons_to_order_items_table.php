<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        if (! Schema::hasTable('order_items') || Schema::hasColumn('order_items', 'addons')) {
            return;
        }

        Schema::table('order_items', function (Blueprint $table) {
            $table->json('addons')->nullable();
        });
    }

    public function down(): void
    {
        if (Schema::hasTable('order_items') && Schema::hasColumn('order_items', 'addons')) {
            Schema::table('order_items', function (Blueprint $table) {
                $table->dropColumn('addons');
            });
        }
    }
};
