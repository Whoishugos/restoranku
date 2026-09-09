<!DOCTYPE html>
<html lang="id">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>@yield('title', 'Dashboard') — {{ config('app.name') }}</title>
    <link rel="icon" href="{{ asset('icons/icon-192.png') }}" type="image/png">

    <link rel="stylesheet" crossorigin href="{{ asset('assets/admin/compiled/css/app.css') }}">
    <link rel="stylesheet" crossorigin href="{{ asset('assets/admin/compiled/css/app-dark.css') }}">
    <link rel="stylesheet" crossorigin href="{{ asset('assets/admin/compiled/css/iconly.css') }}">
    <link rel="stylesheet" href="{{ asset('assets/admin/css/mobile.css') }}">

    @yield('css')
</head>
