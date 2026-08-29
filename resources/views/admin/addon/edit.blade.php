@extends('admin.layouts.master')
@section('title', 'Ubah Grup Add-ons')

@section('content')
<div class="page-title">
    <h3>Ubah Grup: {{ $group->name }}</h3>
</div>
@if (session('success'))
    <div class="alert alert-success">{{ session('success') }}</div>
@endif
@if ($errors->any())
    <div class="alert alert-danger">
        @foreach ($errors->all() as $error)<div>{{ $error }}</div>@endforeach
    </div>
@endif
<div class="card mb-4">
    <div class="card-body">
        <form method="POST" action="{{ route('addon-groups.update', $group) }}">
            @csrf
            @method('PUT')
            @include('admin.addon._group_fields', ['group' => $group, 'categories' => $categories, 'items' => $items])
            <button class="btn btn-primary">Simpan grup</button>
            <a href="{{ route('addon-groups.index') }}" class="btn btn-light">Kembali</a>
        </form>
    </div>
</div>

<div class="card">
    <div class="card-header"><h5 class="mb-0">Pilihan dalam grup</h5></div>
    <div class="card-body">
        <table class="table">
            <thead>
                <tr>
                    <th>Gambar</th>
                    <th>Nama</th>
                    <th>Harga</th>
                    <th>Stok</th>
                    <th>Aktif</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                @foreach ($group->addons as $addon)
                <tr>
                    <td>
                        @if ($addon->img)
                            <img src="{{ asset('img_addon_upload/'.$addon->img) }}" width="48" class="rounded" alt="">
                        @else
                            <span class="text-muted">—</span>
                        @endif
                    </td>
                    <td>{{ $addon->name }}</td>
                    <td>Rp{{ number_format($addon->price, 0, ',', '.') }}</td>
                    <td>{{ $addon->stock }}</td>
                    <td>{{ $addon->is_active ? 'Ya' : 'Tidak' }}</td>
                    <td>
                        <form action="{{ route('addons.update', $addon) }}" method="POST" enctype="multipart/form-data" class="row g-1 align-items-end">
                            @csrf
                            @method('PUT')
                            <div class="col-auto"><input type="text" name="name" class="form-control form-control-sm" value="{{ $addon->name }}" required></div>
                            <div class="col-auto"><input type="number" name="price" class="form-control form-control-sm" value="{{ $addon->price }}" required></div>
                            <div class="col-auto"><input type="number" name="stock" class="form-control form-control-sm" value="{{ $addon->stock }}" min="0" required></div>
                            <div class="col-auto"><input type="file" name="img" class="form-control form-control-sm"></div>
                            <div class="col-auto">
                                <input type="hidden" name="is_active" value="0">
                                <div class="form-check"><input class="form-check-input" type="checkbox" name="is_active" value="1" @checked($addon->is_active)><label class="form-check-label">Aktif</label></div>
                            </div>
                            <div class="col-auto"><button class="btn btn-sm btn-warning">Simpan</button></div>
                        </form>
                        <form action="{{ route('addons.destroy', $addon) }}" method="POST" class="d-inline">
                            @csrf
                            @method('DELETE')
                            <button class="btn btn-sm btn-danger mt-1" onclick="return confirm('Hapus pilihan ini?')">Hapus</button>
                        </form>
                    </td>
                </tr>
                @endforeach
            </tbody>
        </table>

        <h6 class="mt-4">Tambah pilihan</h6>
        <form action="{{ route('addon-groups.options.store', $group) }}" method="POST" enctype="multipart/form-data" class="row g-2 align-items-end">
            @csrf
            <div class="col-md-3"><label class="form-label">Nama</label><input type="text" name="name" class="form-control" required></div>
            <div class="col-md-2"><label class="form-label">Harga (boleh 0)</label><input type="number" name="price" class="form-control" value="0" required></div>
            <div class="col-md-2"><label class="form-label">Stok gudang</label><input type="number" name="stock" class="form-control" value="100" min="0" required></div>
            <div class="col-md-3"><label class="form-label">Gambar</label><input type="file" name="img" class="form-control"></div>
            <div class="col-md-2">
                <input type="hidden" name="is_active" value="0">
                <div class="form-check mb-2"><input class="form-check-input" type="checkbox" name="is_active" value="1" checked><label>Aktif</label></div>
                <button class="btn btn-primary">Tambah</button>
            </div>
        </form>
    </div>
</div>
@endsection
