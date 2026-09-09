<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        if (! Schema::hasTable('orders') || Schema::hasColumn('orders', 'paid_at')) {
            return;
        }

        Schema::table('orders', function (Blueprint $table) {
            $table->timestamp('paid_at')->nullable()->after('payment_method');
        });

        DB::table('orders')
            ->whereIn('status', ['settlement', 'cooked'])
            ->whereNull('paid_at')
            ->update(['paid_at' => DB::raw('updated_at')]);
    }

    public function down(): void
    {
        if (Schema::hasTable('orders') && Schema::hasColumn('orders', 'paid_at')) {
            Schema::table('orders', function (Blueprint $table) {
                $table->dropColumn('paid_at');
            });
        }
    }
};
