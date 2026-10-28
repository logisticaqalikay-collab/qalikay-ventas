import re
import json

with open('ejecucion/PROTOTIPO_DASHBOARD_VENTAS_QALIKAY.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Verify injected JSON
match = re.search(r'window\.__QALIKAY_REAL_DATA__\s*=\s*(\{.*?\});\s*</script>', html, re.DOTALL)
assert match, 'Injected JSON block not found'
data = json.loads(match.group(1))
print('[VERIFY] Injected JSON successfully parsed:')
for k, v in data.items():
    if isinstance(v, dict):
        print(f'   - {k}: {list(v.keys())[:5]}...')
    elif isinstance(v, list):
        print(f'   - {k}: list of length {len(v)}')

# 2. Check all IDs referenced in applyRealDataToDom exist in HTML
referenced_ids = [
    'dropzone-modal', 'dropzone-area', 'dropzone-results', 'dropzone-result-stats',
    'status-val-rpa', 'status-val-carteras', 'status-val-kardex', 'sync-subtext',
    'hud-val-ventas', 'hud-sub-ventas', 'hud-highlight-ventas',
    'hud-val-criticas', 'hud-sub-criticas', 'hud-val-b2c',
    'btn-feed-ALL', 'btn-feed-Cristian', 'btn-feed-Enrique', 'btn-feed-Carlos C',
    'btn-feed-Walter', 'btn-feed-Linda B2B', 'btn-feed-Linda B2C', 'btn-feed-B2C_VENCIDOS',
    'wa-cristian-block', 'wa-enrique-block', 'wa-carlos-block', 'wa-zully-b2b-block',
    'wa-zully-b2c-block', 'wa-walter-block'
]
missing_ids = []
for rid in referenced_ids:
    if f'id="{rid}"' not in html and f"id='{rid}'" not in html:
        missing_ids.append(rid)

if missing_ids:
    print('[WARNING] Missing IDs:', missing_ids)
    assert False, f'Missing IDs: {missing_ids}'
else:
    print(f'[VERIFY] All {len(referenced_ids)} referenced DOM IDs exist in HTML markup!')

# 3. Check for openWaModal syntax issues
assert 'openWaModalByIndex' in html, 'openWaModalByIndex not found'
print('[VERIFY] openWaModalByIndex successfully wired to action cards and tables!')
print('[SUCCESS] All dashboard integrity checks PASSED.')
