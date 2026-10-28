"""
Script de Verificación de Integridad Matemática y Operativa de la Fase 6 (T023 a T027)
Sistema de Inteligencia Comercial - Qali Kay S.A.C.
Framework Spec-Kit: specs/001-dashboard-inteligencia-comercial/
"""

import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import pandas as pd

def verify_phase6():
    print("=" * 80)
    print("INICIANDO AUDITORIA DE INTEGRIDAD MATEMATICA Y OPERATIVA - FASE 6")
    print("=" * 80)
    
    errors = []
    
    # --------------------------------------------------------------------------
    # 1. VERIFICACION T023: MOTOR DE REGLAS DE CARTERAS
    # --------------------------------------------------------------------------
    print("\n[1/4] Verificando Reglas de Clasificacion y Recompra en motor_reglas_carteras.py...")
    try:
        from src.motor_reglas_carteras import (
            determine_client_cartera_owner,
            generate_smart_repurchase_recommendation,
            FALLBACK_STAR_SKUS
        )
        
        # Test 1A: Clasificacion estricta Nro_Doc > 400
        # Cliente con RUC 20 pero todas sus compras <= 400 -> DEBE SER zully-b2c
        dummy_df_b2c = pd.DataFrame([
            {"Nro_Doc": "B001-1", "Total_Detalle": 150.0, "Fecha": "2026-10-01", "Nombre_Vendedor": "Rep. Comercial"},
            {"Nro_Doc": "B001-2", "Total_Detalle": 200.0, "Fecha": "2026-10-15", "Nombre_Vendedor": "Rep. Comercial"}
        ])
        owner_b2c = determine_client_cartera_owner(dummy_df_b2c, "20609999999", "EMPRESA PRUEBA SAC")
        assert owner_b2c == "zully-b2c", f"Esperado zully-b2c para compras <= 400, obtenido {owner_b2c}"
        
        # Cliente con compra individual > 400 -> DEBE SER zully-b2b
        dummy_df_b2b = pd.DataFrame([
            {"Nro_Doc": "F001-1", "Total_Detalle": 450.0, "Fecha": "2026-10-01", "Nombre_Vendedor": "Zully Rios"}
        ])
        owner_b2b = determine_client_cartera_owner(dummy_df_b2b, "10485171680", "PERSONA NATURAL")
        assert owner_b2b == "zully-b2b", f"Esperado zully-b2b para doc > 400, obtenido {owner_b2b}"
        print("      * [OK] Clasificacion B2B vs B2C por Nro_Doc > 400 verificada.")
        
        # Test 1B: Garantia de 3 productos recomendados en canasta habitual
        dummy_sales_1_sku = pd.DataFrame([
            {"Cod_Producto": "ORD-502", "Desc_Producto": "Citrato de Potasio caps", "Proveedor_Titular": "NUTRIVAS", "Cantidad": 5, "Total_Detalle": 250.0, "Fecha": "2026-10-01"}
        ])
        recompra = generate_smart_repurchase_recommendation(
            client_df=dummy_sales_1_sku,
            client_name="Dietética San Pedro",
            contact_info={"nombre_comercial": "Dietética San Pedro", "contacto": "María", "celular": "999888777"},
            kardex_inventory={"ORD-502": {"stock": 10.0, "costo": 15.0}, "NAN-004": {"stock": 50.0, "costo": 20.0}},
            promociones=[],
            vendedor_cartera="enrique-garcia"
        )
        
        items_c = recompra["items_canasta"]
        assert len(items_c) == 3, f"Esperado exactamente 3 productos recomendados, obtenido {len(items_c)}"
        wa_text = recompra["whatsapp_copy"]
        bullet_count = wa_text.count("• *")
        assert bullet_count == 3, f"Esperado exactamente 3 viñetas en whatsapp_copy, obtenido {bullet_count}"
        print(f"      * [OK] Garantia de 3 productos y 3 viñetas WhatsApp verificada.")
        
    except Exception as e:
        errors.append(f"Fallo en verificacion de T023: {e}")
        print(f"      * [FAIL] T023 error: {e}")
        
    # --------------------------------------------------------------------------
    # 2. VERIFICACION T024: DATOS EXPORTADOS EN JSON
    # --------------------------------------------------------------------------
    print("\n[2/4] Verificando Estructuras Exportadas en data/datos_comerciales.json...")
    json_path = Path("data/datos_comerciales.json")
    if not json_path.exists():
        errors.append("data/datos_comerciales.json no existe.")
    else:
        with open(json_path, encoding="utf-8") as f:
            data = json.load(f)
            
        cxc_glob = data.get("GLOBAL_CXC_VENCIDOS", {})
        assert "totalClientesVencidos" in cxc_glob, "GLOBAL_CXC_VENCIDOS sin totalClientesVencidos"
        assert "totalMontoVencido" in cxc_glob, "GLOBAL_CXC_VENCIDOS sin totalMontoVencido"
        assert "totalDocsVencidos" in cxc_glob, "GLOBAL_CXC_VENCIDOS sin totalDocsVencidos"
        assert "desglosePorVendedor" in cxc_glob, "GLOBAL_CXC_VENCIDOS sin desglosePorVendedor"
        assert "clientesVencidosList" in cxc_glob, "GLOBAL_CXC_VENCIDOS sin clientesVencidosList"
        assert "comprobantesVencidosList" in cxc_glob, "GLOBAL_CXC_VENCIDOS sin comprobantesVencidosList"
        
        monto_venc = cxc_glob["totalMontoVencido"]
        docs_venc = cxc_glob["totalDocsVencidos"]
        cli_venc = cxc_glob["totalClientesVencidos"]
        assert abs(monto_venc - 162464.07) < 1.0, f"Monto vencido {monto_venc} difiere de S/ 162,464.07"
        assert docs_venc == 179, f"Docs vencidos {docs_venc} difiere de 179"
        assert cli_venc == 54, f"Clientes vencidos {cli_venc} difiere de 54"
        print(f"      * [OK] GLOBAL_CXC_VENCIDOS: S/ {monto_venc:,.2f} en {docs_venc} docs de {cli_venc} clientes.")
        
        b2c_full = data.get("LINDA_B2C_FULL_HISTORY", [])
        assert len(b2c_full) == 877, f"LINDA_B2C_FULL_HISTORY count {len(b2c_full)} difiere de 877"
        print(f"      * [OK] LINDA_B2C_FULL_HISTORY: {len(b2c_full)} clientes exportados para descarga Excel.")
        
        feed_clients = data.get("CLIENTS", [])
        b2c_feed = [c for c in feed_clients if c.get("vendedor") == "Linda B2C"]
        assert len(b2c_feed) <= 70, f"Clientes de Linda B2C en Feed exceden 70 ({len(b2c_feed)})"
        for c in b2c_feed:
            assert c["diasSinCompra"] <= 90, f"Cliente {c['nombre']} en Feed B2C con >90d ({c['diasSinCompra']}d)"
        print(f"      * [OK] Feed visible Linda B2C: {len(b2c_feed)} clientes accionables (<= 90d con inactividad/deuda).")
        
        # Verificar que agendas WA tengan 3 productos sugeridos
        wa_agendas = data.get("WA_AGENDAS", {})
        assert len(wa_agendas) == 6, f"WA_AGENDAS debe contener 6 carteras, tiene {len(wa_agendas)}"
        print(f"      * [OK] WA_AGENDAS: 6 carteras generadas.")

        # Test T029: Inactivos por vendedor en SELLER_DRILLDOWN_DETAILS
        print("\n[T029] Verificando inactivosDetalle en SELLER_DRILLDOWN_DETAILS...")
        sellers_dd = data.get("SELLER_DRILLDOWN_DETAILS", {})
        assert len(sellers_dd) == 6, f"SELLER_DRILLDOWN_DETAILS debe tener 6 vendedores, tiene {len(sellers_dd)}"
        
        total_inact_empresa = 0
        total_una_empresa = 0
        expected_fields = {
            "ruc", "cliente", "comercial", "contacto", "celular", "distrito",
            "cantCompras", "esUnaCompra", "tipoInactividad", "ultimaCompra",
            "diasSinCompra", "cicloHabitual", "ticketPromedio", "ultimoTicket",
            "deudaVencida", "top3Productos"
        }
        
        for sid, sdata in sellers_dd.items():
            assert "inactivosDetalle" in sdata, f"Vendedor {sid} no tiene inactivosDetalle"
            assert "inactivosTotalCount" in sdata, f"Vendedor {sid} no tiene inactivosTotalCount"
            assert "inactivosUnaCompraCount" in sdata, f"Vendedor {sid} no tiene inactivosUnaCompraCount"
            
            inacts = sdata["inactivosDetalle"]
            tot_cnt = sdata["inactivosTotalCount"]
            una_cnt = sdata["inactivosUnaCompraCount"]
            
            assert len(inacts) == tot_cnt, f"{sid}: len(inactivosDetalle)={len(inacts)} != inactivosTotalCount={tot_cnt}"
            assert sum(1 for x in inacts if x["esUnaCompra"]) == una_cnt, f"{sid}: conteo esUnaCompra no coincide con una_cnt"
            
            # Verificar orden descendente por ticketPromedio
            tickets = [x["ticketPromedio"] for x in inacts]
            assert tickets == sorted(tickets, reverse=True), f"{sid}: inactivosDetalle no está ordenado por ticketPromedio descendente"
            
            # Verificar campos de cada registro
            for rec in inacts:
                assert expected_fields.issubset(rec.keys()), f"{sid}: registro sin campos requeridos: {expected_fields - set(rec.keys())}"
                assert rec["diasSinCompra"] > 60, f"{sid}: cliente con diasSinCompra <= 60 ({rec['diasSinCompra']})"
                if rec["esUnaCompra"]:
                    assert rec["tipoInactividad"] == "1 Sola Compra (>2M)"
                else:
                    assert rec["tipoInactividad"] == "Recurrente Inactivo (>2M)"
                    
            total_inact_empresa += tot_cnt
            total_una_empresa += una_cnt
            print(f"      * [OK] {sid:10}: {tot_cnt:3} inactivos ({una_cnt:3} una compra, {tot_cnt - una_cnt:3} recurrentes).")
            
        print(f"      * [OK] Total Inactivos Empresa (>60d): {total_inact_empresa} ({total_una_empresa} una compra, {total_inact_empresa - total_una_empresa} recurrentes).")
        
    # --------------------------------------------------------------------------
    # 3. VERIFICACION T025, T026 & T029: COMPONENTES EN EL DASHBOARD HTML
    # --------------------------------------------------------------------------
    print("\n[3/4] Verificando Componentes y Scripts en PROTOTIPO_DASHBOARD_VENTAS_QALIKAY.html...")
    html_path = Path("ejecucion/PROTOTIPO_DASHBOARD_VENTAS_QALIKAY.html")
    html = html_path.read_text(encoding="utf-8")
    
    checks = [
        ("hud-card-cxc-global", "Tarjeta 4 HUD Clientes con Deuda Vencida"),
        ("openGlobalCxcModal()", "Handler de apertura del modal de Deuda Vencida"),
        ("id=\"global-cxc-modal\"", "Modal de Deuda Vencida #global-cxc-modal"),
        ("downloadGlobalCxcExcel()", "Funcion downloadGlobalCxcExcel"),
        ("downloadLindaB2cFullExcel()", "Funcion downloadLindaB2cFullExcel"),
        ("downloadSellerCxcExcel", "Funcion downloadSellerCxcExcel en Tab 1"),
        ("btn-feed-DEUDA_VENCIDA", "Boton de filtro Clientes con Deuda Vencida en Feed"),
        ("btn-download-linda-b2c", "Boton de descarga Excel Linda B2C en Feed"),
        ("GLOBAL_CXC_VENCIDOS", "Constante GLOBAL_CXC_VENCIDOS en JS"),
        ("LINDA_B2C_FULL_HISTORY", "Constante LINDA_B2C_FULL_HISTORY en JS"),
        ("xlsx.full.min.js", "Carga de libreria SheetJS"),
        # T029 UI checks
        ("id=\"seller-inactivos-detail-panel\"", "Panel colapsable #seller-inactivos-detail-panel"),
        ("toggleSellerInactiveDetail", "Funcion toggleSellerInactiveDetail()"),
        ("filterSellerInactives", "Funcion filterSellerInactives()"),
        ("downloadSellerInactiveExcel", "Funcion downloadSellerInactiveExcel()"),
        ("downloadAllSellersInactiveExcel", "Funcion downloadAllSellersInactiveExcel()"),
        ("onclick=\"downloadAllSellersInactiveExcel()\"", "Boton downloadAllSellersInactiveExcel en Toolbar"),
        ("toggleSellerInactiveDetail('UNA_COMPRA')", "Celda clickable una2m en renderSellerMatrix"),
        ("toggleSellerInactiveDetail('ALL')", "Celda clickable sin2m en renderSellerMatrix"),
        ("seller-inactivos-tbody", "Tabla tbody seller-inactivos-tbody")
    ]
    
    for needle, desc in checks:
        if needle in html:
            print(f"      * [OK] {desc} presente.")
        else:
            errors.append(f"No se encontro {desc} ('{needle}') en el HTML.")
            print(f"      * [FAIL] {desc} AUSENTE.")

    # --------------------------------------------------------------------------
    # 4. RESUMEN FINAL
    # --------------------------------------------------------------------------
    print("\n" + "=" * 80)
    if errors:
        print(f"[ERROR] Se encontraron {len(errors)} fallas de integridad en la Fase 6:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print("[SUCCESS] TODOS LOS CRITERIOS DE ACEPTACION DE LA FASE 6 (INCLUYENDO T029) SE CUMPLIERON AL 100%.")
        print("================================================================================")
        sys.exit(0)

if __name__ == "__main__":
    verify_phase6()

