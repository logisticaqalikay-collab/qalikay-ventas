import os
import re
import json
from pathlib import Path

html_path = Path('ejecucion/PROTOTIPO_DASHBOARD_VENTAS_QALIKAY.html')
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

print("=" * 80)
print("AUDITORIA EMPIRICA DE PREFLIGHT - FASE 5 (T020 Y T021)")
print("=" * 80)

# ----------------------------------------------------------------------
# 1. AUDITORIA TIPOGRAFICA (< 12px)
# ----------------------------------------------------------------------
# Buscamos en CSS y en estilos inline / template strings JS
font_size_pattern = re.compile(r'font-size:\s*([0-9\.]+(?:px|rem|em))', re.IGNORECASE)

lines = html.splitlines()
sub_12px_matches = []

for idx, line in enumerate(lines, 1):
    for m in font_size_pattern.finditer(line):
        val_str = m.group(1).lower()
        val = None
        if val_str.endswith('px'):
            val = float(val_str[:-2])
        elif val_str.endswith('rem') or val_str.endswith('em'):
            val = float(val_str[:-3]) * 16.0  # asumiendo 1rem = 16px
        
        if val is not None and val < 12.0:
            sub_12px_matches.append({
                'line': idx,
                'val_str': val_str,
                'val_px': val,
                'snippet': line.strip()[:100]
            })

print(f"\n[1.1 TIPOGRAFIA SUB-12px] Total de ocurrencias detectadas: {len(sub_12px_matches)}")
from collections import Counter
counts_by_size = Counter(m['val_str'] for m in sub_12px_matches)
for size, cnt in sorted(counts_by_size.items(), key=lambda x: x[1], reverse=True):
    print(f"   - {size:8s}: {cnt:3d} ocurrencias")

print("\n   Muestreo de componentes con texto menor a 12px:")
for sample in sub_12px_matches[:10]:
    print(f"   L{sample['line']:4d} [{sample['val_str']}]: {sample['snippet']}")

# ----------------------------------------------------------------------
# 2. AUDITORIA TOUCH TARGETS (< 48px)
# ----------------------------------------------------------------------
print("\n[1.2 TOUCH TARGETS] Analizando botones interactivos...")
button_classes = ['.pill-btn', '.tab-btn', '.toggle-btn', '.btn-copy', '.btn-wa-action', '.btn-open-wa']
for btn in button_classes:
    match = re.search(rf'{re.escape(btn)}\s*\{{([^}}]+)\}}', html)
    if match:
        css = match.group(1)
        padding = re.search(r'padding:\s*([^;]+);', css)
        height = re.search(r'(?:min-)?height:\s*([^;]+);', css)
        print(f"   Botón {btn}:")
        print(f"      Padding: {padding.group(1) if padding else 'No definido'}")
        print(f"      Height:  {height.group(1) if height else 'Auto / Contenido'}")

# ----------------------------------------------------------------------
# 3. TABULAR NUMS & MONOSPACE
# ----------------------------------------------------------------------
print("\n[1.3 ALINEACION TABULAR NUMS]")
has_tabular = 'tabular-nums' in html
print(f"   - ¿Usa font-variant-numeric: tabular-nums?: {has_tabular}")
has_monospace = 'font-family: monospace' in html
print(f"   - ¿Usa font-family: monospace en montos?:   {has_monospace}")

# ----------------------------------------------------------------------
# 4. RENDIMIENTO DOM FEED (1,312 CLIENTES)
# ----------------------------------------------------------------------
print("\n[1.4 RENDIMIENTO DOM DEL FEED (1,312 CLIENTES)]")
# Contar elementos HTML creados por tarjeta
card_template_match = re.search(r'card\.innerHTML\s*=\s*`([^`]+)`', html)
if card_template_match:
    tpl = card_template_match.group(1)
    tag_count = len(re.findall(r'<[a-zA-Z0-9]+', tpl))
    total_nodes = 1312 * (tag_count + 1)
    print(f"   - Etiquetas HTML por tarjeta: ~{tag_count}")
    print(f"   - Nodos DOM inyectados al renderizar 1,312 tarjetas: ~{total_nodes:,} nodos!")
    print(f"   - Impacto: Carga masiva síncrona puede causar tirones (jank) o 'Page Unresponsive' en Safari iOS / Android.")

# ----------------------------------------------------------------------
# 5. AUDITORIA GIT Y ENTORNO
# ----------------------------------------------------------------------
print("\n[2.1 ENTORNO GIT]")
cur_dir = Path.cwd()
has_git_repo = (cur_dir / '.git').exists()
print(f"   - Directorio de trabajo: {cur_dir}")
print(f"   - ¿Existe repositorio .git local?: {has_git_repo}")

# Buscar git.exe en ubicaciones conocidas
potential_git_paths = [
    Path(r"C:\Program Files\Git\bin\git.exe"),
    Path(r"C:\Program Files\Git\cmd\git.exe"),
    Path(r"C:\Program Files (x86)\Git\bin\git.exe"),
    Path(r"C:\Program Files (x86)\Git\cmd\git.exe"),
    Path(os.environ.get('LOCALAPPDATA', '')) / r"Programs\Git\bin\git.exe",
    Path(os.environ.get('LOCALAPPDATA', '')) / r"GitHubDesktop\app-3.4.15\resources\app\git\cmd\git.exe",
    Path(os.environ.get('LOCALAPPDATA', '')) / r"GitHubDesktop\bin\git.exe",
]
found_git = None
for p in potential_git_paths:
    if p.exists():
        found_git = p
        break

print(f"   - git.exe encontrado en disco: {found_git}")

# Buscar si proyectos hermanos tienen .git
parent_dir = cur_dir.parent
siblings = list(parent_dir.glob("*"))
print(f"   - Carpetas hermanas en {parent_dir}:")
for s in siblings:
    if s.is_dir():
        is_repo = (s / '.git').exists()
        print(f"      * {s.name}: {'[REPOSITORIO .GIT]' if is_repo else '[No git]'}")

# ----------------------------------------------------------------------
# 6. ARCHIVOS SENSIBLES A IGNORAR (.gitignore)
# ----------------------------------------------------------------------
print("\n[2.2 ARCHIVOS SENSIBLES Y PESADOS EN data/]")
data_dir = cur_dir / 'data'
if data_dir.exists():
    for f in data_dir.glob('*'):
        sz_mb = f.stat().st_size / (1024 * 1024)
        print(f"   - {f.name:45s} ({sz_mb:6.2f} MB)")
