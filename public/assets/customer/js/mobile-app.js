(function () {
    function setCartCount(count) {
        var value = Number(count || 0);
        document.querySelectorAll('[data-cart-count]').forEach(function (el) {
            el.textContent = String(value);
            if (value > 0) {
                el.removeAttribute('hidden');
            } else {
                el.setAttribute('hidden', 'hidden');
            }
        });
    }

    window.updateCartBadge = function (cart) {
        if (typeof cart === 'number') {
            setCartCount(cart);
            return;
        }
        var count = 0;
        Object.keys(cart || {}).forEach(function (key) {
            count += Number((cart[key] && cart[key].qty) || 0);
        });
        setCartCount(count);
    };

    if ('serviceWorker' in navigator) {
        window.addEventListener('load', function () {
            navigator.serviceWorker.register('/sw.js').catch(function () {});
        });
    }

    var banner = document.getElementById('pwa-install-banner');
    var installBtn = document.getElementById('pwa-install-btn');
    var dismissBtn = document.getElementById('pwa-install-dismiss');
    var hint = document.getElementById('pwa-install-hint');
    var deferredPrompt = null;
    var dismissedKey = 'kekupu-pwa-dismissed';

    function isStandalone() {
        return window.matchMedia('(display-mode: standalone)').matches
            || window.navigator.standalone === true;
    }

    function isIos() {
        return /iphone|ipad|ipod/i.test(window.navigator.userAgent);
    }

    function showBanner() {
        if (!banner || isStandalone() || localStorage.getItem(dismissedKey)) {
            return;
        }
        banner.hidden = false;
    }

    window.addEventListener('beforeinstallprompt', function (event) {
        event.preventDefault();
        deferredPrompt = event;
        if (installBtn) {
            installBtn.hidden = false;
        }
        showBanner();
    });

    if (isIos() && !isStandalone()) {
        if (hint) {
            hint.textContent = 'Di Safari: ketuk Bagikan, lalu pilih Tambah ke Layar Utama.';
        }
        if (installBtn) {
            installBtn.hidden = true;
        }
        showBanner();
    }

    if (installBtn) {
        installBtn.addEventListener('click', function () {
            if (!deferredPrompt) {
                return;
            }
            deferredPrompt.prompt();
            deferredPrompt.userChoice.finally(function () {
                deferredPrompt = null;
                if (banner) {
                    banner.hidden = true;
                }
            });
        });
    }

    if (dismissBtn) {
        dismissBtn.addEventListener('click', function () {
            localStorage.setItem(dismissedKey, '1');
            if (banner) {
                banner.hidden = true;
            }
        });
    }
})();
