@extends('admin.layouts.master')
@section('title', 'Tambah Grup Add-ons')

@section('content')
<div class="page-title">
    <h3>Tambah Grup Add-ons</h3>
    <p class="text-subtitle text-muted">Petakan grup ke kategori agar rekomendasi tidak acak.</p>
</div>
<div class="card">
    <div class="card-body">
        @if ($errors->any())
            <div class="alert alert-danger">
                @foreach ($errors->all() as $error)<div>{{ $error }}</div>@endforeach
            </div>
        @endif
        <form method="POST" action="{{ route('addon-groups.store') }}">
            @csrf
            @include('admin.addon._group_fields', ['group' => null, 'categories' => $categories, 'items' => $items])
            <button class="btn btn-primary">Simpan & isi pilihan</button>
            <a href="{{ route('addon-groups.index') }}" class="btn btn-light">Batal</a>
        </form>
    </div>
</div>
@endsection
