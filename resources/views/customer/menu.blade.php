@extends('customer.layouts.master')

@section('content')
<!-- Single Page Header start -->
<div class="container-fluid page-header py-5">
    <h1 class="text-center text-white display-6">Menu</h1>
    <ol class="breadcrumb justify-content-center mb-0">
        <li class="breadcrumb-item active text-primary">Berbagai pilihan menu terbaik</li>
    </ol>
</div>
<!-- Single Page Header End -->
<!-- Fruits Shop Start-->
<div class="container-fluid fruite py-5">
    <div class="container py-5">
        @if (session('error'))
            <div class="alert alert-danger">{{ session('error') }}</div>
        @endif
        @if (session('success'))
            <div class="alert alert-success">{{ session('success') }}</div>
        @endif
        <ul class="nav nav-pills justify-content-center mb-5 gap-2" id="menu-category-tabs" role="tablist">
            <li class="nav-item" role="presentation">
                <button class="nav-link active rounded-pill px-4" id="tab-makanan-btn" data-bs-toggle="pill" data-bs-target="#tab-makanan" type="button" role="tab">Makanan</button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link rounded-pill px-4" id="tab-minuman-btn" data-bs-toggle="pill" data-bs-target="#tab-minuman" type="button" role="tab">Minuman</button>
            </li>
        </ul>
        <div class="tab-content">
            <div class="tab-pane fade show active" id="tab-makanan" role="tabpanel">
                <div class="row g-4 justify-content-center">
                    @forelse ($foods as $item)
                        @include('customer.partials.menu-card', ['item' => $item])
                    @empty
                        <p class="text-center text-muted">Belum ada menu makanan.</p>
                    @endforelse
                </div>
            </div>
            <div class="tab-pane fade" id="tab-minuman" role="tabpanel">
                <div class="row g-4 justify-content-center">
                    @forelse ($drinks as $item)
                        @include('customer.partials.menu-card', ['item' => $item])
                    @empty
                        <p class="text-center text-muted">Belum ada menu minuman.</p>
                    @endforelse
                </div>
            </div>
        </div>
    </div>
</div>
<!-- Fruits Shop End-->
<div class="modal fade" id="addonModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-lg modal-dialog-scrollable">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="addon-modal-title">Rekomendasi add-ons</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <div class="d-flex gap-3 mb-3">
                    <img id="addon-modal-img" src="" alt="" class="rounded" style="width: 96px; height: 96px; object-fit: cover;">
                    <div>
                        <div class="text-muted small">Harga berubah otomatis saat diklik. Pajak 10% dihitung di kasir.</div>
                        <div class="fs-4 fw-bold text-primary" id="addon-live-price">Rp0</div>
                    </div>
                </div>
                <div id="addon-groups"></div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-light" data-bs-dismiss="modal">Batal</button>
                <button type="button" class="btn btn-primary" id="addon-confirm-btn">Masukkan keranjang</button>
            </div>
        </div>
    </div>
</div>
@endsection

@section('script')
    <script>
        let addonState = { itemId: null, basePrice: 0, groups: [] };
        const addonModal = new bootstrap.Modal(document.getElementById('addonModal'));
        const customizeUrl = {!! json_encode(url('/menu')) !!};
        const cartAddUrl = {!! json_encode(route('cart.add')) !!};
        const csrf = {!! json_encode(csrf_token()) !!};

        function formatRp(n) {
            return 'Rp' + Number(n).toLocaleString('id-ID');
        }

        function selectedAddonIds() {
            const ids = [];
            document.querySelectorAll('#addon-groups input:checked').forEach(function (el) {
                ids.push(parseInt(el.value, 10));
            });
            return ids;
        }

        function livePrice() {
            let total = addonState.basePrice;
            document.querySelectorAll('#addon-groups input:checked').forEach(function (el) {
                total += parseInt(el.dataset.price || '0', 10);
            });
            document.getElementById('addon-live-price').textContent = formatRp(total);
        }

        function enforceGroup(groupId, maxSelect, single) {
            const inputs = document.querySelectorAll('.addon-group-' + groupId);
            const checked = Array.from(inputs).filter(function (el) { return el.checked; });
            if (single) {
                return;
            }
            if (checked.length > maxSelect) {
                checked[checked.length - 1].checked = false;
                alert('Maksimal ' + maxSelect + ' pilihan pada grup ini.');
            }
        }

        function renderGroups(data) {
            const wrap = document.getElementById('addon-groups');
            wrap.innerHTML = '';
            data.groups.forEach(function (group) {
                const box = document.createElement('div');
                box.className = 'mb-4';
                const req = group.required ? '<span class="badge bg-danger ms-1">Wajib</span>' : '<span class="badge bg-secondary ms-1">Opsional</span>';
                box.innerHTML = '<h6 class="mb-2">' + group.name + ' ' + req +
                    '<div class="small text-muted">' + group.type_label + ' · min ' + group.min_select + ' / maks ' + group.max_select + '</div></h6>';
                const row = document.createElement('div');
                row.className = 'row g-2';
                group.addons.forEach(function (addon) {
                    const col = document.createElement('div');
                    col.className = 'col-md-6';
                    const inputType = group.single ? 'radio' : 'checkbox';
                    const img = addon.img
                        ? '<img src="/img_addon_upload/' + addon.img + '" class="rounded me-2" style="width:48px;height:48px;object-fit:cover" alt="">'
                        : '';
                    const priceLabel = addon.price === 0 ? 'Rp0' : (addon.price > 0 ? '+' + formatRp(addon.price) : formatRp(addon.price));
                    col.innerHTML = '<label class="border rounded p-2 d-flex align-items-center w-100 h-100">' +
                        '<input class="form-check-input me-2 addon-group-' + group.id + '" type="' + inputType + '" name="group-' + group.id + '" value="' + addon.id +
                        '" data-price="' + addon.price + '" data-group="' + group.id + '" data-max="' + group.max_select + '" data-single="' + (group.single ? '1' : '0') + '">' +
                        img + '<span><strong>' + addon.name + '</strong><br><span class="small text-muted">' + priceLabel + ' · stok ' + addon.stock + '</span></span></label>';
                    row.appendChild(col);
                });
                box.appendChild(row);
                wrap.appendChild(box);
            });
            wrap.querySelectorAll('input').forEach(function (el) {
                el.addEventListener('change', function () {
                    enforceGroup(el.dataset.group, parseInt(el.dataset.max, 10), el.dataset.single === '1');
                    livePrice();
                });
            });
            livePrice();
        }

        function customizeMenu(menuId) {
            fetch(customizeUrl + '/' + menuId + '/customize', { headers: { 'Accept': 'application/json' } })
                .then(function (res) { return res.json().then(function (data) { return { ok: res.ok, data: data }; }); })
                .then(function (result) {
                    if (!result.ok) {
                        alert(result.data.message || 'Menu tidak tersedia');
                        return;
                    }
                    const payload = result.data.data;
                    addonState = { itemId: payload.item.id, basePrice: payload.item.price, groups: payload.groups };
                    document.getElementById('addon-modal-title').textContent = 'Kustomisasi ' + payload.item.name;
                    const img = document.getElementById('addon-modal-img');
                    img.src = '/img_item_upload/' + payload.item.image;
                    img.onerror = function () { this.src = payload.item.image; };
                    if (!payload.groups.length) {
                        addToCart(payload.item.id, []);
                        return;
                    }
                    renderGroups(payload);
                    addonModal.show();
                })
                .catch(function () { alert('Gagal memuat rekomendasi add-ons'); });
        }

        function addToCart(menuId, addonIds) {
            fetch(cartAddUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-TOKEN': csrf,
                    'Accept': 'application/json'
                },
                body: JSON.stringify({ id: menuId, addon_ids: addonIds || [] })
            })
            .then(function (res) { return res.json().then(function (data) { return { ok: res.ok, data: data }; }); })
            .then(function (result) {
                alert(result.data.message || (result.ok ? 'Berhasil' : 'Gagal'));
                if (result.ok) {
                    addonModal.hide();
                }
            })
            .catch(function () { alert('Gagal menambahkan ke keranjang'); });
        }

        document.getElementById('addon-confirm-btn').addEventListener('click', function () {
            for (let i = 0; i < addonState.groups.length; i++) {
                const group = addonState.groups[i];
                const count = document.querySelectorAll('.addon-group-' + group.id + ':checked').length;
                if (count < group.min_select) {
                    alert('Pilih minimal ' + group.min_select + ' opsi pada ' + group.name);
                    return;
                }
                if (count > group.max_select) {
                    alert('Maksimal ' + group.max_select + ' opsi pada ' + group.name);
                    return;
                }
            }
            addToCart(addonState.itemId, selectedAddonIds());
        });
    </script>
@endsection
