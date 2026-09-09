@include('customer.layouts.__header')

    <body class="customer-app">

        <!-- Spinner Start -->
        <div id="spinner" class="show w-100 vh-100 bg-white position-fixed translate-middle top-50 start-50  d-flex align-items-center justify-content-center">
            <div class="spinner-grow text-primary" role="status"></div>
        </div>
        <!-- Spinner End -->

        <!-- Navbar start -->
        @include('customer.layouts.__navbar')
        <!-- Navbar End -->

        <main class="customer-main">
            @yield('content')
        </main>

        <!-- Footer Start -->
        @include('customer.layouts.__footer')
        <!-- Footer End -->

        @include('customer.layouts.__bottom_nav')

        <div id="pwa-install-banner" class="pwa-install-banner d-xl-none" hidden>
            <div class="pwa-install-copy">
                <strong>Pasang di HP</strong>
                <div class="small" id="pwa-install-hint">Tambahkan ke layar utama supaya bisa dibuka seperti aplikasi.</div>
            </div>
            <button type="button" class="btn btn-primary btn-sm" id="pwa-install-btn">Pasang</button>
            <button type="button" class="btn btn-light btn-sm" id="pwa-install-dismiss" aria-label="Tutup">Nanti</button>
        </div>

        <!-- Back to Top -->
        <a href="#" class="btn btn-primary border-3 border-primary rounded-circle back-to-top"><i class="fa fa-arrow-up"></i></a>


    <!-- JavaScript Libraries -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.4/jquery.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="{{ asset('assets/customer/lib/easing/easing.min.js') }}"></script>
    <script src="{{ asset('assets/customer/lib/waypoints/waypoints.min.js') }}"></script>
    <script src="{{ asset('assets/customer/lib/lightbox/js/lightbox.min.js') }}"></script>
    <script src="{{ asset('assets/customer/lib/owlcarousel/owl.carousel.min.js') }}"></script>

    <!-- Template Javascript -->
    <script src="{{ asset('assets/customer/js/main.js') }}"></script>
    <script src="{{ asset('assets/customer/js/mobile-app.js') }}"></script>

    <script>
        document.getElementById('currentYear').textContent = new Date().getFullYear();
    </script>

    @yield('script')
    </body>
</html>
