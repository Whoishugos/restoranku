<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        if (! Schema::hasTable('orders') || Schema::hasColumn('orders', 'kitchen_status')) {
            return;
        }

        Schema::table('orders', function (Blueprint $table) {
            $table->string('kitchen_status', 32)->default('waiting')->after('status');
        });

        DB::table('orders')->where('status', 'cooked')->update([
            'kitchen_status' => 'ready',
        ]);

        DB::table('orders')->where('status', 'settlement')->where('kitchen_status', 'waiting')->update([
            'kitchen_status' => 'processing',
        ]);
    }

    public function down(): void
    {
        if (Schema::hasTable('orders') && Schema::hasColumn('orders', 'kitchen_status')) {
            Schema::table('orders', function (Blueprint $table) {
                $table->dropColumn('kitchen_status');
            });
        }
    }
};
