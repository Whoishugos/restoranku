@php
    $categoryName = $item->category?->cat_name;
@endphp
<div class="col-12 col-md-6 col-xl-4">
    <div class="rounded position-relative fruite-item menu-card h-100">
        <div class="fruite-img menu-card-img">
            <img src="{{ $item->imageUrl() }}" class="img-fluid w-100 rounded-top" alt="{{ $item->name }}" onerror="this.onerror=null;this.src='{{ asset('img_item_upload/default.jpg') }}';">
        </div>
        <div class="text-white px-3 py-1 rounded position-absolute menu-card-badge
            @if ($categoryName == 'Makanan')
                bg-warning
            @elseif ($categoryName == 'Minuman')
                bg-info
            @else
                bg-primary
            @endif">
            {{ $categoryName }}
        </div>
        <div class="p-3 p-md-4 border border-secondary border-top-0 rounded-bottom menu-card-body">
            <h4 class="menu-card-title">{{ $item->name }}</h4>
            <p class="text-limited mb-2">{{ $item->description }}</p>
            <div class="d-flex justify-content-between align-items-center flex-wrap gap-2 menu-card-meta">
                <p class="text-dark fs-5 fw-bold mb-0">{{ 'Rp'. number_format($item->price, 0, ',','.') }}</p>
                <a href="#" onclick="event.preventDefault(); customizeMenu({{ $item->id }})" class="btn border border-secondary rounded-pill px-3 text-primary"><i class="fa fa-shopping-bag me-2 text-primary"></i> <span class="menu-card-cta">Tambah</span></a>
            </div>
        </div>
    </div>
</div>
