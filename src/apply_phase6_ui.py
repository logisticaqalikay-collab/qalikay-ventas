"""
Script determinista para aplicar las modificaciones de la Fase 6 (T025 y T026)
en ejecucion/PROTOTIPO_DASHBOARD_VENTAS_QALIKAY.html.
"""

from pathlib import Path
import re

HTML_PATH = Path("ejecucion/PROTOTIPO_DASHBOARD_VENTAS_QALIKAY.html")

def apply_phase6_ui():
    html = HTML_PATH.read_text(encoding="utf-8")

    # 1. Declarar GLOBAL_CXC_VENCIDOS y LINDA_B2C_FULL_HISTORY en JS tras const _REAL
    real_decl = "const _REAL = (typeof window !== 'undefined' && window.__QALIKAY_REAL_DATA__) ? window.__QALIKAY_REAL_DATA__ : null;"
    target_vars = """const _REAL = (typeof window !== 'undefined' && window.__QALIKAY_REAL_DATA__) ? window.__QALIKAY_REAL_DATA__ : null;
    const GLOBAL_CXC_VENCIDOS = (_REAL && _REAL.GLOBAL_CXC_VENCIDOS) ? _REAL.GLOBAL_CXC_VENCIDOS : {
      totalClientesVencidos: 54,
      totalMontoVencido: 162464.07,
      totalDocsVencidos: 179,
      desglosePorVendedor: {},
      clientesVencidosList: [],
      comprobantesVencidosList: []
    };
    const LINDA_B2C_FULL_HISTORY = (_REAL && _REAL.LINDA_B2C_FULL_HISTORY) ? _REAL.LINDA_B2C_FULL_HISTORY : [];"""

    if real_decl in html and "const GLOBAL_CXC_VENCIDOS" not in html:
        html = html.replace(real_decl, target_vars, 1)
        print("[OK] Constantes GLOBAL_CXC_VENCIDOS y LINDA_B2C_FULL_HISTORY insertadas en JS.")

    # 2. Insertar Modal #global-cxc-modal antes de <!-- ==================== JAVASCRIPT ==================== -->
    modal_html = """  <!-- MODAL GLOBAL DE DEUDA VENCIDA (T025) -->
  <div id="global-cxc-modal" class="modal-overlay hidden" style="position: fixed; inset: 0; background: rgba(15,23,42,0.7); display: flex; align-items: center; justify-content: center; z-index: 9999; padding: 16px;">
    <div class="modal-content" style="background: white; border-radius: 16px; max-width: 1060px; width: 100%; max-height: 92vh; display: flex; flex-direction: column; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.35); overflow: hidden; border: 1px solid #e2e8f0;">
      
      <!-- HEADER -->
      <div style="padding: 16px 24px; border-bottom: 1px solid #fecdd3; display: flex; justify-content: space-between; align-items: center; background: #fff1f2;">
        <div>
          <h3 style="margin: 0; font-size: 17px; font-weight: 800; color: #991b1b; display: flex; align-items: center; gap: 8px;">
            <span>🚨</span> Detalle Global de Deuda Vencida — Qali Kay S.A.C.
          </h3>
          <p style="margin: 4px 0 0 0; font-size: 12px; color: #9f1239;">
            Total Exigible: <strong id="global-cxc-modal-total">S/ 162,464.07</strong> en <strong id="global-cxc-modal-docs">179 comprobantes</strong> de <strong id="global-cxc-modal-clients">54 clientes</strong> · Fuente Oficial: <code>Cuentas por cobrar 2026.xlsx</code>
          </p>
        </div>
        <button onclick="closeGlobalCxcModal()" style="background: none; border: none; font-size: 22px; cursor: pointer; color: #64748b; line-height: 1; padding: 4px 8px; border-radius: 6px;" title="Cerrar modal">✕</button>
      </div>

      <!-- DESGLOSE POR VENDEDOR -->
      <div style="padding: 12px 24px; background: #f8fafc; border-bottom: 1px solid #e2e8f0;">
        <div style="font-size: 11px; font-weight: 700; color: #475569; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px;">Resumen por Cartera Comercial (Clic para filtrar):</div>
        <div id="global-cxc-seller-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px;">
          <!-- Rendered by JS -->
        </div>
      </div>

      <!-- CONTROLES Y FILTROS -->
      <div style="padding: 12px 24px; border-bottom: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; background: white;">
        <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
          <span style="font-size: 12px; font-weight: 700; color: #475569;">Vista:</span>
          <button onclick="setGlobalCxcView('clients')" id="btn-gcxc-view-clients" class="pill-btn active" style="font-size: 12px; padding: 4px 12px;">👥 Por Cliente</button>
          <button onclick="setGlobalCxcView('docs')" id="btn-gcxc-view-docs" class="pill-btn" style="font-size: 12px; padding: 4px 12px;">📄 Por Comprobante</button>
          
          <span style="font-size: 12px; font-weight: 700; color: #475569; margin-left: 6px;">Vendedor:</span>
          <select id="gcxc-seller-select" onchange="renderGlobalCxcView()" style="padding: 4px 8px; border-radius: 6px; border: 1px solid #cbd5e1; font-size: 12px; background: white; font-weight: 600;">
            <option value="ALL">Todos los Vendedores</option>
            <option value="cristian">Cristian Gutiérrez</option>
            <option value="walter">Walter Gutiérrez</option>
            <option value="enrique">Enrique García</option>
            <option value="carlos">Carlos Cuadros</option>
            <option value="zully-b2c">Linda B2C</option>
            <option value="zully-b2b">Linda B2B</option>
          </select>
        </div>

        <button onclick="downloadGlobalCxcExcel()" style="background: #10b981; color: white; border: none; padding: 6px 14px; border-radius: 8px; font-size: 12px; font-weight: 700; cursor: pointer; display: flex; align-items: center; gap: 6px; box-shadow: 0 1px 2px rgba(0,0,0,0.05);" title="Descargar detalle consolidado de deuda vencida en 2 hojas Excel">
          📥 Descargar Excel Deuda Vencida Qali Kay (.xlsx)
        </button>
      </div>

      <!-- TABLA RESULTADOS -->
      <div style="padding: 0 24px; overflow-y: auto; flex: 1; max-height: calc(92vh - 270px);">
        <table id="global-cxc-table" style="width: 100%; border-collapse: collapse; font-size: 12px; text-align: left;">
          <thead id="global-cxc-thead" style="position: sticky; top: 0; background: #f8fafc; z-index: 2;">
            <!-- Rendered by JS -->
          </thead>
          <tbody id="global-cxc-tbody">
            <!-- Rendered by JS -->
          </tbody>
        </table>
      </div>

      <!-- FOOTER -->
      <div style="padding: 10px 24px; border-top: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center; background: #f8fafc;">
        <span id="global-cxc-table-count" style="font-size: 12px; color: #64748b; font-weight: 600;">Cargando clientes...</span>
        <button onclick="closeGlobalCxcModal()" style="padding: 6px 16px; border: 1px solid #cbd5e1; background: white; border-radius: 6px; font-size: 12px; cursor: pointer; font-weight: 600;">Cerrar</button>
      </div>

    </div>
  </div>\n\n"""

    marker_js = "<!-- ==================== JAVASCRIPT ==================== -->"
    if marker_js in html and "id=\"global-cxc-modal\"" not in html:
        html = html.replace(marker_js, modal_html + marker_js, 1)
        print("[OK] Modal #global-cxc-modal insertado.")

    # 3. Actualizar filterFeed para soportar DEUDA_VENCIDA
    old_ff_keys = "['ALL', 'Cristian', 'Enrique', 'Carlos C', 'Walter', 'Linda B2B', 'Linda B2C', 'B2C_VENCIDOS']"
    new_ff_keys = "['ALL', 'Cristian', 'Enrique', 'Carlos C', 'Walter', 'Linda B2B', 'Linda B2C', 'B2C_VENCIDOS', 'DEUDA_VENCIDA']"
    if old_ff_keys in html:
        html = html.replace(old_ff_keys, new_ff_keys)
        print("[OK] filterFeed keys actualizado con DEUDA_VENCIDA.")

    old_ff_cond = "btn.className = key === 'B2C_VENCIDOS' ? 'pill-btn danger active' : 'pill-btn active';"
    new_ff_cond = "btn.className = (key === 'B2C_VENCIDOS' || key === 'DEUDA_VENCIDA') ? 'pill-btn danger active' : 'pill-btn active';"
    if old_ff_cond in html:
        html = html.replace(old_ff_cond, new_ff_cond)

    old_ff_cond2 = "btn.className = key === 'B2C_VENCIDOS' ? 'pill-btn danger' : 'pill-btn';"
    new_ff_cond2 = "btn.className = (key === 'B2C_VENCIDOS' || key === 'DEUDA_VENCIDA') ? 'pill-btn danger' : 'pill-btn';"
    if old_ff_cond2 in html:
        html = html.replace(old_ff_cond2, new_ff_cond2)

    # 4. Actualizar renderActionCards y renderTableRows con filtro DEUDA_VENCIDA
    cards_filter_old = """      if (filter === 'B2C_VENCIDOS') {
        list = CLIENTS.filter(c => isClientOverdueTotal(c));
      } else if (filter !== 'ALL') {"""
    cards_filter_new = """      if (filter === 'B2C_VENCIDOS') {
        list = CLIENTS.filter(c => isClientOverdueTotal(c));
      } else if (filter === 'DEUDA_VENCIDA') {
        list = CLIENTS.filter(c => c.cxcIsDebt);
      } else if (filter !== 'ALL') {"""
    if cards_filter_old in html:
        html = html.replace(cards_filter_old, cards_filter_new)
        print("[OK] renderActionCards y renderTableRows actualizados para DEUDA_VENCIDA.")

    # 5. Insertar funciones JS de la Fase 6 antes de applyRealDataToDom
    js_functions = """    // =========================================================================
    // FASE 6 (T025 & T026): FUNCIONES DEL MODAL DEUDA VENCIDA Y EXCEL EXPORTS
    // =========================================================================
    let currentGlobalCxcView = 'clients'; // 'clients' | 'docs'

    function openGlobalCxcModal() {
      const modal = document.getElementById('global-cxc-modal');
      if (!modal) return;
      modal.classList.remove('hidden');
      document.body.style.overflow = 'hidden';

      const elTot = document.getElementById('global-cxc-modal-total');
      if (elTot) elTot.textContent = `S/ ${fmtNum(GLOBAL_CXC_VENCIDOS.totalMontoVencido)}`;
      const elDocs = document.getElementById('global-cxc-modal-docs');
      if (elDocs) elDocs.textContent = `${GLOBAL_CXC_VENCIDOS.totalDocsVencidos} comprobantes`;
      const elCli = document.getElementById('global-cxc-modal-clients');
      if (elCli) elCli.textContent = `${GLOBAL_CXC_VENCIDOS.totalClientesVencidos} clientes`;

      renderGlobalCxcSellerGrid();
      renderGlobalCxcView();
    }

    function closeGlobalCxcModal() {
      const modal = document.getElementById('global-cxc-modal');
      if (!modal) return;
      modal.classList.add('hidden');
      document.body.style.overflow = '';
    }

    function setGlobalCxcView(viewMode) {
      currentGlobalCxcView = viewMode;
      const btnCli = document.getElementById('btn-gcxc-view-clients');
      const btnDocs = document.getElementById('btn-gcxc-view-docs');
      if (btnCli && btnDocs) {
        if (viewMode === 'clients') {
          btnCli.className = 'pill-btn active';
          btnDocs.className = 'pill-btn';
        } else {
          btnCli.className = 'pill-btn';
          btnDocs.className = 'pill-btn active';
        }
      }
      renderGlobalCxcView();
    }

    function renderGlobalCxcSellerGrid() {
      const grid = document.getElementById('global-cxc-seller-grid');
      if (!grid) return;
      const desglose = GLOBAL_CXC_VENCIDOS.desglosePorVendedor || {};
      let html = '';
      const sellerOrder = ['cristian', 'walter', 'enrique', 'carlos', 'zully-b2c', 'zully-b2b'];
      sellerOrder.forEach(sId => {
        const item = desglose[sId] || { sellerShort: sId, docsCount: 0, clientesCount: 0, montoVencido: 0 };
        const hasDebt = item.montoVencido > 0;
        const color = hasDebt ? '#dc2626' : '#059669';
        const bg = hasDebt ? '#fff1f2' : '#f0fdf4';
        const border = hasDebt ? '#fecdd3' : '#bbf7d0';
        html += `
          <div style="background: ${bg}; border: 1px solid ${border}; border-radius: 8px; padding: 8px 12px; cursor: pointer; transition: all 0.15s ease;" onclick="document.getElementById('gcxc-seller-select').value='${sId}'; renderGlobalCxcView();" title="Filtrar por ${item.sellerShort}">
            <div style="font-size: 11px; font-weight: 700; color: #475569;">${item.sellerShort || sId}</div>
            <div style="font-size: 14px; font-weight: 800; color: ${color}; font-family: monospace; margin: 2px 0;">S/ ${fmtNum(item.montoVencido)}</div>
            <div style="font-size: 10px; color: #64748b;">${item.clientesCount} cli · ${item.docsCount} docs</div>
          </div>
        `;
      });
      grid.innerHTML = html;
    }

    function renderGlobalCxcView() {
      const thead = document.getElementById('global-cxc-thead');
      const tbody = document.getElementById('global-cxc-tbody');
      const countEl = document.getElementById('global-cxc-table-count');
      const selSeller = document.getElementById('gcxc-seller-select') ? document.getElementById('gcxc-seller-select').value : 'ALL';

      if (!thead || !tbody) return;

      if (currentGlobalCxcView === 'clients') {
        thead.innerHTML = `
          <tr style="border-bottom: 2px solid #cbd5e1; color: #334155;">
            <th style="padding: 10px 8px;">RUC</th>
            <th style="padding: 10px 8px;">Cliente / Comercial</th>
            <th style="padding: 10px 8px;">Vendedor</th>
            <th style="padding: 10px 8px; text-align: center;">Docs Venc.</th>
            <th style="padding: 10px 8px; text-align: center;">Máx Mora</th>
            <th style="padding: 10px 8px; text-align: right;">Monto Vencido</th>
          </tr>
        `;
        let list = GLOBAL_CXC_VENCIDOS.clientesVencidosList || [];
        if (selSeller !== 'ALL') {
          list = list.filter(c => c.sellerId === selSeller);
        }
        if (countEl) countEl.textContent = `Mostrando ${list.length} clientes con deuda vencida`;
        tbody.innerHTML = list.map(c => `
          <tr style="border-bottom: 1px solid #f1f5f9;">
            <td style="padding: 8px; font-family: monospace; font-size: 11px;">${c.ruc}</td>
            <td style="padding: 8px;">
              <strong>${c.comercial || c.cliente}</strong>
              <div style="font-size: 10px; color: #64748b;">${c.cliente}</div>
            </td>
            <td style="padding: 8px;">
              <span class="badge-pill" style="background: #f1f5f9; color: #334155; font-size: 10px; padding: 2px 6px;">${c.vendedor}</span>
            </td>
            <td style="padding: 8px; text-align: center; font-weight: 700;">${c.docsCount}</td>
            <td style="padding: 8px; text-align: center;">
              <span style="color: ${c.maxDiasMora > 60 ? '#dc2626' : '#b45309'}; font-weight: 700;">${c.maxDiasMora}d</span>
            </td>
            <td style="padding: 8px; text-align: right; font-weight: 800; color: #dc2626; font-family: monospace;">
              S/ ${fmtNum(c.montoVencido)}
            </td>
          </tr>
        `).join('') || `<tr><td colspan="6" style="padding: 24px; text-align: center; color: #64748b;">Sin clientes con deuda vencida para este filtro.</td></tr>`;
      } else {
        thead.innerHTML = `
          <tr style="border-bottom: 2px solid #cbd5e1; color: #334155;">
            <th style="padding: 10px 8px;">Comprobante</th>
            <th style="padding: 10px 8px;">Tipo</th>
            <th style="padding: 10px 8px;">RUC</th>
            <th style="padding: 10px 8px;">Cliente</th>
            <th style="padding: 10px 8px;">Vendedor</th>
            <th style="padding: 10px 8px; text-align: center;">F. Emisión</th>
            <th style="padding: 10px 8px; text-align: center;">F. Venc.</th>
            <th style="padding: 10px 8px; text-align: center;">Días Mora</th>
            <th style="padding: 10px 8px; text-align: right;">Total Doc</th>
            <th style="padding: 10px 8px; text-align: right;">Saldo Vencido</th>
          </tr>
        `;
        let list = GLOBAL_CXC_VENCIDOS.comprobantesVencidosList || [];
        if (selSeller !== 'ALL') {
          list = list.filter(d => d.sellerId === selSeller);
        }
        if (countEl) countEl.textContent = `Mostrando ${list.length} comprobantes vencidos`;
        tbody.innerHTML = list.map(d => `
          <tr style="border-bottom: 1px solid #f1f5f9;">
            <td style="padding: 8px; font-family: monospace; font-size: 11px; font-weight: 700;">${d.nroDoc}</td>
            <td style="padding: 8px; font-size: 11px;">${d.tipoDoc}</td>
            <td style="padding: 8px; font-family: monospace; font-size: 11px;">${d.ruc}</td>
            <td style="padding: 8px; font-size: 11px;">${d.comercial || d.cliente}</td>
            <td style="padding: 8px;">
              <span class="badge-pill" style="background: #f1f5f9; color: #334155; font-size: 10px; padding: 2px 6px;">${d.vendedor}</span>
            </td>
            <td style="padding: 8px; text-align: center; font-size: 11px;">${d.fechaEmision}</td>
            <td style="padding: 8px; text-align: center; font-size: 11px;">${d.fechaVenc}</td>
            <td style="padding: 8px; text-align: center; font-weight: 700; color: ${d.diasMora > 60 ? '#dc2626' : '#b45309'};">${d.diasMora}d</td>
            <td style="padding: 8px; text-align: right; font-family: monospace; font-size: 11px;">S/ ${fmtNum(d.total)}</td>
            <td style="padding: 8px; text-align: right; font-weight: 800; color: #dc2626; font-family: monospace; font-size: 11px;">S/ ${fmtNum(d.saldo)}</td>
          </tr>
        `).join('') || `<tr><td colspan="10" style="padding: 24px; text-align: center; color: #64748b;">Sin comprobantes para este filtro.</td></tr>`;
      }
    }

    function downloadGlobalCxcExcel() {
      if (typeof XLSX === 'undefined') {
        alert('SheetJS (XLSX) no está disponible en este momento.');
        return;
      }
      const clientsData = (GLOBAL_CXC_VENCIDOS.clientesVencidosList || []).map(c => ({
        'RUC': c.ruc,
        'Razón Social': c.cliente,
        'Nombre Comercial': c.comercial,
        'Vendedor Asignado': c.vendedor,
        'Facturas Vencidas': c.docsCount,
        'Máximo Días Mora': c.maxDiasMora,
        'Monto Vencido (S/)': c.montoVencido
      }));

      const docsData = (GLOBAL_CXC_VENCIDOS.comprobantesVencidosList || []).map(d => ({
        'Nro Comprobante': d.nroDoc,
        'Tipo Documento': d.tipoDoc,
        'RUC': d.ruc,
        'Cliente': d.cliente,
        'Nombre Comercial': d.comercial,
        'Vendedor': d.vendedor,
        'Fecha Emisión': d.fechaEmision,
        'Fecha Vencimiento': d.fechaVenc,
        'Días de Mora': d.diasMora,
        'Total Comprobante (S/)': d.total,
        'Saldo Vencido (S/)': d.saldo
      }));

      const wb = XLSX.utils.book_new();
      const ws1 = XLSX.utils.json_to_sheet(clientsData);
      const ws2 = XLSX.utils.json_to_sheet(docsData);
      XLSX.utils.book_append_sheet(wb, ws1, "Resumen por Cliente");
      XLSX.utils.book_append_sheet(wb, ws2, "Detalle Comprobantes");
      XLSX.writeFile(wb, "Deuda_Vencida_QaliKay_2026.xlsx");
    }

    function downloadLindaB2cFullExcel() {
      if (typeof XLSX === 'undefined') {
        alert('SheetJS (XLSX) no está disponible en este momento.');
        return;
      }
      const data = (LINDA_B2C_FULL_HISTORY || []).map(c => ({
        'RUC': c.ruc,
        'Nombre Cliente': c.nombre,
        'Nombre Comercial': c.comercial,
        'Contacto': c.contacto,
        'Celular': c.celular,
        'Distrito': c.distrito,
        'Canal': c.canal,
        'Compras Históricas': c.cantCompras,
        'Es Recurrente': c.esRecurrente ? 'SÍ' : 'NO',
        'Última Fecha Compra': c.ultimaFecha,
        'Días Sin Compra': c.diasInactivo,
        'Ciclo Habitual (días)': c.cicloHabitual,
        'Ticket Promedio (S/)': c.ticketPromedio,
        'Último Ticket (S/)': c.ultimoTicket,
        'Deuda Vencida (S/)': c.deudaVencida,
        'Deuda Total (S/)': c.deudaTotal,
        'Docs Vencidos': c.docsVencidos,
        'Máx Días Mora': c.diasMoraMax,
        'Severidad': c.severidad,
        'Alerta': c.alerta || c.textoAlerta,
        'Top 3 Productos Canasta': c.topProductos,
        'Promoción Activa': c.promocionActiva
      }));

      const wb = XLSX.utils.book_new();
      const ws = XLSX.utils.json_to_sheet(data);
      XLSX.utils.book_append_sheet(wb, ws, "Histórico Linda B2C");
      XLSX.writeFile(wb, "Historico_Total_Linda_B2C_QaliKay.xlsx");
    }

    function downloadSellerCxcExcel(sellerId) {
      if (typeof XLSX === 'undefined') {
        alert('SheetJS (XLSX) no está disponible en este momento.');
        return;
      }
      const s = SELLER_DRILLDOWN_DETAILS[sellerId] || SELLER_DRILLDOWN_DETAILS['enrique'];
      const docs = (s && s.cxcDetalle) ? s.cxcDetalle : [];
      const data = docs.map(d => ({
        'Comprobante': d.nroDoc,
        'Tipo Documento': d.tipoDoc,
        'RUC': d.ruc,
        'Cliente': d.cliente,
        'Nombre Comercial': d.comercial,
        'Fecha Emisión': d.fechaEmision,
        'Fecha Vencimiento': d.fechaVenc,
        'Días Mora': d.diasMora,
        'Estado': d.estado,
        'Total Comprobante (S/)': d.total,
        'Saldo Pendiente (S/)': d.saldo
      }));

      const wb = XLSX.utils.book_new();
      const ws = XLSX.utils.json_to_sheet(data);
      const sheetName = (s && s.nombre) ? s.nombre.substring(0, 31).replace(/[:\\\\/\\?\\*\\[\\]]/g, '') : 'CxC Vendedor';
      XLSX.utils.book_append_sheet(wb, ws, sheetName);
      XLSX.writeFile(wb, `CxC_${sellerId}_QaliKay.xlsx`);
    }\n\n"""

    marker_apply = "function applyRealDataToDom() {"
    if marker_apply in html and "function openGlobalCxcModal" not in html:
        html = html.replace(marker_apply, js_functions + marker_apply, 1)
        print("[OK] Funciones JS de Fase 6 insertadas.")

    # 6. Actualizar applyRealDataToDom para setear Card 4 y botones con deuda vencida
    target_apply_end = """      // 3. Tarjeta 4 del HUD Ejecutivo: Clientes con Deuda Vencida (Qali Kay)
      const elValCxcGlobal = document.getElementById('hud-val-cxc-global');
      if (elValCxcGlobal) {
        elValCxcGlobal.textContent = `${GLOBAL_CXC_VENCIDOS.totalClientesVencidos} Clientes`;
      }
      const elSubCxcGlobal = document.getElementById('hud-sub-cxc-global');
      if (elSubCxcGlobal) {
        elSubCxcGlobal.textContent = `S/ ${fmtNum(GLOBAL_CXC_VENCIDOS.totalMontoVencido)} vencidos (${GLOBAL_CXC_VENCIDOS.totalDocsVencidos} docs)`;
      }

      // Alertas Críticas & Conteo de Cartera
      const cntCriticas = CLIENTS.filter(c => c.alertaClass === 'urgent').length;
      const cntDeudas = CLIENTS.filter(c => c.cxcIsDebt).length;
      const elCrit = document.getElementById('hud-val-criticas');
      if (elCrit) elCrit.textContent = `${cntCriticas.toLocaleString('es-PE')} Clientes`;
      const elSubCrit = document.getElementById('hud-sub-criticas');
      if (elSubCrit) elSubCrit.textContent = `${cntDeudas} con deuda vencida CxC`;

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
      if (bB2C) bB2C.textContent = `👤 Linda B2C 90d (${cntLindaB2C})`;
      const bDebt = document.getElementById('btn-feed-DEUDA_VENCIDA');
      if (bDebt) bDebt.textContent = `🚨 Clientes con Deuda Vencida (${cntDeudas})`;
      const bLindaFull = document.getElementById('btn-download-linda-b2c');
      if (bLindaFull) bLindaFull.innerHTML = `📥 Descargar Excel Histórico Total Linda B2C (${LINDA_B2C_FULL_HISTORY.length} Clientes)`;"""

    old_apply_section = """      // 3. Alertas Críticas & Clientes Vencidos del Total de la Cartera Qali Kay (Punto #4)
      const cntCriticas = CLIENTS.filter(c => c.alertaClass === 'urgent').length;
      const cntDeudas = CLIENTS.filter(c => c.cxcIsDebt).length;
      const vencidosTotalList = CLIENTS.filter(c => isClientOverdueTotal(c));
      const cntVencidosTotal = vencidosTotalList.length;
      const cntVencidosB2B = vencidosTotalList.filter(c => c.vendedor !== 'Linda B2C').length;
      const cntVencidosB2C = vencidosTotalList.filter(c => c.vendedor === 'Linda B2C').length;
      
      const elCrit = document.getElementById('hud-val-criticas');
      if (elCrit) elCrit.textContent = `${cntCriticas.toLocaleString('es-PE')} Clientes`;
      const elSubCrit = document.getElementById('hud-sub-criticas');
      if (elSubCrit) elSubCrit.textContent = `${cntDeudas} con deuda vencida CxC`;
      const elB2c = document.getElementById('hud-val-b2c');
      if (elB2c) elB2c.textContent = `${cntVencidosTotal.toLocaleString('es-PE')} Clientes`;
      const elSubB2c = document.getElementById('hud-sub-b2c');
      if (elSubB2c) elSubB2c.textContent = `${cntVencidosB2B} B2B + ${cntVencidosB2C} B2C vencidos`;
      
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
      if (bB2CV) bB2CV.textContent = `🚨 Clientes Vencidos Qali Kay (${cntVencidosTotal})`;"""

    if old_apply_section in html:
        html = html.replace(old_apply_section, target_apply_end)
        print("[OK] applyRealDataToDom actualizado con bindings de Card 4 y contadores.")

    HTML_PATH.write_text(html, encoding="utf-8")
    print("[SUCCESS] HTML actualizado exitosamente con la UI de Fase 6.")

if __name__ == "__main__":
    apply_phase6_ui()
