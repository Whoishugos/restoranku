<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Symfony\Component\HttpFoundation\Response;

class RoleMiddleware
{
    /**
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next, string ...$roles): Response
    {
        if (Auth::guest()) {
            return redirect()->route('login');
        }

        $allowed = [];
        foreach ($roles as $role) {
            foreach (explode('|', $role) as $name) {
                $name = trim($name);
                if ($name !== '') {
                    $allowed[] = $name;
                }
            }
        }

        $roleName = Auth::user()->role?->role_name;
        if ($roleName === null || ! in_array($roleName, $allowed, true)) {
            abort(403);
        }

        return $next($request);
    }
}
