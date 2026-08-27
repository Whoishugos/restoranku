<?php

namespace Database\Seeders;

// use Illuminate\Database\Console\Seeds\WithoutModelEvents;
// use Illuminate\Database\Seeder;
use App\Models\Role;
use App\Models\User;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Hash;

class UserSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        // Create 10 users
        $adminRoleId = Role::where('role_name', 'admin')->value('id') ?? 1;
        $cashierRoleId = Role::where('role_name', 'cashier')->value('id') ?? 2;
        $chefRoleId = Role::where('role_name', 'chef')->value('id') ?? 3;
        User::updateOrCreate(
            ['email' => 'admin@restoranku.com'],
            [
                'username' => 'admin',
                'fullname' => 'Administrator',
                'phone' => '080000000001',
                'password' => Hash::make('password'),
                'role_id' => $adminRoleId,
            ]
        );
        User::updateOrCreate(
            ['email' => 'kasir@restoranku.com'],
            [
                'username' => 'kasir',
                'fullname' => 'Kasir',
                'phone' => '080000000002',
                'password' => Hash::make('password'),
                'role_id' => $cashierRoleId,
            ]
        );
        User::updateOrCreate(
            ['email' => 'koki@restoranku.com'],
            [
                'username' => 'koki',
                'fullname' => 'Koki',
                'phone' => '080000000003',
                'password' => Hash::make('password'),
                'role_id' => $chefRoleId,
            ]
        );
    }
}
