@include('admin.layouts.__header')

<body>
    <script src="{{ asset('assets/admin/static/js/initTheme.js') }}"></script>
    @include('admin.layouts.__sidebar')

    <div id="app">
        <div id="main">
            <header class="mb-3 d-flex justify-content-between align-items-center">
                <a href="#" class="burger-btn d-block d-xl-none">
                    <i class="bi bi-justify fs-3"></i>
                </a>
                <div class="dropdown ms-auto" id="order-notification">
                    <a href="#" class="d-inline-flex align-items-center gap-2 text-gray-600" data-bs-toggle="dropdown" aria-expanded="false" aria-label="Notifikasi pesanan">
                        <i class="bi bi-bell-fill fs-4"></i>
                        <span class="badge bg-danger" id="order-notif-badge" style="display: none;">0</span>
                    </a>
                    <div class="dropdown-menu dropdown-menu-end" style="min-width: 320px; max-width: 360px;">
                        <h6 class="dropdown-header">Pesanan baru</h6>
                        <div id="order-notif-list">
                            <p class="dropdown-item-text text-muted mb-0">Belum ada pesanan baru.</p>
                        </div>
                        <div class="dropdown-divider"></div>
                        <a class="dropdown-item text-center" href="{{ route('orders.index') }}">Lihat semua pesanan</a>
                    </div>
                </div>
            </header>

            @yield('content')

            @include('admin.layouts.__footer')

        </div>
    </div>

    <div class="toast-container position-fixed top-0 end-0 p-3" style="z-index: 1080;">
        <div id="new-order-toast" class="toast align-items-center text-bg-primary border-0" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body" id="new-order-toast-body">Ada pesanan baru.</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    </div>

    <script src="{{ asset('assets/admin/static/js/components/dark.js') }}"></script>
    <script src="{{ asset('assets/admin/extensions/perfect-scrollbar/perfect-scrollbar.min.js') }}"></script>
    <script src="{{ asset('assets/admin/compiled/js/app.js') }}"></script>
    <script>
        (function () {
            const feedUrl = @json(route('dashboard.notifications'));
            const storageKey = 'restoranku.order.seen_id';
            const badge = document.getElementById('order-notif-badge');
            const list = document.getElementById('order-notif-list');
            const toastEl = document.getElementById('new-order-toast');
            const toastBody = document.getElementById('new-order-toast-body');
            const sidebarBadge = document.getElementById('sidebar-order-badge');
            const listsEl = document.getElementById('dashboard-order-lists');
            let seenId = parseInt(localStorage.getItem(storageKey) || '0', 10);

            function escapeHtml(value) {
                return String(value ?? '').replace(/[&<>"']/g, function (char) {
                    return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[char];
                });
            }

            function setBadge(count) {
                if (!badge) return;
                if (count > 0) {
                    badge.textContent = count > 99 ? '99+' : String(count);
                    badge.style.display = 'inline-block';
                } else {
                    badge.style.display = 'none';
                }
                if (sidebarBadge) {
                    if (count > 0) {
                        sidebarBadge.textContent = count > 99 ? '99+' : String(count);
                        sidebarBadge.style.display = 'inline-block';
                    } else {
                        sidebarBadge.style.display = 'none';
                    }
                }
            }

            function renderList(orders) {
                if (!list) return;
                if (!orders.length) {
                    list.innerHTML = '<p class="dropdown-item-text text-muted mb-0">Belum ada pesanan baru.</p>';
                    return;
                }
                list.innerHTML = orders.map(function (order) {
                    return '<a class="dropdown-item py-2" href="' + escapeHtml(order.url) + '">'
                        + '<div class="fw-semibold">' + escapeHtml(order.order_code) + '</div>'
                        + '<div class="small text-muted">Meja ' + escapeHtml(order.table_number)
                        + ' · ' + escapeHtml(order.customer)
                        + ' · ' + escapeHtml(order.grand_total_label) + '</div>'
                        + '<span class="badge ' + escapeHtml(order.status_badge) + '">' + escapeHtml(order.status_label) + '</span>'
                        + '</a>';
                }).join('');
            }

            function showToast(orders) {
                if (!toastEl || !window.bootstrap) return;
                const first = orders[0];
                const extra = orders.length > 1 ? ' dan ' + (orders.length - 1) + ' pesanan lain' : '';
                toastBody.textContent = first
                    ? ('Pesanan baru ' + first.order_code + ' (Meja ' + first.table_number + ')' + extra)
                    : 'Ada pesanan baru.';
                bootstrap.Toast.getOrCreateInstance(toastEl, { delay: 8000 }).show();
            }

            function poll() {
                fetch(feedUrl + '?since_id=' + encodeURIComponent(seenId), {
                    headers: { 'Accept': 'application/json' },
                    credentials: 'same-origin'
                })
                    .then(function (response) { return response.json(); })
                    .then(function (data) {
                        const latestId = Number(data.latest_id || 0);
                        const newOrders = data.new_orders || [];
                        renderList(data.recent_orders || []);
                        setBadge(data.pending_count || 0);

                        if (seenId === 0) {
                            seenId = latestId;
                            localStorage.setItem(storageKey, String(seenId));
                            return;
                        }

                        if (newOrders.length > 0) {
                            showToast(newOrders);
                            seenId = latestId;
                            localStorage.setItem(storageKey, String(seenId));
                            if (listsEl) {
                                window.setTimeout(function () { window.location.reload(); }, 8500);
                            }
                        }
                    })
                    .catch(function () {});
            }

            document.getElementById('order-notification')?.addEventListener('show.bs.dropdown', function () {
                fetch(feedUrl, { headers: { 'Accept': 'application/json' }, credentials: 'same-origin' })
                    .then(function (response) { return response.json(); })
                    .then(function (data) {
                        seenId = Number(data.latest_id || seenId);
                        localStorage.setItem(storageKey, String(seenId));
                    })
                    .catch(function () {});
            });

            poll();
            window.setInterval(poll, 8000);
        })();
    </script>

    @yield('script')

</body>

</html>
