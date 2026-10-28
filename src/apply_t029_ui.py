"""
Script determinista para aplicar las modificaciones de la Tarea T029
en ejecucion/PROTOTIPO_DASHBOARD_VENTAS_QALIKAY.html.
"""

from pathlib import Path
import sys

HTML_PATH = Path("ejecucion/PROTOTIPO_DASHBOARD_VENTAS_QALIKAY.html")

def apply_t029():
    html = HTML_PATH.read_text(encoding="utf-8")
    original_len = len(html)

    # 1. Botón en Toolbar de Pestaña 1
    t1_old = """            <button onclick="switchSellerSubMode('matrix')" id="btn-seller-matrix" class="pill-btn">📊 2. Matriz Comparativa de Vendedores</button>
          </div>"""
    t1_new = """            <button onclick="switchSellerSubMode('matrix')" id="btn-seller-matrix" class="pill-btn">📊 2. Matriz Comparativa de Vendedores</button>
            <button onclick="downloadAllSellersInactiveExcel()" class="pill-btn" style="background: #10b981; color: white; border: 1px solid #059669; font-weight: 700; display: flex; align-items: center; gap: 4px;" title="Exportar consolidado de clientes inactivos (>60 días) de todas las carteras en Excel">
              📥 Excel Clientes Inactivos (Todas las Carteras)
            </button>
          </div>"""
    if "downloadAllSellersInactiveExcel()" not in html:
        if t1_old in html:
            html = html.replace(t1_old, t1_new, 1)
            print("[OK 1/6] Botón Excel Clientes Inactivos (Todas las Carteras) agregado al toolbar de Pestaña 1.")
        else:
            print("[WARN 1/6] No se encontró ancla para botón de Pestaña 1.")
    else:
        print("[SKIP 1/6] Botón de Pestaña 1 ya presente.")

    # 2. Funciones JS: toggleSellerInactiveDetail y filterSellerInactives antes de toggleSellerCxcDetail
    js_funcs = """    let currentInactiveFilter = 'ALL';

    function toggleSellerInactiveDetail(filterType) {
      const panel = document.getElementById('seller-inactivos-detail-panel');
      if (!panel) return;
      if (filterType) {
        panel.classList.remove('hidden');
        filterSellerInactives(filterType);
        panel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      } else {
        panel.classList.toggle('hidden');
        if (!panel.classList.contains('hidden')) {
          panel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
      }
    }

    function filterSellerInactives(type) {
      currentInactiveFilter = type;
      const bAll = document.getElementById('btn-inact-all');
      const bUna = document.getElementById('btn-inact-una');
      const bRec = document.getElementById('btn-inact-rec');
      if (bAll) bAll.className = type === 'ALL' ? 'pill-btn active' : 'pill-btn';
      if (bUna) bUna.className = type === 'UNA_COMPRA' ? 'pill-btn active' : 'pill-btn';
      if (bRec) bRec.className = type === 'RECURRENTE' ? 'pill-btn active' : 'pill-btn';

      const tbody = document.getElementById('seller-inactivos-tbody');
      if (!tbody) return;
      const rows = tbody.querySelectorAll('tr[data-es-una]');
      rows.forEach(r => {
        const isUna = r.getAttribute('data-es-una') === '1';
        if (type === 'ALL') {
          r.style.display = '';
        } else if (type === 'UNA_COMPRA') {
          r.style.display = isUna ? '' : 'none';
        } else if (type === 'RECURRENTE') {
          r.style.display = !isUna ? '' : 'none';
        }
      });
    }

    function toggleSellerCxcDetail() {"""
    if "function toggleSellerInactiveDetail(" not in html:
        if "function toggleSellerCxcDetail() {" in html:
            html = html.replace("function toggleSellerCxcDetail() {", js_funcs, 1)
            print("[OK 2/6] Funciones toggleSellerInactiveDetail y filterSellerInactives insertadas.")
        else:
            print("[WARN 2/6] No se encontró toggleSellerCxcDetail().")
    else:
        print("[SKIP 2/6] Funciones toggleSellerInactiveDetail ya presentes.")

    # 3. Construir inactivosDetailRows antes de proySubText en renderSingleSellerDrilldown
    inact_builder = """      // T029: Construir tabla desplegable de Detalle de Clientes Inactivos (>60 Días)
      const inactList = s.inactivosDetalle || [];
      const unaCompraCount = s.inactivosUnaCompraCount || 0;
      const recurrentesCount = Math.max(0, inactList.length - unaCompraCount);
      let inactivosDetailRows = '';
      if (inactList.length === 0) {
        inactivosDetailRows = `
          <tr>
            <td colspan="12" style="padding: 24px; text-align: center; color: #64748b;">
              🎉 ¡Excelente! No hay clientes inactivos con más de 60 días sin compra en esta cartera.
            </td>
          </tr>
        `;
      } else {
        inactList.forEach(c => {
          const isUna = c.esUnaCompra;
          const badgeType = isUna
            ? '<span style="padding: 2px 8px; border-radius: 999px; font-size: 11px; font-weight: 800; background: #fff7ed; color: #ea580c; border: 1px solid #fdba74;">🟠 1 Sola Compra</span>'
            : '<span style="padding: 2px 8px; border-radius: 999px; font-size: 11px; font-weight: 800; background: #fef2f2; color: #dc2626; border: 1px solid #fecaca;">🔴 Recurrente Inactivo</span>';
          const telLink = c.celular ? `<a href="https://wa.me/51${c.celular.replace(/\\D/g, '')}" target="_blank" style="color: #059669; font-weight: 700; text-decoration: none;">📱 ${c.celular}</a>` : '<span style="color: #94a3b8;">Sin tel.</span>';
          const deudaStr = c.deudaVencida > 0 ? `<strong style="color: #dc2626;">S/ ${c.deudaVencida.toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</strong>` : '<span style="color: #059669;">Al día</span>';

          inactivosDetailRows += `
            <tr style="border-bottom: 1px solid #f1f5f9;" data-es-una="${isUna ? '1' : '0'}">
              <td style="padding: 8px 10px;">
                <strong style="color: #0f172a;">${c.comercial || c.cliente}</strong>
                <div style="font-size: 11px; color: #64748b;">${c.cliente !== c.comercial ? c.cliente + ' · ' : ''}RUC/DNI: ${c.ruc}</div>
              </td>
              <td style="padding: 8px 10px;">
                <div>${c.contacto || 'Sin contacto'}</div>
                <div style="font-size: 11px;">${telLink}</div>
              </td>
              <td style="padding: 8px 10px; color: #475569;">${c.distrito || '—'}</td>
              <td style="padding: 8px 10px; text-align: center; font-weight: 800; color: #1e293b;">${c.cantCompras}</td>
              <td style="padding: 8px 10px; text-align: center;">${badgeType}</td>
              <td style="padding: 8px 10px; text-align: center; font-family: monospace;">${c.ultimaCompra || '—'}</td>
              <td style="padding: 8px 10px; text-align: center; font-weight: 800; color: #b91c1c;">${c.diasSinCompra}d</td>
              <td style="padding: 8px 10px; text-align: center; color: #64748b;">${c.cicloHabitual}d</td>
              <td style="padding: 8px 10px; text-align: right; font-family: monospace; font-weight: 800; color: #047857;">S/ ${c.ticketPromedio.toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>
              <td style="padding: 8px 10px; text-align: right; font-family: monospace; color: #64748b;">S/ ${c.ultimoTicket.toLocaleString('es-PE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>
              <td style="padding: 8px 10px; text-align: right; font-family: monospace;">${deudaStr}</td>
              <td style="padding: 8px 10px; font-size: 11px; color: #334155; max-width: 280px; white-space: normal; line-height: 1.3;">${c.top3Productos || '—'}</td>
            </tr>
          `;
        });
      }

      const proySubText = pStats.proy"""
    if "const inactList = s.inactivosDetalle || [];" not in html:
        if "const proySubText = pStats.proy" in html:
            html = html.replace("const proySubText = pStats.proy", inact_builder, 1)
            print("[OK 3/6] Generación de inactivosDetailRows agregada en renderSingleSellerDrilldown.")
        else:
            print("[WARN 3/6] No se encontró const proySubText.")
    else:
        print("[SKIP 3/6] inactivosDetailRows ya presente.")

    # 4. Tarjeta KPI 4 Clickable en Dossier
    card4_old = """            <div class="hud-card alert" style="padding: 10px 12px; background: #fef2f2; border-color: #fecaca;">
              <div style="font-size: 11px; font-weight: 700; color: #b91c1c; text-transform: uppercase;">🔴 Inactivos &gt;2 Meses</div>
              <div style="font-size: 16px; font-weight: 900; color: #b91c1c;">${pStats.inactivos2m}</div>
              <div style="font-size: 11px; color: #dc2626; margin-top: 2px;">${pStats.una2m || 0} con 1 sola compra</div>
            </div>"""
    card4_new = """            <div class="hud-card alert cxc-clickable-card" onclick="toggleSellerInactiveDetail()" title="Haz clic para ver el listado detallado de clientes inactivos y descargar en Excel" style="padding: 10px 12px; background: #fef2f2; border: 2px solid #fca5a5; cursor: pointer;">
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 11px; font-weight: 800; color: #b91c1c; text-transform: uppercase;">🔴 Inactivos &gt;2 Meses</span>
                <span style="font-size: 10px; font-weight: 800; color: #b91c1c; background: #ffffff; padding: 1px 6px; border-radius: 999px; border: 1px solid #fecaca;">🔍 Ver Detalle</span>
              </div>
              <div style="font-size: 16px; font-weight: 900; color: #b91c1c; margin-top: 4px;">${pStats.inactivos2m}</div>
              <div style="font-size: 11px; color: #dc2626; margin-top: 2px;">${pStats.una2m || 0} con 1 sola compra · Clic para ver ▼</div>
            </div>"""
    if "toggleSellerInactiveDetail()" not in html or "onclick=\"toggleSellerInactiveDetail()\"" not in html:
        if card4_old in html:
            html = html.replace(card4_old, card4_new, 1)
            print("[OK 4/6] Tarjeta 4 Inactivos >2 Meses convertida a clickable con badge y subtítulo.")
        else:
            print("[WARN 4/6] No se encontró tarjeta 4 original.")
    else:
        print("[SKIP 4/6] Tarjeta 4 ya es clickable.")

    # 5. Insertar Contenedor Colapsable #seller-inactivos-detail-panel tras #seller-cxc-detail-panel
    panel_insert_marker = """          <!-- SECCIÓN DE 2 COLUMNAS: HISTORIAL 6 MESES vs MIX DE SKUS Y PROVEEDORES -->"""
    panel_html = """          <!-- SECCIÓN DESPLEGABLE: DETALLE DE CLIENTES INACTIVOS (>60 DÍAS) DE LA CARTERA (T029) -->
          <div id="seller-inactivos-detail-panel" class="hidden" style="background: #fff7ed; border: 2px solid #f97316; border-radius: 14px; padding: 18px; box-shadow: 0 4px 12px rgba(249,115,22,0.1); margin-top: 8px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; flex-wrap: wrap; gap: 8px;">
              <div>
                <h4 style="font-size: 14px; font-weight: 800; color: #9a3412;">
                  📁 Cartera de Clientes Inactivos (>60 Días) — ${s.nombre}
                </h4>
                <p style="font-size: 12px; color: #c2410c; margin-top: 2px;">
                  Total Inactivos: <strong>${(s.inactivosDetalle || []).length} clientes</strong> (${unaCompraCount} con 1 sola compra · ${recurrentesCount} recurrentes perdidos) · Ordenados por Ticket Promedio descendente
                </p>
              </div>
              <div style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap;">
                <button onclick="downloadSellerInactiveExcel('${sellerId}')" class="pill-btn" style="background: #10b981; color: white; border: 1px solid #059669; font-weight: 700; display: flex; align-items: center; gap: 4px;" title="Descargar listado de clientes inactivos de este vendedor en Excel">
                  📥 Descargar Excel Inactivos Cartera (.xlsx)
                </button>
                <button onclick="downloadAllSellersInactiveExcel()" class="pill-btn" style="background: #0284c7; color: white; border: 1px solid #0369a1; font-weight: 700; display: flex; align-items: center; gap: 4px;" title="Descargar consolidado completo de todas las carteras">
                  📥 Todas las Carteras (.xlsx)
                </button>
                <button onclick="toggleSellerInactiveDetail()" class="pill-btn" style="background: #ffffff; color: #9a3412; border: 1px solid #fdba74; font-weight: 800;">
                  ✖ Ocultar Detalle Inactivos
                </button>
              </div>
            </div>

            <!-- Filtros de Inactividad -->
            <div style="display: flex; gap: 8px; align-items: center; margin-bottom: 12px; flex-wrap: wrap;">
              <span style="font-size: 12px; font-weight: 700; color: #9a3412;">Filtrar por Tipo:</span>
              <button id="btn-inact-all" onclick="filterSellerInactives('ALL')" class="pill-btn active" style="font-size: 11px; padding: 3px 10px;">
                Todos (${(s.inactivosDetalle || []).length})
              </button>
              <button id="btn-inact-una" onclick="filterSellerInactives('UNA_COMPRA')" class="pill-btn" style="font-size: 11px; padding: 3px 10px;">
                🟠 1 Sola Compra (${unaCompraCount})
              </button>
              <button id="btn-inact-rec" onclick="filterSellerInactives('RECURRENTE')" class="pill-btn" style="font-size: 11px; padding: 3px 10px;">
                🔴 Recurrentes ≥2 Compras (${recurrentesCount})
              </button>
            </div>

            <!-- Tabla con Scroll -->
            <div style="overflow-x: auto; max-height: 420px; overflow-y: auto; background: #ffffff; border-radius: 10px; border: 1px solid #fed7aa;">
              <table style="width: 100%; border-collapse: collapse; font-size: 12px; text-align: left;">
                <thead style="position: sticky; top: 0; background: #ffedd5; z-index: 2;">
                  <tr style="border-bottom: 2px solid #fdba74; color: #9a3412;">
                    <th style="padding: 8px 10px;">Cliente / RUC</th>
                    <th style="padding: 8px 10px;">Contacto / Celular</th>
                    <th style="padding: 8px 10px;">Distrito</th>
                    <th style="padding: 8px 10px; text-align: center;">Compras Hist.</th>
                    <th style="padding: 8px 10px; text-align: center;">Tipo Inactividad</th>
                    <th style="padding: 8px 10px; text-align: center;">Última Compra</th>
                    <th style="padding: 8px 10px; text-align: center;">Días Inactivo</th>
                    <th style="padding: 8px 10px; text-align: center;">Ciclo Mediana</th>
                    <th style="padding: 8px 10px; text-align: right;">Ticket Prom.</th>
                    <th style="padding: 8px 10px; text-align: right;">Último Ticket</th>
                    <th style="padding: 8px 10px; text-align: right;">Deuda Vencida</th>
                    <th style="padding: 8px 10px;">Top 3 Productos Sugeridos (Recompra)</th>
                  </tr>
                </thead>
                <tbody id="seller-inactivos-tbody">
                  ${inactivosDetailRows}
                </tbody>
              </table>
            </div>
          </div>

          <!-- SECCIÓN DE 2 COLUMNAS: HISTORIAL 6 MESES vs MIX DE SKUS Y PROVEEDORES -->"""
    if "id=\"seller-inactivos-detail-panel\"" not in html:
        if panel_insert_marker in html:
            html = html.replace(panel_insert_marker, panel_html, 1)
            print("[OK 5/6] Panel colapsable #seller-inactivos-detail-panel insertado.")
        else:
            print("[WARN 5/6] No se encontró panel_insert_marker.")
    else:
        print("[SKIP 5/6] Panel #seller-inactivos-detail-panel ya presente.")

    # 6. Celdas clickables en Matriz Comparativa y Exportación Excel
    mat_old = """          <td style="text-align: center; font-weight: 800; color: #b45309; background: #fffbeb;">${r.una2m}</td>
          <td style="text-align: center; font-weight: 800; color: #b91c1c; background: #fef2f2;">${r.sin2m}</td>"""
    mat_new = """          <td style="text-align: center; font-weight: 800; color: #b45309; background: #fffbeb; cursor: pointer; text-decoration: underline;" onclick="openSellerDrilldown('${r.id}'); setTimeout(() => toggleSellerInactiveDetail('UNA_COMPRA'), 80);" title="Clic para ver detalle de clientes con 1 sola compra">${r.una2m}</td>
          <td style="text-align: center; font-weight: 800; color: #b91c1c; background: #fef2f2; cursor: pointer; text-decoration: underline;" onclick="openSellerDrilldown('${r.id}'); setTimeout(() => toggleSellerInactiveDetail('ALL'), 80);" title="Clic para ver detalle de clientes inactivos >2 meses">${r.sin2m}</td>"""
    if "toggleSellerInactiveDetail('UNA_COMPRA')" not in html:
        if mat_old in html:
            html = html.replace(mat_old, mat_new, 1)
            print("[OK 6a/6] Celdas una2m y sin2m convertidas a clickables en renderSellerMatrix.")
        else:
            print("[WARN 6a/6] No se encontraron celdas de matriz comparativa.")
    else:
        print("[SKIP 6a/6] Celdas de matriz comparativa ya clickables.")

    tot_old = """        <td style="text-align: center; font-weight: 800; color: #b45309;">${totUna2m}</td>
        <td style="text-align: center; font-weight: 800; color: #b91c1c;">${totSin2m}</td>"""
    tot_new = """        <td style="text-align: center; font-weight: 800; color: #b45309; cursor: pointer; text-decoration: underline;" onclick="downloadAllSellersInactiveExcel()" title="Descargar clientes con 1 sola compra de todas las carteras en Excel">${totUna2m}</td>
        <td style="text-align: center; font-weight: 800; color: #b91c1c; cursor: pointer; text-decoration: underline;" onclick="downloadAllSellersInactiveExcel()" title="Descargar todos los clientes inactivos de todas las carteras en Excel">${totSin2m}</td>"""
    if tot_old in html:
        html = html.replace(tot_old, tot_new, 1)
        print("[OK 6b/6] Celdas totales de inactivos convertidas a clickables para descarga Excel.")

    # 7. Funciones de Exportación Excel: downloadSellerInactiveExcel y downloadAllSellersInactiveExcel
    excel_funcs = """    function downloadSellerInactiveExcel(sellerId) {
      if (typeof XLSX === 'undefined') {
        alert('SheetJS (XLSX) no está disponible en este momento.');
        return;
      }
      const s = SELLER_DRILLDOWN_DETAILS[sellerId] || SELLER_DRILLDOWN_DETAILS['enrique'];
      const inactList = (s && s.inactivosDetalle) ? s.inactivosDetalle : [];
      const data = inactList.map(c => ({
        'Vendedor / Cartera': s.nombre || sellerId,
        'RUC / DNI': c.ruc,
        'Cliente': c.cliente,
        'Nombre Comercial': c.comercial,
        'Contacto': c.contacto,
        'Celular': c.celular,
        'Distrito': c.distrito,
        'Cant. Compras Históricas': c.cantCompras,
        'Tipo Inactividad': c.tipoInactividad,
        'Última Fecha Compra': c.ultimaCompra,
        'Días Sin Compra': c.diasSinCompra,
        'Ciclo Habitual (Días)': c.cicloHabitual,
        'Ticket Promedio (S/)': c.ticketPromedio,
        'Último Ticket (S/)': c.ultimoTicket,
        'Deuda Vencida CxC (S/)': c.deudaVencida,
        'Top 3 Productos Sugeridos': c.top3Productos
      }));

      const wb = XLSX.utils.book_new();
      const ws = XLSX.utils.json_to_sheet(data);
      const sheetName = (s && s.nombre) ? s.nombre.substring(0, 31).replace(/[:\\\\/?*[\\]]/g, '') : 'Inactivos';
      XLSX.utils.book_append_sheet(wb, ws, sheetName);
      XLSX.writeFile(wb, `Inactivos_${sellerId}_QaliKay.xlsx`);
    }

    function downloadAllSellersInactiveExcel() {
      if (typeof XLSX === 'undefined') {
        alert('SheetJS (XLSX) no está disponible en este momento.');
        return;
      }
      const allRows = [];
      const sellersOrder = ['enrique', 'walter', 'cristian', 'carlos', 'zully-b2b', 'zully-b2c'];
      sellersOrder.forEach(sid => {
        const s = SELLER_DRILLDOWN_DETAILS[sid];
        if (!s || !s.inactivosDetalle) return;
        s.inactivosDetalle.forEach(c => {
          allRows.push({
            'Vendedor': s.nombre || sid,
            'Canal Comercial': s.canal || '',
            'RUC / DNI': c.ruc,
            'Cliente': c.cliente,
            'Nombre Comercial': c.comercial,
            'Contacto': c.contacto,
            'Celular': c.celular,
            'Distrito': c.distrito,
            'Cant. Compras Históricas': c.cantCompras,
            'Tipo Inactividad': c.tipoInactividad,
            'Última Fecha Compra': c.ultimaCompra,
            'Días Sin Compra': c.diasSinCompra,
            'Ciclo Habitual (Días)': c.cicloHabitual,
            'Ticket Promedio (S/)': c.ticketPromedio,
            'Último Ticket (S/)': c.ultimoTicket,
            'Deuda Vencida CxC (S/)': c.deudaVencida,
            'Top 3 Productos Sugeridos': c.top3Productos
          });
        });
      });

      const wb = XLSX.utils.book_new();
      const ws = XLSX.utils.json_to_sheet(allRows);
      XLSX.utils.book_append_sheet(wb, ws, "Inactivos Todas Carteras");
      XLSX.writeFile(wb, "Clientes_Inactivos_Todas_Las_Carteras_QaliKay.xlsx");
    }
"""
    if "function downloadAllSellersInactiveExcel()" not in html:
        excel_marker = "    function downloadSellerCxcExcel(sellerId) {"
        if excel_marker in html:
            html = html.replace(excel_marker, excel_funcs + "\n    function downloadSellerCxcExcel(sellerId) {", 1)
            print("[OK 7/7] Funciones SheetJS downloadSellerInactiveExcel y downloadAllSellersInactiveExcel insertadas.")
        else:
            print("[WARN 7/7] No se encontró downloadSellerCxcExcel.")
    else:
        print("[SKIP 7/7] Funciones de exportación Excel ya presentes.")

    if len(html) != original_len:
        HTML_PATH.write_text(html, encoding="utf-8")
        print(f"[SUCCESS] HTML actualizado exitosamente. Nuevo tamaño: {len(html)} bytes.")
    else:
        print("[INFO] Sin cambios pendientes en el HTML.")

if __name__ == "__main__":
    apply_t029()
