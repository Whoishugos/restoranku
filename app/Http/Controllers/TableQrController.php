<?php
namespace App\Http\Controllers;
use Illuminate\Http\Request;
use Illuminate\View\View;
class TableQrController extends Controller
{
    public function index(Request $request): View
    {
        $tableCount = (int) $request->query('jumlah', 12);
        $tableCount = max(1, min($tableCount, 50));
        $tables = [];
        for ($i = 1; $i <= $tableCount; $i++) {
            $tables[] = [
                'number' => $i,
                'url' => route('menu.scan', ['tableNumber' => $i]),
            ];
        }
        return view('admin.table.index', compact('tables', 'tableCount'));
    }
}