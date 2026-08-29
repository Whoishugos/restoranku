@if (! empty($addons))
    <div class="kds-ticket mt-1">
        @foreach ($addons as $addon)
            <div class="fw-bold mb-1" style="font-size: 1.05rem; letter-spacing: .02em;">
                <span class="badge {{ \App\Models\AddonGroup::typeBadgeClass($addon['type'] ?? '') }} px-2 py-2">
                    {{ strtoupper($addon['type_label'] ?? 'ADD-ON') }}: {{ strtoupper($addon['name'] ?? '') }}
                </span>
            </div>
        @endforeach
    </div>
@endif

