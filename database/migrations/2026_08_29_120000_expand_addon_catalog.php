<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        if (! Schema::hasTable('addon_groups')) {
            Schema::create('addon_groups', function (Blueprint $table) {
                $table->id();
                $table->string('name');
                $table->string('type');
                $table->foreignId('category_id')->constrained('categories');
                $table->unsignedTinyInteger('min_select')->default(0);
                $table->unsignedTinyInteger('max_select')->default(1);
                $table->boolean('is_active')->default(true);
                $table->timestamps();
            });
        }

        if (! Schema::hasTable('addon_group_item')) {
            Schema::create('addon_group_item', function (Blueprint $table) {
                $table->id();
                $table->foreignId('addon_group_id')->constrained('addon_groups')->cascadeOnDelete();
                $table->foreignId('item_id')->constrained('items')->cascadeOnDelete();
                $table->unique(['addon_group_id', 'item_id']);
            });
        }

        if (Schema::hasTable('addons')) {
            Schema::table('addons', function (Blueprint $table) {
                if (! Schema::hasColumn('addons', 'addon_group_id')) {
                    $table->foreignId('addon_group_id')->nullable()->constrained('addon_groups')->nullOnDelete();
                }
                if (! Schema::hasColumn('addons', 'img')) {
                    $table->string('img')->nullable();
                }
                if (! Schema::hasColumn('addons', 'stock')) {
                    $table->unsignedInteger('stock')->default(100);
                }
            });
        }

        if (Schema::hasTable('items') && ! Schema::hasColumn('items', 'stock')) {
            Schema::table('items', function (Blueprint $table) {
                $table->unsignedInteger('stock')->default(100);
            });
        }
    }

    public function down(): void
    {
        if (Schema::hasTable('addons') && Schema::hasColumn('addons', 'addon_group_id')) {
            Schema::table('addons', function (Blueprint $table) {
                $table->dropConstrainedForeignId('addon_group_id');
            });
        }

        Schema::dropIfExists('addon_group_item');
        Schema::dropIfExists('addon_groups');
    }
};
