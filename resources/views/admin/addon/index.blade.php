@extends('admin.layouts.master')
@section('title', 'Manajemen Add-ons')

@section('content')
<div class="page-heading">
    <div class="page-title">
        <div class="row">
            <div class="col-12 col-md-6 order-md-1 order-last">
                <h3>Manajemen Add-ons</h3>
                <p class="text-subtitle text-muted">Kelompokkan pilihan berdasarkan kategori, atur wajib/opsional, stok, dan harga terkunci.</p>
            </div>
            <div class="col-12 col-md-6 order-md-2 order-first">
                <a href="{{ route('addon-groups.create') }}" class="btn btn-primary float-start float-lg-end">
                    <i class="bi bi-plus"></i> Tambah Grup
                </a>
            </div>
        </div>
    </div>
    <section class="section">
        <div class="card">
            <div class="card-body">
                @if (session('success'))
                    <div class="alert alert-success">{{ session('success') }}</div>
                @endif
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Grup</th>
                            <th>Tipe</th>
                            <th>Kategori</th>
                            <th>Aturan</th>
                            <th>Pilihan</th>
                            <th>Status</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        @forelse ($groups as $group)
                        <tr>
                            <td>{{ $group->name }}</td>
                            <td><span class="badge {{ \App\Models\AddonGroup::typeBadgeClass($group->type) }}">{{ $group->typeLabel() }}</span></td>
                            <td>{{ $group->category->cat_name ?? '-' }}</td>
                            <td>
                                Min {{ $group->min_select }} / Maks {{ $group->max_select }}
                                @if ($group->isRequired())
                                    <span class="badge bg-danger">Wajib</span>
                                @else
                                    <span class="badge bg-secondary">Opsional</span>
                                @endif
                                @if ($group->items->isNotEmpty())
                                    <div class="small text-muted">{{ $group->items->count() }} menu khusus</div>
                                @else
                                    <div class="small text-muted">Semua menu kategori</div>
                                @endif
                            </td>
                            <td>{{ $group->addons->count() }}</td>
                            <td>{{ $group->is_active ? 'Aktif' : 'Nonaktif' }}</td>
                            <td>
                                <a href="{{ route('addon-groups.edit', $group) }}" class="btn btn-warning btn-sm">Ubah</a>
                                <form action="{{ route('addon-groups.destroy', $group) }}" method="POST" class="d-inline">
                                    @csrf
                                    @method('DELETE')
                                    <button class="btn btn-danger btn-sm" onclick="return confirm('Hapus grup ini?')">Hapus</button>
                                </form>
                            </td>
                        </tr>
                        @empty
                        <tr><td colspan="7" class="text-center text-muted">Belum ada grup add-ons.</td></tr>
                        @endforelse
                    </tbody>
                </table>
            </div>
        </div>
    </section>
</div>
@endsection
