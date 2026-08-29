@php
    $selectedItems = old('item_ids', $group?->items->pluck('id')->all() ?? []);
@endphp
<div class="form-group">
    <label>Nama grup</label>
    <input type="text" name="name" class="form-control" required value="{{ old('name', $group->name ?? '') }}" placeholder="Contoh: Tambah bahan">
</div>
<div class="form-group">
    <label>Tipe kustomisasi</label>
    <select name="type" class="form-select" required>
        @foreach (\App\Models\AddonGroup::typeLabels() as $value => $label)
            <option value="{{ $value }}" @selected(old('type', $group->type ?? '') === $value)>{{ $label }}</option>
        @endforeach
    </select>
</div>
<div class="form-group">
    <label>Kategori menu (pemetaan)</label>
    <select name="category_id" class="form-select" required>
        <option value="">Pilih kategori</option>
        @foreach ($categories as $category)
            <option value="{{ $category->id }}" @selected((int) old('category_id', $group->category_id ?? 0) === $category->id)>{{ $category->cat_name }}</option>
        @endforeach
    </select>
</div>
<div class="row">
    <div class="col-md-6">
        <div class="form-group">
            <label>Minimal pilih (0 = opsional)</label>
            <input type="number" name="min_select" class="form-control" min="0" max="20" required value="{{ old('min_select', $group->min_select ?? 0) }}">
        </div>
    </div>
    <div class="col-md-6">
        <div class="form-group">
            <label>Maksimal pilih</label>
            <input type="number" name="max_select" class="form-control" min="1" max="20" required value="{{ old('max_select', $group->max_select ?? 1) }}">
        </div>
    </div>
</div>
<div class="form-group">
    <div class="form-check form-switch">
        <input type="hidden" name="is_active" value="0">
        <input type="checkbox" class="form-check-input" name="is_active" value="1" @checked(old('is_active', $group->is_active ?? true))>
        <label>Aktif</label>
    </div>
</div>
<div class="form-group">
    <label>Batasi ke menu tertentu (kosongkan = semua menu kategori ini)</label>
    <div class="border rounded p-3" style="max-height: 220px; overflow:auto;">
        @foreach ($items as $item)
            <div class="form-check">
                <input class="form-check-input" type="checkbox" name="item_ids[]" value="{{ $item->id }}" id="map-item-{{ $item->id }}" @checked(in_array($item->id, $selectedItems, true))>
                <label class="form-check-label" for="map-item-{{ $item->id }}">{{ $item->name }} <span class="text-muted">({{ $item->category->cat_name ?? '-' }})</span></label>
            </div>
        @endforeach
    </div>
</div>
