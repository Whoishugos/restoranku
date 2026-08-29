<?php

namespace App\Http\Controllers;

use App\Models\Addon;
use App\Models\AddonGroup;
use App\Models\Category;
use App\Models\Item;
use Illuminate\Http\Request;

class AddonGroupController extends Controller
{
    public function index()
    {
        $groups = AddonGroup::with(['category', 'addons', 'items'])->orderBy('name')->get();

        return view('admin.addon.index', compact('groups'));
    }

    public function create()
    {
        $categories = Category::orderBy('cat_name')->get();
        $items = Item::with('category')->orderBy('name')->get();

        return view('admin.addon.create', compact('categories', 'items'));
    }

    public function store(Request $request)
    {
        $data = $this->validatedGroup($request);
        $group = AddonGroup::create($data);
        $group->items()->sync($request->input('item_ids', []));

        return redirect()->route('addon-groups.edit', $group)->with('success', 'Grup add-ons dibuat. Tambahkan pilihan di bawah.');
    }

    public function edit(AddonGroup $addon_group)
    {
        $addon_group->load(['addons', 'items']);
        $categories = Category::orderBy('cat_name')->get();
        $items = Item::with('category')->orderBy('name')->get();

        return view('admin.addon.edit', [
            'group' => $addon_group,
            'categories' => $categories,
            'items' => $items,
        ]);
    }

    public function update(Request $request, AddonGroup $addon_group)
    {
        $addon_group->update($this->validatedGroup($request));
        $addon_group->items()->sync($request->input('item_ids', []));

        return redirect()->route('addon-groups.edit', $addon_group)->with('success', 'Grup add-ons diperbarui.');
    }

    public function destroy(AddonGroup $addon_group)
    {
        $addon_group->addons()->delete();
        $addon_group->items()->detach();
        $addon_group->delete();

        return redirect()->route('addon-groups.index')->with('success', 'Grup add-ons dihapus.');
    }

    public function storeOption(Request $request, AddonGroup $addon_group)
    {
        $data = $this->validatedOption($request);
        if ($request->hasFile('img')) {
            $data['img'] = $this->storeImage($request);
        }
        $data['addon_group_id'] = $addon_group->id;
        $data['is_active'] = $request->boolean('is_active', true);
        Addon::create($data);

        return redirect()->route('addon-groups.edit', $addon_group)->with('success', 'Pilihan add-on ditambahkan.');
    }

    public function updateOption(Request $request, Addon $addon)
    {
        $data = $this->validatedOption($request, $addon->id);
        if ($request->hasFile('img')) {
            $data['img'] = $this->storeImage($request);
        }
        $data['is_active'] = $request->boolean('is_active');
        $addon->update($data);

        return redirect()->route('addon-groups.edit', $addon->addon_group_id)->with('success', 'Pilihan add-on diperbarui.');
    }

    public function destroyOption(Addon $addon)
    {
        $groupId = $addon->addon_group_id;
        $addon->delete();

        return redirect()->route('addon-groups.edit', $groupId)->with('success', 'Pilihan add-on dihapus.');
    }

    private function validatedGroup(Request $request): array
    {
        $validated = $request->validate([
            'name' => 'required|string|max:255',
            'type' => 'required|in:size,ingredient_add,ingredient_remove,companion',
            'category_id' => 'required|exists:categories,id',
            'min_select' => 'required|integer|min:0|max:20',
            'max_select' => 'required|integer|min:1|max:20',
            'is_active' => 'nullable|boolean',
            'item_ids' => 'nullable|array',
            'item_ids.*' => 'exists:items,id',
        ]);

        if ($validated['min_select'] > $validated['max_select']) {
            $validated['min_select'] = $validated['max_select'];
        }

        $validated['is_active'] = $request->boolean('is_active');

        unset($validated['item_ids']);

        return $validated;
    }

    private function validatedOption(Request $request, ?int $ignoreId = null): array
    {
        $unique = 'unique:addons,name';
        if ($ignoreId) {
            $unique .= ','.$ignoreId;
        }

        $data = $request->validate([
            'name' => 'required|string|max:255|'.$unique,
            'price' => 'required|integer',
            'stock' => 'required|integer|min:0',
            'img' => 'nullable|image|mimes:jpeg,png,jpg,gif|max:2048',
        ]);
        unset($data['img']);

        return $data;
    }

    private function storeImage(Request $request): string
    {
        $image = $request->file('img');
        $name = time().'_'.preg_replace('/\s+/', '_', $image->getClientOriginalName());
        $image->move(public_path('img_addon_upload'), $name);

        return $name;
    }
}
