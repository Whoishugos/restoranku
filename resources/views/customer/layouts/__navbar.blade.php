<div class="container-fluid fixed-top customer-topbar">
    <div class="container px-0">
        <nav class="navbar navbar-light bg-white navbar-expand-xl">
            <a href="{{ route('menu') }}" class="navbar-brand brand-lockup d-flex align-items-center gap-2 me-2 py-0">
                <img src="{{ asset('img/logo-kekupu.png') }}" alt="Logo {{ config('app.name') }}" class="brand-logo">
                <span class="brand-title">
                    <span class="d-block">RESTORAN KEKUPU</span>
                    <span class="d-block brand-subtitle">VILLA JEMBRANA</span>
                </span>
            </a>
            @if (! empty($tableNumber))
                <span class="badge rounded-pill bg-secondary text-dark table-chip">Meja {{ $tableNumber }}</span>
            @endif
            <a href="{{ route('cart') }}" class="position-relative cart-icon-link d-xl-none ms-auto me-2 my-auto" aria-label="Keranjang">
                <i class="fa fa-shopping-bag fa-lg"></i>
                <span class="cart-badge" data-cart-count {{ ($cartCount ?? 0) === 0 ? 'hidden' : '' }}>{{ $cartCount ?? 0 }}</span>
            </a>
            <button class="navbar-toggler py-2 px-3 d-none" type="button" data-bs-toggle="collapse" data-bs-target="#navbarCollapse" aria-label="Menu">
                <span class="fa fa-bars text-primary"></span>
            </button>
            <div class="collapse navbar-collapse bg-white" id="navbarCollapse">
                <div class="navbar-nav navbar-center-links">
                    <a href="{{ route('menu') }}" class="nav-item nav-link {{ request()->routeIs('menu') ? 'active' : '' }}">Menu</a>
                    <a href="{{ route('customer.orders') }}" class="nav-item nav-link {{ request()->routeIs('customer.orders*') ? 'active' : '' }}">Pesanan Saya</a>
                </div>
                <div class="d-none d-xl-flex m-3 me-0 ms-xl-auto">
                    <a href="{{ route('cart') }}" class="position-relative me-4 my-auto cart-icon-link" aria-label="Keranjang">
                        <i class="fa fa-shopping-bag fa-2x"></i>
                        <span class="cart-badge" data-cart-count {{ ($cartCount ?? 0) === 0 ? 'hidden' : '' }}>{{ $cartCount ?? 0 }}</span>
                    </a>
                </div>
            </div>
        </nav>
    </div>
</div>
