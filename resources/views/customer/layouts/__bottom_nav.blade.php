<nav class="customer-bottom-nav d-xl-none" aria-label="Navigasi HP">
    <a href="{{ route('menu') }}" class="{{ request()->routeIs('menu') ? 'active' : '' }}">
        <i class="fa fa-utensils"></i>
        <span>Menu</span>
    </a>
    <a href="{{ route('customer.orders') }}" class="{{ request()->routeIs('customer.orders*') ? 'active' : '' }}">
        <i class="fa fa-receipt"></i>
        <span>Pesanan</span>
    </a>
    <a href="{{ route('cart') }}" class="{{ request()->routeIs('cart') || request()->routeIs('checkout*') ? 'active' : '' }}">
        <i class="fa fa-shopping-bag"></i>
        <span>Keranjang</span>
        <span class="cart-badge bottom-cart-badge" data-cart-count {{ ($cartCount ?? 0) === 0 ? 'hidden' : '' }}>{{ $cartCount ?? 0 }}</span>
    </a>
</nav>
