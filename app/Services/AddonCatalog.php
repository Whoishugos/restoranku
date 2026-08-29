<?php

namespace App\Services;

use App\Models\Addon;
use App\Models\AddonGroup;
use App\Models\Item;
use Illuminate\Support\Collection;
use Illuminate\Validation\ValidationException;

class AddonCatalog
{
    public function groupsForItem(Item $item): Collection
    {
        if (! $item->category_id) {
            return collect();
        }

        return AddonGroup::with(['addons' => function ($query) {
            $query->where('is_active', true)->where('stock', '>', 0);
        }, 'items'])
            ->where('is_active', true)
            ->where('category_id', $item->category_id)
            ->orderBy('name')
            ->get()
            ->filter(function (AddonGroup $group) use ($item) {
                if ($group->items->isEmpty()) {
                    return true;
                }

                return $group->items->contains('id', $item->id);
            })
            ->values();
    }

    public function payloadForItem(Item $item): array
    {
        $groups = $this->groupsForItem($item);

        return [
            'item' => [
                'id' => $item->id,
                'name' => $item->name,
                'price' => (int) $item->price,
                'image' => $item->img,
                'stock' => (int) $item->stock,
            ],
            'groups' => $groups->map(function (AddonGroup $group) {
                return [
                    'id' => $group->id,
                    'name' => $group->name,
                    'type' => $group->type,
                    'type_label' => $group->typeLabel(),
                    'required' => $group->isRequired(),
                    'min_select' => $group->min_select,
                    'max_select' => $group->max_select,
                    'single' => $group->isSingle(),
                    'addons' => $group->addons->map(function (Addon $addon) {
                        return [
                            'id' => $addon->id,
                            'name' => $addon->name,
                            'price' => (int) $addon->price,
                            'img' => $addon->img,
                            'stock' => (int) $addon->stock,
                        ];
                    })->values(),
                ];
            })->values(),
        ];
    }

    /**
     * @param  list<int>  $addonIds
     * @return list<array{id: int, name: string, price: int, type: string, type_label: string}>
     */
    public function validateAndSnapshot(Item $item, array $addonIds): array
    {
        $ids = collect($addonIds)->map(fn ($id) => (int) $id)->filter()->unique()->values();
        $groups = $this->groupsForItem($item);
        $allowed = $groups->flatMap->addons->keyBy('id');

        foreach ($ids as $id) {
            if (! $allowed->has($id)) {
                throw ValidationException::withMessages([
                    'addons' => 'Pilihan add-ons tidak valid untuk menu ini.',
                ]);
            }
        }

        foreach ($groups as $group) {
            $selectedInGroup = $group->addons->whereIn('id', $ids)->count();
            if ($selectedInGroup < $group->min_select) {
                throw ValidationException::withMessages([
                    'addons' => 'Pilih minimal '.$group->min_select.' opsi pada '.$group->name.'.',
                ]);
            }
            if ($selectedInGroup > $group->max_select) {
                throw ValidationException::withMessages([
                    'addons' => 'Maksimal '.$group->max_select.' opsi pada '.$group->name.'.',
                ]);
            }
        }

        $snapshot = [];
        foreach ($ids as $id) {
            $addon = $allowed->get($id);
            $group = $groups->first(fn (AddonGroup $candidate) => $candidate->addons->contains('id', $id));
            $snapshot[] = [
                'id' => $addon->id,
                'name' => $addon->name,
                'price' => (int) $addon->price,
                'type' => $group?->type ?? AddonGroup::TYPE_ADD,
                'type_label' => $group?->typeLabel() ?? 'Add-on',
            ];
        }

        return $snapshot;
    }
}
