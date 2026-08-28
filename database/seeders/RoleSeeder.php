<?php

namespace Database\Seeders;

use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class RoleSeeder extends Seeder
{
    public function run(): void
    {
        $now = now();
        $roles = [
            ['role_name' => 'admin', 'description' => 'Administrator', 'created_at' => $now, 'updated_at' => $now],
            ['role_name' => 'cashier', 'description' => 'Kasir', 'created_at' => $now, 'updated_at' => $now],
            ['role_name' => 'chef', 'description' => 'Koki', 'created_at' => $now, 'updated_at' => $now],
            ['role_name' => 'customer', 'description' => 'Pelanggan', 'created_at' => $now, 'updated_at' => $now],
        ];

        foreach ($roles as $role) {
            DB::table('roles')->updateOrInsert(
                ['role_name' => $role['role_name']],
                $role
            );
        }

    }
}