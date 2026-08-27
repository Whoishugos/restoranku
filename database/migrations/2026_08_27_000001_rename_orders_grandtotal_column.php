<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;
return new class extends Migration
{
    public function up(): void
    {
        if (Schema::hasTable('orders') && Schema::hasColumn('orders', 'grandtotal') && ! Schema::hasColumn('orders', 'grand_total')) {
            Schema::table('orders', function (Blueprint $table) {
                $table->renameColumn('grandtotal', 'grand_total');
            });
        }
    }
    public function down(): void
    {
        if (Schema::hasTable('orders') && Schema::hasColumn('orders', 'grand_total') && ! Schema::hasColumn('orders', 'grandtotal')) {
            Schema::table('orders', function (Blueprint $table) {
                $table->renameColumn('grand_total', 'grandtotal');
            });
        }
    }
};