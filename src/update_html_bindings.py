import shutil
from pathlib import Path

html_path = Path('ejecucion/PROTOTIPO_DASHBOARD_VENTAS_QALIKAY.html')
shutil.copy2(html_path, html_path.with_suffix('.html.bak'))

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. CLIENTS wrapping & _REAL
target_clients = """  <script>
    const CLIENTS = ["""

repl_clients = """  <script>
    const _REAL = (typeof window !== 'undefined' && window.__QALIKAY_REAL_DATA__) ? window.__QALIKAY_REAL_DATA__ : null;
    const CLIENTS = (_REAL && _REAL.CLIENTS && _REAL.CLIENTS.length > 0) ? _REAL.CLIENTS : ["""

assert target_clients in content, 'target_clients not found'
content = content.replace(target_clients, repl_clients, 1)

# 2. openWaModalByIndex and index assignment after CLIENTS
target_end_clients = """    ];

    function renderActionCards(filter) {"""

repl_end_clients = """    ];
    CLIENTS.forEach((c, idx) => { c._idx = idx; });

    function openWaModalByIndex(idx) {
      const c = CLIENTS[idx];
      if (!c) return;
      openWaModal(c.nombre, c.comercial, c.vendedor, c.phone, c.waMsg);
    }

    function renderActionCards(filter) {"""

assert target_end_clients in content, 'target_end_clients not found'
content = content.replace(target_end_clients, repl_end_clients, 1)

# 3. Replace openWaModal in renderActionCards and renderTableRows
old_line_1670 = "          <button onclick=\"openWaModal('${c.nombre}', '${c.comercial}', '${c.vendedor}', '${c.phone}', \\`${c.waMsg.replace(/`/g, '\\\\`')}\\`)\" class=\"btn-wa-action\">"
new_line_1670 = "          <button onclick=\"openWaModalByIndex(${c._idx})\" class=\"btn-wa-action\">"
assert old_line_1670 in content, 'old_line_1670 not found'
content = content.replace(old_line_1670, new_line_1670, 1)

old_line_1704 = "            <button onclick=\"openWaModal('${c.nombre}', '${c.comercial}', '${c.vendedor}', '${c.phone}', \\`${c.waMsg.replace(/`/g, '\\\\`')}\\`)\" class=\"btn-copy\">"
new_line_1704 = "            <button onclick=\"openWaModalByIndex(${c._idx})\" class=\"btn-copy\">"
assert old_line_1704 in content, 'old_line_1704 not found'
content = content.replace(old_line_1704, new_line_1704, 1)
print('Replaced both openWaModal button calls with openWaModalByIndex!')

# 4. SUPPLIERS_MONTHLY_DATA
target_supp = 'const SUPPLIERS_MONTHLY_DATA = {'
repl_supp = 'const SUPPLIERS_MONTHLY_DATA = (_REAL && _REAL.SUPPLIERS_MONTHLY_DATA) ? _REAL.SUPPLIERS_MONTHLY_DATA : {'
assert target_supp in content, 'target_supp not found'
content = content.replace(target_supp, repl_supp, 1)

# 5. SUPPLIER_TOP_SKUS_MASTER
target_skus = 'const SUPPLIER_TOP_SKUS_MASTER = {'
repl_skus = 'const SUPPLIER_TOP_SKUS_MASTER = (_REAL && _REAL.SUPPLIER_TOP_SKUS_MASTER) ? _REAL.SUPPLIER_TOP_SKUS_MASTER : {'
assert target_skus in content, 'target_skus not found'
content = content.replace(target_skus, repl_skus, 1)

# 6. SELLER_DRILLDOWN_DETAILS
target_drill = 'const SELLER_DRILLDOWN_DETAILS = {'
repl_drill = 'const SELLER_DRILLDOWN_DETAILS = (_REAL && _REAL.SELLER_DRILLDOWN_DETAILS) ? _REAL.SELLER_DRILLDOWN_DETAILS : {'
assert target_drill in content, 'target_drill not found'
content = content.replace(target_drill, repl_drill, 1)

# 7. MONTHLY_DATA
target_monthly = 'const MONTHLY_DATA = {'
repl_monthly = 'const MONTHLY_DATA = (_REAL && _REAL.MONTHLY_DATA) ? _REAL.MONTHLY_DATA : {'
assert target_monthly in content, 'target_monthly not found'
content = content.replace(target_monthly, repl_monthly, 1)

# 8. TIME_SERIES
target_ts = 'const TIME_SERIES = {'
repl_ts = 'const TIME_SERIES = (_REAL && _REAL.TIME_SERIES) ? _REAL.TIME_SERIES : {'
assert target_ts in content, 'target_ts not found'
content = content.replace(target_ts, repl_ts, 1)

# 9. Dropzone & applyRealDataToDom functions
dropzone_and_dom_funcs = '''
    // ==========================================================================
    // FUNCIONES DROPZONE (NIVEL 3 DE ACTUALIZACIÓN MANUAL)
    // ==========================================================================
    function openDropzoneModal() {
      const modal = document.getElementById('dropzone-modal');
      if (modal) modal.classList.remove('hidden');
    }

    function closeDropzoneModal() {
      const modal = document.getElementById('dropzone-modal');
      if (modal) modal.classList.add('hidden');
    }

    function handleDragOver(e) {
      e.preventDefault();
      e.stopPropagation();
      const area = document.getElementById('dropzone-area');
      if (area) {
        area.style.borderColor = '#2563eb';
        area.style.background = '#eff6ff';
      }
    }

    function handleDragLeave(e) {
      e.preventDefault();
      e.stopPropagation();
      const area = document.getElementById('dropzone-area');
      if (area) {
        area.style.borderColor = '#94a3b8';
        area.style.background = '#f8fafc';
      }
    }

    function handleFileDrop(e) {
      e.preventDefault();
      e.stopPropagation();
      handleDragLeave(e);
      const files = e.dataTransfer.files;
      if (files && files.length > 0) {
        processUploadedFile(files[0]);
      }
    }

    function handleFileSelect(e) {
      const files = e.target.files;
      if (files && files.length > 0) {
        processUploadedFile(files[0]);
      }
    }

    function copyBatCommand() {
      navigator.clipboard.writeText('.\\\\actualizar_dashboard.bat');
      alert('Comando copiado al portapapeles: .\\\\actualizar_dashboard.bat');
    }

    function processUploadedFile(file) {
      if (typeof XLSX === 'undefined') {
        alert('SheetJS (XLSX) no está disponible en este momento.');
        return;
      }
      const reader = new FileReader();
      reader.onload = function(e) {
        try {
          const data = new Uint8Array(e.target.result);
          const workbook = XLSX.read(data, { type: 'array' });
          const firstSheetName = workbook.SheetNames[0];
          const worksheet = workbook.Sheets[firstSheetName];
          const json = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
          
          const rowCount = json.length;
          const resBox = document.getElementById('dropzone-results');
          const resStats = document.getElementById('dropzone-result-stats');
          
          if (resBox && resStats) {
            resBox.classList.remove('hidden');
            resStats.innerHTML = `
              <div><strong>Archivo:</strong> ${file.name} (${Math.round(file.size / 1024)} KB)</div>
              <div><strong>Pestaña leída:</strong> ${firstSheetName}</div>
              <div><strong>Filas totales detectadas:</strong> ${rowCount.toLocaleString('es-PE')}</div>
              <div style="margin-top: 6px; color: #15803d; font-weight: 700;">
                ✨ Archivo analizado y verificado correctamente. Para consolidar en el Parquet de producción y recalcular los motores comerciales, ejecute el script por lotes <code>.\\\\actualizar_dashboard.bat</code>.
              </div>
            `;
          }
        } catch (err) {
          alert('Error al leer el archivo con SheetJS: ' + err.message);
        }
      };
      reader.readAsArrayBuffer(file);
    }

    // ==========================================================================
    // VINCULACIÓN DINÁMICA DE DATOS REALES AL DOM (HUD, HEADER, AGENDAS)
    // ==========================================================================
    function applyRealDataToDom() {
      if (!_REAL) return;
      
      // 1. Header status badges
      if (_REAL.SYNC_STATUS) {
        const s = _REAL.SYNC_STATUS;
        const elRpa = document.getElementById('status-val-rpa');
        if (elRpa) elRpa.textContent = s.estado || '🟢 Sincronizado';
        const elCli = document.getElementById('status-val-carteras');
        if (elCli) elCli.textContent = `⚙️ ${s.clientes_totales.toLocaleString('es-PE')} Cli`;
        const elKardex = document.getElementById('status-val-kardex');
        if (elKardex) elKardex.textContent = `📦 ${s.filas_kardex} SKUs`;
        const elSub = document.getElementById('sync-subtext');
        if (elSub) {
          elSub.innerHTML = `Última sync automática RPA: <strong>${s.ultima_actualizacion}</strong> (Nivel 1) · Exportado: ${s.timestamp_exportacion}`;
        }
      }
      
      // 2. HUD Executive Cards
      if (_REAL.MONTHLY_DATA && _REAL.MONTHLY_DATA['2026-10']) {
        const mRows = _REAL.MONTHLY_DATA['2026-10'];
        const totVenta = mRows.reduce((acc, r) => acc + (r.venta || 0), 0);
        const totProy = mRows.reduce((acc, r) => acc + (r.proy || 0), 0);
        const totPedidos = mRows.reduce((acc, r) => acc + (r.pedidos || 0), 0);
        
        const elVentas = document.getElementById('hud-val-ventas');
        if (elVentas) elVentas.textContent = fmtNum(totVenta, true);
        const elSubVentas = document.getElementById('hud-sub-ventas');
        if (elSubVentas) elSubVentas.textContent = `${totPedidos} pedidos cerrados`;
        const elHighVentas = document.getElementById('hud-highlight-ventas');
        if (elHighVentas) elHighVentas.textContent = `Proy: ${fmtNum(totProy, true)}`;
      }
      
      // 3. Alertas Críticas & B2C
      const cntCriticas = CLIENTS.filter(c => c.alertaClass === 'urgent').length;
      const cntDeudas = CLIENTS.filter(c => c.cxcIsDebt).length;
      const cntB2CVencidos = CLIENTS.filter(c => c.vendedor === 'Linda B2C' && (c.alerta.includes('VENCIDO') || c.alerta.includes('INACTIVO') || c.alerta.includes('25 DÍAS'))).length;
      
      const elCrit = document.getElementById('hud-val-criticas');
      if (elCrit) elCrit.textContent = `${cntCriticas.toLocaleString('es-PE')} Clientes`;
      const elSubCrit = document.getElementById('hud-sub-criticas');
      if (elSubCrit) elSubCrit.textContent = `${cntDeudas} en mora CxC`;
      const elB2c = document.getElementById('hud-val-b2c');
      if (elB2c) elB2c.textContent = `${cntB2CVencidos.toLocaleString('es-PE')} Consumidores`;
      
      // 4. Feed Filter Buttons Count
      const cntAll = CLIENTS.length;
      const cntCristian = CLIENTS.filter(c => c.vendedor === 'Cristian').length;
      const cntEnrique = CLIENTS.filter(c => c.vendedor === 'Enrique').length;
      const cntCarlos = CLIENTS.filter(c => c.vendedor === 'Carlos C').length;
      const cntWalter = CLIENTS.filter(c => c.vendedor === 'Walter').length;
      const cntLindaB2B = CLIENTS.filter(c => c.vendedor === 'Linda B2B').length;
      const cntLindaB2C = CLIENTS.filter(c => c.vendedor === 'Linda B2C').length;
      
      const bAll = document.getElementById('btn-feed-ALL');
      if (bAll) bAll.textContent = `Todos (${cntAll})`;
      const bCris = document.getElementById('btn-feed-Cristian');
      if (bCris) bCris.textContent = `⭐ Mi Cartera: Cristian (${cntCristian})`;
      const bEnr = document.getElementById('btn-feed-Enrique');
      if (bEnr) bEnr.textContent = `Enrique (${cntEnrique})`;
      const bCarl = document.getElementById('btn-feed-Carlos C');
      if (bCarl) bCarl.textContent = `Carlos C (${cntCarlos})`;
      const bWalt = document.getElementById('btn-feed-Walter');
      if (bWalt) bWalt.textContent = `Walter (${cntWalter})`;
      const bB2B = document.getElementById('btn-feed-Linda B2B');
      if (bB2B) bB2B.textContent = `🏢 Linda B2B (${cntLindaB2B})`;
      const bB2C = document.getElementById('btn-feed-Linda B2C');
      if (bB2C) bB2C.textContent = `👤 Linda B2C (${cntLindaB2C})`;
      const bB2CV = document.getElementById('btn-feed-B2C_VENCIDOS');
      if (bB2CV) bB2CV.textContent = `🚨 B2C Vencidos (${cntB2CVencidos})`;
      
      // 5. WhatsApp Agenda Blocks
      if (_REAL.WA_AGENDAS) {
        for (const [k, txt] of Object.entries(_REAL.WA_AGENDAS)) {
          const blk = document.getElementById('wa-' + k + '-block');
          if (blk) blk.textContent = txt;
        }
      }
    }
'''

target_init = '    // INICIALIZACIÓN COMPLETA'
repl_init = dropzone_and_dom_funcs + '\n    // INICIALIZACIÓN COMPLETA\n    applyRealDataToDom();'

assert target_init in content, 'target_init not found'
content = content.replace(target_init, repl_init, 1)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Successfully updated HTML file with real data wiring and dropzone logic!')
