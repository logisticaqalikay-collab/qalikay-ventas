import re
from pathlib import Path

html_path = Path('ejecucion/PROTOTIPO_DASHBOARD_VENTAS_QALIKAY.html')
lines = html_path.read_text(encoding='utf-8').splitlines()

font_size_pattern = re.compile(r'font-size:\s*([0-9\.]+(?:px|rem|em))', re.IGNORECASE)

print("INVENTARIO COMPLETO DE FUENTES SUB-12px:")
categorized = {
    'css_classes': [],
    'header_kpi': [],
    'feed_cards': [],
    'tables': [],
    'seller_drilldown': [],
    'supplier_drilldown': [],
    'modals': []
}

for i, l in enumerate(lines, 1):
    m = font_size_pattern.search(l)
    if m:
        val_str = m.group(1).lower()
        val = float(val_str.replace('px', '').replace('rem', '').replace('em', ''))
        if val < 12.0:
            item = (i, val_str, l.strip())
            if i < 735:
                categorized['css_classes'].append(item)
            elif 'feed' in l or 'latency' in l or 'metric-caption' in l or 'client' in l:
                categorized['feed_cards'].append(item)
            elif 'table' in l or 'th' in l or 'td' in l:
                categorized['tables'].append(item)
            elif 'seller' in l or 'dossier' in l:
                categorized['seller_drilldown'].append(item)
            elif 'supp' in l or 'supplier' in l:
                categorized['supplier_drilldown'].append(item)
            elif 'modal' in l or 'dropzone' in l or 'wa' in l:
                categorized['modals'].append(item)
            else:
                categorized['header_kpi'].append(item)

for cat, items in categorized.items():
    print(f"\n--- {cat.upper()} ({len(items)} ocurrencias) ---")
    for line_num, sz, snip in items:
        print(f"  L{line_num:4d} [{sz}]: {snip[:90]}")
