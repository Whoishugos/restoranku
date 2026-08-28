<div class="container-fluid fixed-top">
    <div class="container px-0">
        <nav class="navbar navbar-light bg-white navbar-expand-xl">
            <a href="{{ route('menu') }}" class="navbar-brand"><h1 class="text-primary display-6">RESTORAN KEKUPU VILLA JEMBRANA</h1></a>
            <button class="navbar-toggler py-2 px-3" type="button" data-bs-toggle="collapse" data-bs-target="#navbarCollapse">
                <span class="fa fa-bars text-primary"></span>
            </button>
            <div class="collapse navbar-collapse bg-white" id="navbarCollapse">
                <div class="navbar-nav mx-auto">
                    <a href="{{ route('menu') }}" class="nav-item nav-link {{ request()->routeIs('menu') ? 'active' : '' }}">Menu</a>
                    <a href="{{ route('customer.orders') }}" class="nav-item nav-link {{ request()->routeIs('customer.orders*') ? 'active' : '' }}">Pesanan Saya</a>
                </div>
                <div class="d-flex m-3 me-0">
                    <a href="{{ route('cart') }}" class="position-relative me-4 my-auto">
                        <i class="fa fa-shopping-bag fa-2x"></i>
                    </a>
                </div>
            </div>
        </nav>
    </div>
</div>


