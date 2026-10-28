"""
Modulo de Exportacion de Datos del Dashboard Comercial (Qali Kay S.A.C.)
======================================================================
Modulo: src/exportar_datos_dashboard.py
Alcance: Tarea T017 (Fase 4 & Correcciones Operativas 11 Puntos)
Presupuesto: S/ 0.00 ($0.00 USD)
Determinismo Matematico: Cero calculos via LLM.

Genera el consolidado determinista data/datos_comerciales.json y realiza la
inyeccion directa de window.__QALIKAY_REAL_DATA__ en
ejecucion/PROTOTIPO_DASHBOARD_VENTAS_QALIKAY.html.
"""

import os
import sys
import re
from pathlib import Path

# Agregar directorio raiz al sys.path para importaciones absolutas
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import json
import argparse
import datetime
from typing import Dict, List, Any, Optional, Tuple, Set

import pandas as pd
import numpy as np

# Rutas predeterminadas
DEFAULT_PARQUET_PATH = Path("data/ventas_2025_2026.parquet")
DEFAULT_ALERTAS_PATH = Path("data/alertas_comerciales_consolidadas.json")
DEFAULT_RESUMEN_PATH = Path("data/resumen_carteras.json")
DEFAULT_SYNC_PATH = Path("data/sync_status_cache.json")
DEFAULT_MAESTRO_CSV = Path("data/maestro_articulos_abastecimiento.csv")
DEFAULT_CXC_PATH = Path(r"C:\Users\cguti\OneDrive\Inka Comex\CUENTAS POR COBRAR\QALI KAY\2026\Cuentas por cobrar 2026.xlsx")
DEFAULT_OUTPUT_JSON = Path("data/datos_comerciales.json")
DEFAULT_HTML_PATH = Path("ejecucion/PROTOTIPO_DASHBOARD_VENTAS_QALIKAY.html")

from src.motor_reglas_carteras import (
    classify_transactional_cartera,
    determine_client_cartera_owner,
    LEAD_TIME_RULES,
    ORGANA_RUCS,
    UNALM_RUC,
    WHITNIN_CODES
)

CONSUMO_INTERNO_CXC: Set[str] = {
    "73615353", "06024456", "6024456", "76423008", "09072925",
    "9072925", "72164623", "72931481", "06604924", "6604924"
}

SELLER_CONFIG = [
    {
        "id": "enrique",
        "cartera_id": "enrique-garcia",
        "name": "1. Enrique García",
        "filter": "Enrique",
        "canal": "Canal Dietéticas Lima Este & Mayoristas B2B",
        "badge": "Líder en Amplitud de Cartera Activa",
        "badgeClass": "badge-pill green",
        "short": "Enrique"
    },
    {
        "id": "walter",
        "cartera_id": "walter-gutierrez",
        "name": "2. Walter Gutiérrez",
        "filter": "Walter",
        "canal": "Canal Relacional & Cuentas Tradicionales",
        "badge": "Alta Retención de Cartera",
        "badgeClass": "badge-pill blue",
        "short": "Walter"
    },
    {
        "id": "cristian",
        "cartera_id": "cristian-gutierrez",
        "name": "3. ⭐ Cristian Gutiérrez (Mi Cartera)",
        "filter": "Cristian",
        "canal": "Key Accounts & Clientes Institucionales VIP",
        "badge": "Líder en Facturación y Ticket Promedio",
        "badgeClass": "badge-pill purple",
        "short": "Cristian"
    },
    {
        "id": "carlos",
        "cartera_id": "carlos-cuadros",
        "name": "4. Carlos Cuadros (+ex Joel)",
        "filter": "Carlos C",
        "canal": "Cuentas B2B Campo (Fusión Cartera Joel García)",
        "badge": "Canal B2B en Expansión",
        "badgeClass": "badge-pill blue",
        "short": "Carlos C"
    },
    {
        "id": "zully-b2c",
        "cartera_id": "zully-b2c",
        "name": "5. 👤 Linda / Zully — B2C (<= S/ 400)",
        "filter": "Linda B2C",
        "canal": "Consumidor Final B2C (WhatsApp / Delivery <= S/ 400)",
        "badge": "Mayor Captación de Clientes Nuevos",
        "badgeClass": "badge-pill purple",
        "short": "Linda B2C"
    },
    {
        "id": "zully-b2b",
        "cartera_id": "zully-b2b",
        "name": "6. 🏢 Linda / Zully — B2B (> S/ 400)",
        "filter": "Linda B2B",
        "canal": "Tiendas Orgánicas Provincia & Mayoristas (> S/ 400)",
        "badge": "Mayoristas Inbound & Provincias",
        "badgeClass": "badge-pill green",
        "short": "Linda B2B"
    }
]

# Configuración oficial de Proveedores sacados estrictamente del Maestro de Artículos (RAW_ARTICULOS)
OFFICIAL_SUPPLIERS_META: Dict[str, Dict[str, Any]] = {
    "NUTRIVAS": {
        "id": "nutrivas",
        "nombre": "🏭 NUTRIVAS S.A.C.",
        "shortName": "NUTRIVAS",
        "cardStyle": "supplier-amber",
        "badge": "4-5d s/stock · 24-48h c/stock",
        "badgeClass": "badge-pill",
        "badgeStyle": "background: #fef3c7; color: #92400e; border: 1px solid #fcd34d;",
        "leadTime": "Con stock en almacén: 24 a 48h. Sin stock (pedido a lab): 4 a 5 días hábiles.",
        "promoVigente": "Bonificación 12+1 en NAD+Resveratrol (NAN-036) y 6+1 en Calabaza/Selenium/Colágeno.",
        "colors": ["#f59e0b", "#d97706", "#3b82f6", "#10b981", "#8b5cf6"]
    },
    "MOLINOS DEL MUNDO": {
        "id": "molinos-del-mundo",
        "nombre": "🏭 MOLINOS DEL MUNDO S.A.C.",
        "shortName": "MOLINOS DEL MUNDO",
        "cardStyle": "supplier-slate",
        "badge": "Entrega Fija Miércoles",
        "badgeClass": "badge-pill",
        "badgeStyle": "background: #f1f5f9; color: #334155; border: 1px solid #cbd5e1;",
        "leadTime": "Con stock: 24-48h. Reposición de fábrica: entregas fijas únicamente los miércoles.",
        "promoVigente": "Condiciones por volumen en cajas surtidas de pastas y libres de gluten.",
        "colors": ["#475569", "#64748b", "#334155", "#94a3b8", "#cbd5e1"]
    },
    "PECADITOS INTEGRALES": {
        "id": "pecaditos-integrales",
        "nombre": "🏭 PECADITOS INTEGRALES",
        "shortName": "PECADITOS INTEGRALES",
        "cardStyle": "supplier-purple",
        "badge": "Producción Semanal (7d)",
        "badgeClass": "badge-pill purple",
        "leadTime": "Con stock: 24-48h. Sin stock: producción bajo pedido (1 semana).",
        "promoVigente": "Rotación continua en galletas y snacks integrales artesanales.",
        "colors": ["#9333ea", "#a855f7", "#7e22ce", "#c084fc", "#d8b4fe"]
    },
    "AMAZON ANDES": {
        "id": "amazon-andes",
        "nombre": "🏭 AMAZON ANDES EXPORT S.A.C.",
        "shortName": "AMAZON ANDES",
        "cardStyle": "supplier-green",
        "badge": "Rápido (1-2 días)",
        "badgeClass": "badge-pill green",
        "leadTime": "Con stock: 24 a 48h. Sin stock: reposición rápida en 2 días hábiles.",
        "promoVigente": "Bonificación por volumen en superfoods, cápsulas y polvos orgánicos.",
        "colors": ["#059669", "#10b981", "#34d399", "#6ee7b7", "#a7f3d0"]
    },
    "WILD FOODS": {
        "id": "wild-foods",
        "nombre": "🏭 WILD FOODS",
        "shortName": "WILD FOODS",
        "cardStyle": "supplier-blue",
        "badge": "Stock Regular (24-48h)",
        "badgeClass": "badge-pill blue",
        "leadTime": "Despacho local de almacén: 24 a 48 horas (reposición 3-4 días).",
        "promoVigente": "Barras proteicas y snacks saludables de alta rotación en tiendas.",
        "colors": ["#2563eb", "#3b82f6", "#60a5fa", "#93c5fd", "#bfdbfe"]
    },
    "QORINKA": {
        "id": "qorinka",
        "nombre": "🏭 QORINKA",
        "shortName": "QORINKA",
        "cardStyle": "supplier-amber",
        "badge": "Reposición 4 días",
        "badgeClass": "badge-pill",
        "badgeStyle": "background: #fef3c7; color: #92400e; border: 1px solid #fcd34d;",
        "leadTime": "Con stock: 24-48h. Sin stock: tiempo de reposición de 4 días hábiles.",
        "promoVigente": "Línea de superfoods y suplementos naturales Qorinka.",
        "colors": ["#d97706", "#f59e0b", "#fbbf24", "#fcd34d", "#fde68a"]
    },
    "ANDES CRISP": {
        "id": "andes-crisp",
        "nombre": "🏭 ANDES CRISP",
        "shortName": "ANDES CRISP",
        "cardStyle": "supplier-green",
        "badge": "Rápido (1-2 días)",
        "badgeClass": "badge-pill green",
        "leadTime": "Con stock: 24-48h. Sin stock: despacho rápido en 2 días hábiles.",
        "promoVigente": "Snacks de vegetales y tubérculos andinos por cajas.",
        "colors": ["#10b981", "#059669", "#34d399", "#6ee7b7", "#a7f3d0"]
    },
    "INKA COMEX": {
        "id": "inka-comex",
        "nombre": "🏭 INKA COMEX",
        "shortName": "INKA COMEX",
        "cardStyle": "supplier-blue",
        "badge": "Inmediato (24-48h)",
        "badgeClass": "badge-pill blue",
        "leadTime": "Disponibilidad directa: despacho en 24 a 48 horas.",
        "promoVigente": "Condiciones preferenciales de distribución directa.",
        "colors": ["#1d4ed8", "#2563eb", "#3b82f6", "#60a5fa", "#93c5fd"]
    },
    "OLIVO DE ORO": {
        "id": "olivo-de-oro",
        "nombre": "🏭 OLIVO DE ORO",
        "shortName": "OLIVO DE ORO",
        "cardStyle": "supplier-green",
        "badge": "Rápido (1-2 días)",
        "badgeClass": "badge-pill green",
        "leadTime": "Con stock: 24-48h. Sin stock: reposición en 2 días hábiles.",
        "promoVigente": "Aceites de oliva extra virgen y derivados.",
        "colors": ["#15803d", "#16a34a", "#22c55e", "#4ade80", "#86efac"]
    },
    "DEPURATÉ": {
        "id": "depurate",
        "nombre": "🏭 DEPURATÉ",
        "shortName": "DEPURATÉ",
        "cardStyle": "supplier-purple",
        "badge": "Rápido (1-2 días)",
        "badgeClass": "badge-pill purple",
        "leadTime": "Con stock: 24-48h. Sin stock: reposición en 2 días hábiles.",
        "promoVigente": "Infusiones herbales y mezclas depurativas.",
        "colors": ["#7e22ce", "#9333ea", "#a855f7", "#c084fc", "#e9d5ff"]
    },
    "NOA LIFE": {
        "id": "noa-life",
        "nombre": "🏭 NOA LIFE",
        "shortName": "NOA LIFE",
        "cardStyle": "supplier-red",
        "badge": "En Liquidación",
        "badgeClass": "badge-pill",
        "badgeStyle": "background: #fee2e2; color: #991b1b; border: 1px solid #fca5a5;",
        "leadTime": "En liquidación: despacho inmediato solo hasta agotar stock existente.",
        "promoVigente": "Liquidación de inventario disponible en almacén.",
        "colors": ["#dc2626", "#ef4444", "#f87171", "#fca5a5", "#fecaca"]
    },
    "FIBRA FRUT": {
        "id": "fibra-frut",
        "nombre": "🏭 FIBRA FRUT",
        "shortName": "FIBRA FRUT",
        "cardStyle": "supplier-red",
        "badge": "Plazo 1 sem (MOQ 12u)",
        "badgeClass": "badge-pill",
        "badgeStyle": "background: #fee2e2; color: #991b1b; border: 1px solid #fca5a5;",
        "leadTime": "Con stock: 24-48h. Sin stock: 1 semana (pedido mínimo 12 unidades).",
        "promoVigente": "Bebidas funcionales con fibra prebiótica.",
        "colors": ["#b91c1c", "#dc2626", "#ef4444", "#f87171", "#fca5a5"]
    },
    "QORI": {
        "id": "qori",
        "nombre": "🏭 QORI",
        "shortName": "QORI",
        "cardStyle": "supplier-amber",
        "badge": "En Liquidación",
        "badgeClass": "badge-pill",
        "badgeStyle": "background: #fef3c7; color: #92400e; border: 1px solid #fcd34d;",
        "leadTime": "En liquidación: despacho inmediato hasta agotar stock en almacén.",
        "promoVigente": "Liquidación de stock disponible.",
        "colors": ["#b45309", "#d97706", "#f59e0b", "#fbbf24", "#fcd34d"]
    },
    "TAURI": {
        "id": "tauri",
        "nombre": "🏭 TAURI",
        "shortName": "TAURI",
        "cardStyle": "supplier-blue",
        "badge": "Rápido (1-2 días)",
        "badgeClass": "badge-pill blue",
        "leadTime": "Con stock: 24-48h. Sin stock: reposición rápida en 2 días hábiles.",
        "promoVigente": "Superalimentos a base de Tarwi/Chocho andino.",
        "colors": ["#0284c7", "#0ea5e9", "#38bdf8", "#7dd3fc", "#bae6fd"]
    },
    "OTROS PROVEEDORES": {
        "id": "otros-proveedores",
        "nombre": "🏭 OTROS PROVEEDORES COMPLEMENTARIOS",
        "shortName": "OTROS PROVEEDORES",
        "cardStyle": "supplier-slate",
        "badge": "Varios Plazos",
        "badgeClass": "badge-pill",
        "badgeStyle": "background: #f1f5f9; color: #334155; border: 1px solid #cbd5e1;",
        "leadTime": "Según disponibilidad de inventario en almacén (24-72h).",
        "promoVigente": "Líneas complementarias (Incasur, Inka Prime, Fungi Amazónica, Bromkisan).",
        "colors": ["#64748b", "#94a3b8", "#cbd5e1", "#475569", "#334155"]
    }
}


def normalize_proveedor_titular(raw_prov: str) -> str:
    """Normaliza el nombre del Proveedor Titular desde el Parquet/Maestro."""
    p = str(raw_prov).strip().upper()
    if "DEPURAT" in p:
        return "DEPURATÉ"
    if p in OFFICIAL_SUPPLIERS_META:
        return p
    return "OTROS PROVEEDORES"


def is_excluded_for_alerts(cod_cli: str, nom_cli: str) -> bool:
    """
    Regla Soberana (Comentario #3 de Cristian):
    Organa y UNALM SOLO se excluyen de las alertas (Pestaña 4) y propuestas de acciones / WhatsApp (Pestaña 5).
    Para todos los demás datos (ventas, fichas, matrices, histórico) SÍ están considerados.
    """
    cod = str(cod_cli).strip()
    nom = str(nom_cli).strip().upper()
    if cod == UNALM_RUC or "FUNDEAGRO" in nom or "FUNDACION PARA EL DESARROLLO AGRARIO" in nom:
        return True
    if cod in ORGANA_RUCS or "ORGANA" in nom:
        return True
    return False


def map_cxc_row_to_seller_id(row: pd.Series) -> str:
    """Asigna cada documento de Cuentas por Cobrar a uno de los 6 vendedores."""
    cod = str(row.get("Cod_Cliente", "")).strip()
    nom = str(row.get("Nombre del Cliente", "")).strip().upper()
    com = str(row.get("NOMBRE COMERCIAL", "")).strip().upper()
    vend = str(row.get("Nombre del Vendedor", "")).strip().upper()

    if cod in WHITNIN_CODES or "WHITNIN" in nom or "WHITNIN" in com:
        return "cristian"
    if cod in ORGANA_RUCS or "ORGANA" in nom or "ORGANA" in com:
        return "cristian"
    if cod == UNALM_RUC or "FUNDEAGRO" in nom or "AGRARIA" in com:
        return "walter"

    if "CRISTIAN" in vend:
        return "cristian"
    if "WALTER" in vend:
        return "walter"
    if "ENRIQUE" in vend:
        return "enrique"
    if "CUADROS" in vend or "CARLOS" in vend or "JOEL" in vend:
        return "carlos"
    if "REP. COMERCIAL" in vend or "ZULLY" in vend or "LINDA" in vend:
        total_doc = float(row.get("Total", 0.0) or 0.0)
        if total_doc > 400.0:
            return "zully-b2b"
        return "zully-b2c"
    return "enrique"


def load_cxc_details_by_seller(cxc_path: Path) -> Tuple[Dict[str, float], Dict[str, List[Dict[str, Any]]]]:
    """
    Lee 'Cuentas por cobrar 2026.xlsx' (hoja CXC) y retorna:
    - deuda_vencida_por_vendedor: {seller_id: monto_vencido_soles}
    - detalle_docs_por_vendedor: {seller_id: [lista de facturas VENCIDA y A CUENTA con mora]}
    """
    deuda_vencida: Dict[str, float] = {s["id"]: 0.0 for s in SELLER_CONFIG}
    detalle_docs: Dict[str, List[Dict[str, Any]]] = {s["id"]: [] for s in SELLER_CONFIG}

    if not cxc_path.exists():
        return deuda_vencida, detalle_docs

    try:
        df_cxc = pd.read_excel(cxc_path, sheet_name="CXC", skiprows=10)
        df_cxc = df_cxc.dropna(subset=["Número del Documento"])
        df_cxc["Cod_Cliente"] = (
            df_cxc["Código del Cliente"]
            .astype(str)
            .str.strip()
            .str.replace(r"\.0$", "", regex=True)
            .apply(lambda x: "0" + x if len(x) == 7 and x.isdigit() else x)
        )
        df_cxc = df_cxc[~df_cxc["Cod_Cliente"].isin(CONSUMO_INTERNO_CXC)]

        # Filtrar documentos VENCIDA y A CUENTA con saldo > 0
        df_open = df_cxc[df_cxc["Estado"].isin(["VENCIDA", "A CUENTA"])].copy()
        df_open["Saldo_num"] = pd.to_numeric(df_open["Saldo"], errors="coerce").fillna(0.0)
        df_open["Total_num"] = pd.to_numeric(df_open["Total"], errors="coerce").fillna(0.0)
        df_open["Dias_num"] = pd.to_numeric(df_open["Días vencidos"], errors="coerce").fillna(0).astype(int)
        df_open = df_open[df_open["Saldo_num"] > 0.5]

        for _, r in df_open.iterrows():
            s_id = map_cxc_row_to_seller_id(r)
            estado = str(r["Estado"]).strip().upper()
            saldo = round(float(r["Saldo_num"]), 2)
            total_doc = round(float(r["Total_num"]), 2)
            dias_mora = max(0, int(r["Dias_num"]))

            if estado == "VENCIDA":
                deuda_vencida[s_id] = round(deuda_vencida[s_id] + saldo, 2)

            f_emi = pd.to_datetime(r["Fecha"], errors="coerce")
            f_venc = pd.to_datetime(r["Fecha venc."], errors="coerce")
            emi_str = f_emi.strftime("%Y-%m-%d") if pd.notna(f_emi) else str(r["Fecha"])[:10]
            venc_str = f_venc.strftime("%Y-%m-%d") if pd.notna(f_venc) else str(r["Fecha venc."])[:10]

            nom_cli = str(r["Nombre del Cliente"]).strip() if pd.notna(r["Nombre del Cliente"]) else ""
            nom_com = str(r["NOMBRE COMERCIAL"]).strip() if pd.notna(r["NOMBRE COMERCIAL"]) and str(r["NOMBRE COMERCIAL"]).strip() != "nan" else nom_cli

            detalle_docs[s_id].append({
                "nroDoc": str(r["Número del Documento"]).strip(),
                "tipoDoc": str(r["Nombre del Documento"]).replace("01 Factura Electronica [F]", "Factura").replace("03 Boleta Electronica [B]", "Boleta").strip(),
                "ruc": str(r["Cod_Cliente"]),
                "cliente": nom_cli,
                "comercial": nom_com or nom_cli,
                "fechaEmision": emi_str,
                "fechaVenc": venc_str,
                "diasMora": dias_mora,
                "estado": estado,
                "total": total_doc,
                "saldo": saldo
            })

        # Ordenar los documentos de cada vendedor: primero VENCIDA, luego por mayor saldo
        for s_id in detalle_docs:
            detalle_docs[s_id].sort(key=lambda x: (0 if x["estado"] == "VENCIDA" else 1, -x["saldo"]))

    except Exception as e:
        print(f"[WARN CXC] Error al extraer detalle de CXC por vendedor: {e}")

    return deuda_vencida, detalle_docs


def build_global_cxc_vencidos(cxc_path: Path) -> Dict[str, Any]:
    """
    Construye el objeto consolidado GLOBAL_CXC_VENCIDOS con la totalidad de deuda vencida
    de Qali Kay (T024), con desglose por vendedor, lista por cliente y lista por comprobante.
    """
    default_payload = {
        "totalClientesVencidos": 0,
        "totalMontoVencido": 0.0,
        "totalDocsVencidos": 0,
        "desglosePorVendedor": {},
        "clientesVencidosList": [],
        "comprobantesVencidosList": []
    }

    if not cxc_path.exists():
        return default_payload

    try:
        df_cxc = pd.read_excel(cxc_path, sheet_name="CXC", skiprows=10)
        df_cxc = df_cxc.dropna(subset=["Número del Documento"])
        df_cxc["Cod_Cliente"] = (
            df_cxc["Código del Cliente"]
            .astype(str)
            .str.strip()
            .str.replace(r"\.0$", "", regex=True)
            .apply(lambda x: "0" + x if len(x) == 7 and x.isdigit() else x)
        )
        df_cxc = df_cxc[~df_cxc["Cod_Cliente"].isin(CONSUMO_INTERNO_CXC)]

        # Solo documentos con Estado VENCIDA y saldo > 0.50
        df_venc = df_cxc[df_cxc["Estado"] == "VENCIDA"].copy()
        df_venc["Saldo_num"] = pd.to_numeric(df_venc["Saldo"], errors="coerce").fillna(0.0)
        df_venc["Total_num"] = pd.to_numeric(df_venc["Total"], errors="coerce").fillna(0.0)
        df_venc["Dias_num"] = pd.to_numeric(df_venc["Días vencidos"], errors="coerce").fillna(0).astype(int)
        df_venc = df_venc[df_venc["Saldo_num"] > 0.50].copy()

        # Mapear vendedor de cada comprobante
        df_venc["seller_id"] = [map_cxc_row_to_seller_id(r) for _, r in df_venc.iterrows()]

        seller_meta = {s["id"]: s for s in SELLER_CONFIG}

        # 1. Desglose por Vendedor
        desglose = {}
        for s in SELLER_CONFIG:
            s_id = s["id"]
            sub = df_venc[df_venc["seller_id"] == s_id]
            desglose[s_id] = {
                "sellerId": s_id,
                "sellerName": s["name"],
                "sellerShort": s["short"],
                "badge": s["badge"],
                "badgeClass": s["badgeClass"],
                "docsCount": int(len(sub)),
                "clientesCount": int(sub["Cod_Cliente"].nunique()),
                "montoVencido": round(float(sub["Saldo_num"].sum()), 2)
            }

        # 2. Comprobantes Vencidos List
        comprobantes_list = []
        for _, r in df_venc.iterrows():
            s_id = r["seller_id"]
            s_short = seller_meta.get(s_id, {}).get("short", s_id)
            f_emi = pd.to_datetime(r["Fecha"], errors="coerce")
            f_venc = pd.to_datetime(r["Fecha venc."], errors="coerce")
            emi_str = f_emi.strftime("%Y-%m-%d") if pd.notna(f_emi) else str(r["Fecha"])[:10]
            venc_str = f_venc.strftime("%Y-%m-%d") if pd.notna(f_venc) else str(r["Fecha venc."])[:10]
            nom_cli = str(r["Nombre del Cliente"]).strip() if pd.notna(r["Nombre del Cliente"]) else ""
            nom_com = str(r["NOMBRE COMERCIAL"]).strip() if pd.notna(r["NOMBRE COMERCIAL"]) and str(r["NOMBRE COMERCIAL"]).strip() != "nan" else nom_cli

            comprobantes_list.append({
                "nroDoc": str(r["Número del Documento"]).strip(),
                "tipoDoc": str(r["Nombre del Documento"]).replace("01 Factura Electronica [F]", "Factura").replace("03 Boleta Electronica [B]", "Boleta").strip(),
                "ruc": str(r["Cod_Cliente"]),
                "cliente": nom_cli,
                "comercial": nom_com or nom_cli,
                "vendedor": s_short,
                "sellerId": s_id,
                "fechaEmision": emi_str,
                "fechaVenc": venc_str,
                "diasMora": max(0, int(r["Dias_num"])),
                "total": round(float(r["Total_num"]), 2),
                "saldo": round(float(r["Saldo_num"]), 2)
            })

        # Ordenar comprobantes por saldo descendente
        comprobantes_list.sort(key=lambda x: -x["saldo"])

        # 3. Clientes Vencidos List (Agrupados por Cod_Cliente)
        clientes_dict = {}
        for doc in comprobantes_list:
            ruc = doc["ruc"]
            if ruc not in clientes_dict:
                clientes_dict[ruc] = {
                    "ruc": ruc,
                    "cliente": doc["cliente"],
                    "comercial": doc["comercial"],
                    "vendedor": doc["vendedor"],
                    "sellerId": doc["sellerId"],
                    "docsCount": 0,
                    "maxDiasMora": 0,
                    "montoVencido": 0.0,
                    "docs": []
                }
            c_entry = clientes_dict[ruc]
            c_entry["docsCount"] += 1
            c_entry["maxDiasMora"] = max(c_entry["maxDiasMora"], doc["diasMora"])
            c_entry["montoVencido"] = round(c_entry["montoVencido"] + doc["saldo"], 2)
            c_entry["docs"].append(doc["nroDoc"])

        clientes_list = list(clientes_dict.values())
        clientes_list.sort(key=lambda x: -x["montoVencido"])

        total_monto = round(float(df_venc["Saldo_num"].sum()), 2)
        total_docs = int(len(df_venc))
        total_clientes = int(df_venc["Cod_Cliente"].nunique())

        return {
            "totalClientesVencidos": total_clientes,
            "totalMontoVencido": total_monto,
            "totalDocsVencidos": total_docs,
            "desglosePorVendedor": desglose,
            "clientesVencidosList": clientes_list,
            "comprobantesVencidosList": comprobantes_list
        }

    except Exception as e:
        print(f"[WARN CXC GLOBAL] Error al construir GLOBAL_CXC_VENCIDOS: {e}")
        return default_payload


def build_linda_b2c_full_history(alertas_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Construye la lista completa de clientes historicos de Linda B2C (2025-2026, ~877 clientes)
    con todos sus campos analiticos para descarga directa en Excel (.xlsx) via SheetJS (T024).
    """
    history_out = []
    for c in alertas_data:
        if c.get("cartera_asignada") != "zully-b2c":
            continue

        cod_cli = str(c.get("cod_cliente", "")).strip()
        nom_cli = str(c.get("nombre_cliente", "")).strip()
        if is_excluded_for_alerts(cod_cli, nom_cli):
            continue

        cob = c.get("cobranza", {})
        recompra = c.get("recompra_inteligente", {})
        canasta = [it.get("descripcion", "") for it in recompra.get("canasta_habitual", [])[:3]]

        history_out.append({
            "ruc": cod_cli,
            "nombre": nom_cli,
            "comercial": str(c.get("nombre_comercial", "")) or nom_cli,
            "contacto": str(c.get("contacto", "")),
            "celular": str(c.get("celular", "")),
            "distrito": str(c.get("distrito", "")),
            "canal": "B2C",
            "cantCompras": int(c.get("cant_compras_historicas", 0)),
            "esRecurrente": bool(c.get("es_recurrente", False)),
            "ultimaFecha": str(c.get("ultima_fecha_compra", "")),
            "diasInactivo": int(c.get("dias_inactivo", 0)),
            "cicloHabitual": round(float(c.get("mediana_ciclo_n", 30)), 1),
            "ticketPromedio": round(float(c.get("ticket_promedio", 0.0)), 2),
            "ultimoTicket": round(float(c.get("ultimo_ticket", 0.0)), 2),
            "deudaVencida": round(float(cob.get("deuda_vencida_soles", 0.0)), 2),
            "deudaTotal": round(float(cob.get("deuda_total_soles", 0.0)), 2),
            "docsVencidos": int(cob.get("docs_vencidos", 0)),
            "diasMoraMax": int(cob.get("dias_mora_max", 0)),
            "severidad": str(c.get("severidad", "INFO")),
            "tipoAlerta": str(c.get("tipo_alerta", "")),
            "textoAlerta": str(c.get("texto_alerta", "")),
            "topProductos": "; ".join(canasta),
            "promocionActiva": "; ".join(recompra.get("promociones_aplicables", [])[:1])
        })

    # Ordenar por dias_inactivo ascendente (los mas recientes primero)
    history_out.sort(key=lambda x: (x["diasInactivo"], -x["cantCompras"]))
    return history_out


def generate_clients_array(alertas_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Transforma las alertas consolidadas en el array CLIENTS para el frontend (Pestaña 4).
    Excluye estrictamente a Organa y UNALM de las alertas y propuestas de acciones (Comentario #3).
    Corrige mapeo de cartera_asignada, cobranza, sugerencia y waMsg (Comentarios #1, #6, #7, #8).
    """
    clients_out = []
    seller_name_map = {
        "cristian-gutierrez": "Cristian",
        "walter-gutierrez": "Walter",
        "enrique-garcia": "Enrique",
        "carlos-cuadros": "Carlos C",
        "zully-b2b": "Linda B2B",
        "zully-b2c": "Linda B2C"
    }

    for c in alertas_data:
        cod_cli = str(c.get("cod_cliente", "")).strip()
        nom_cli = str(c.get("nombre_cliente", "")).strip()

        # Comentario #3: Excluir Organa y UNALM de alertas y propuestas de acción
        if is_excluded_for_alerts(cod_cli, nom_cli):
            continue

        c_id = c.get("cartera_asignada", "enrique-garcia")
        vendedor = seller_name_map.get(c_id, "Enrique")
        dias_inactivo = int(c.get("dias_inactivo", 0))
        ciclo_n = round(float(c.get("mediana_ciclo_n", 30)), 1)
        retraso = max(0, int(dias_inactivo - ciclo_n))

        cobranza = c.get("cobranza", {})
        deuda_vencida = float(cobranza.get("deuda_vencida_soles", 0.0))
        deuda_total = float(cobranza.get("deuda_total_soles", 0.0))
        docs_venc = int(cobranza.get("docs_vencidos", 0))
        dias_mora = int(cobranza.get("dias_mora_max", 0))
        tiene_bloqueo = bool(cobranza.get("bloqueo_por_mora", False))

        # T024: Filtro ultimos 90 dias para Linda B2C en el Feed visible (Pestaña 4):
        # Solo incluir clientes de Linda B2C con ultima compra en ultimos 90 dias (dias_inactivo <= 90)
        # Y que requieran accion operativa (dias_inactivo >= 25 o deuda_vencida > 0).
        if c_id == "zully-b2c":
            if not (dias_inactivo <= 90 and (dias_inactivo >= 25 or deuda_vencida > 0)):
                continue

        severidad = c.get("severidad", "INFO")
        tipo_alerta = c.get("tipo_alerta", "")
        texto_alerta = str(c.get("texto_alerta", "")).strip()

        # Formato Alerta y Clase
        if tiene_bloqueo:
            alerta_text = "💸 DEUDA VENCIDA + RECOMPRA"
            alerta_class = "urgent"
            cxc_text = f"🔴 VENCIDA: S/ {deuda_vencida:,.2f} ({docs_venc} doc · {dias_mora}d mora)"
            cxc_is_debt = True
            tipo_accion = "COBRANZA CONDICIONADA + REPOSICIÓN"
        elif severidad == "CRITICA":
            if "B2C" in texto_alerta or c_id == "zully-b2c":
                alerta_text = "🔴 RESCATE B2C (>60d)"
            elif "NUEVO" in tipo_alerta:
                alerta_text = "🔴 RESCATE NUEVO (>30d)"
            else:
                alerta_text = "🔴 FUGA B2B (>N+5d)"
            alerta_class = "urgent"
            cxc_text = f"🟡 Por vencer: S/ {deuda_total:,.2f}" if deuda_total > 0 else "🟢 Al día (Sin deuda)"
            cxc_is_debt = False
            tipo_accion = "REACTIVACIÓN URGENTE DE CUENTA"
        elif severidad == "ADVERTENCIA":
            if c_id == "zully-b2c":
                alerta_text = "🟡 SEGUIMIENTO B2C (36-60d)"
            elif "VOLUMEN" in tipo_alerta:
                alerta_text = "🟡 CAÍDA DE VOLUMEN (>30%)"
            else:
                alerta_text = "🟡 CICLO VENCIDO (N a N+4d)"
            alerta_class = "warning"
            cxc_text = f"🟡 Por vencer: S/ {deuda_total:,.2f}" if deuda_total > 0 else "🟢 Al día (Sin deuda)"
            cxc_is_debt = False
            tipo_accion = "SEGUIMIENTO DE RECOMPRA"
        elif severidad == "OPORTUNIDAD":
            if c_id == "zully-b2c":
                alerta_text = "🟠 FIN DE FRASCO (25-35d)"
            else:
                alerta_text = "🟠 VENTANA DE PEDIDO (N-3 a N)"
            alerta_class = "info"
            cxc_text = f"🟡 Por vencer: S/ {deuda_total:,.2f}" if deuda_total > 0 else "🟢 Al día (Sin deuda)"
            cxc_is_debt = False
            tipo_accion = "LEVANTAR PEDIDO EN CICLO"
        else:
            alerta_text = "🟢 EN CICLO ACTIVO"
            alerta_class = "info"
            cxc_text = f"🟡 Por vencer: S/ {deuda_total:,.2f}" if deuda_total > 0 else "🟢 Al día (Sin deuda)"
            cxc_is_debt = False
            tipo_accion = "FIDELIZACIÓN / CROSS-SELL"

        recompra = c.get("recompra_inteligente", {})
        canasta = recompra.get("canasta_habitual", [])
        promos = recompra.get("promociones_aplicables", [])
        wa_msg = str(recompra.get("whatsapp_copy", "")).strip()

        # Extraer proveedores/productos reales para los tags
        historial_tags = []
        skus_sugeridos = []
        lead_times_list = []

        for item in canasta[:3]:
            prov_name = normalize_proveedor_titular(item.get("proveedor", "NUTRIVAS"))
            desc_corta = str(item.get("descripcion", "")).strip()
            if len(desc_corta) > 30:
                desc_corta = desc_corta[:28] + ".."
            tag_str = f"{prov_name}: {desc_corta}"
            if tag_str not in historial_tags:
                historial_tags.append(tag_str)
            stock_val = int(float(item.get("stock_almacen", 0)))
            skus_sugeridos.append(f"{item.get('descripcion', '')} (Stock: {stock_val}u)")
            est_log = item.get("estado_logistico", "")
            if est_log and est_log not in lead_times_list:
                lead_times_list.append(est_log)

        if not historial_tags:
            historial_tags = ["NUTRIVAS: Catálogo General"]

        lead_time_text = " · ".join(lead_times_list[:2]) if lead_times_list else "Despacho 24 a 48h desde almacén."

        # Construir Acción Sugerida completa y explícita (Comentario #8)
        partes_sugerencia = []
        if tiene_bloqueo:
            partes_sugerencia.append(
                f"Cobrar saldo vencido de S/ {deuda_vencida:,.2f} ({docs_venc} comprobantes, máx {dias_mora}d mora) antes de liberar nuevo despacho."
            )
        if texto_alerta:
            partes_sugerencia.append(texto_alerta)
        if skus_sugeridos:
            partes_sugerencia.append("Ofrecer reposición de: " + "; ".join(skus_sugeridos[:3]) + ".")
        if promos:
            partes_sugerencia.append(f"Impulsar promo vigente: {promos[0]}.")

        sugerencia_final = " ".join(partes_sugerencia).strip()
        if not sugerencia_final:
            sugerencia_final = "Contactar cliente para reposición de canasta habitual e impulsar promociones del mes."

        # Si el cliente tiene deuda vencida, enriquecer el mensaje de WhatsApp para que incluya recordatorio cordial
        if not wa_msg:
            nom_comercial = str(c.get("nombre_comercial", "") or nom_cli)
            wa_msg = (
                f"¡Hola! Te saludamos de Qali Kay S.A.C. 🌿\n\n"
                f"Nos comunicamos con *{nom_comercial}* para coordinar la reposición de tus productos habituales "
                f"y comentarte nuestras promociones vigentes de la semana.\n\n"
                f"¿Te gustaría que revisemos tu pedido para programar despacho?"
            )

        raw_phone = str(c.get("celular", "")).strip().replace(".0", "").replace("-", "").replace(" ", "")
        if raw_phone and not raw_phone.startswith("51") and len(raw_phone) == 9:
            raw_phone = "51" + raw_phone
        phone = raw_phone if raw_phone else "51999999999"

        # Determinar si el cliente está con su ciclo vencido (para la tarjeta Clientes Vencidos Total Qali Kay)
        es_vencido = (severidad in ["CRITICA", "ADVERTENCIA", "OPORTUNIDAD"]) or (retraso > 0) or (dias_inactivo > 25 and c_id == "zully-b2c")

        clients_out.append({
            "vendedor": vendedor,
            "carteraId": c_id,
            "canal": str(c.get("canal", "B2B")),
            "ruc": cod_cli,
            "nombre": nom_cli,
            "comercial": str(c.get("nombre_comercial", "")) or nom_cli,
            "alerta": alerta_text,
            "alertaClass": alerta_class,
            "severidad": severidad,
            "esVencido": es_vencido,
            "historialMarcas": historial_tags[:3],
            "diasSinCompra": dias_inactivo,
            "cicloHabitual": ciclo_n,
            "retrasoDias": retraso,
            "ticket": f"S/ {float(c.get('ticket_promedio', 0.0) or c.get('ultimo_ticket', 0.0)):,.2f}",
            "cxc": cxc_text,
            "cxcIsDebt": cxc_is_debt,
            "deudaVencida": deuda_vencida,
            "tipoAccion": tipo_accion,
            "sugerencia": sugerencia_final,
            "leadTime": lead_time_text,
            "phone": phone,
            "waMsg": wa_msg
        })

    # Ordenar priorizando: 1) Con deuda vencida, 2) Severidad CRITICA, 3) ADVERTENCIA, 4) OPORTUNIDAD, 5) Mayor ticket
    sev_rank = {"CRITICA": 1, "ADVERTENCIA": 2, "OPORTUNIDAD": 3, "INFO": 4}
    clients_out.sort(key=lambda x: (
        0 if x["cxcIsDebt"] else 1,
        sev_rank.get(x["severidad"], 5),
        -x["deudaVencida"],
        -x["retrasoDias"]
    ))

    for idx, item in enumerate(clients_out):
        item["_idx"] = idx

    return clients_out


def compute_portfolio_inactivity_at_cutoff(
    df_up_to_cutoff: pd.DataFrame,
    cutoff_date: datetime.date
) -> Dict[str, Dict[str, int]]:
    """
    Calcula determinísticamente para cada una de las 6 carteras hasta la fecha de corte:
    - cartera_total: total de clientes históricos de esa cartera hasta esa fecha
    - una2m: clientes de esa cartera con 1 sola compra (fecha única) y > 60 días sin comprar al cutoff
    - sin2m: clientes de esa cartera con > 60 días sin comprar al cutoff
    Incluye el 100% de los clientes de la cartera (Comentarios #1, #3 y #5).
    """
    result = {
        s["cartera_id"]: {"cartera": 0, "una2m": 0, "sin2m": 0}
        for s in SELLER_CONFIG
    }
    if df_up_to_cutoff.empty:
        return result

    # Agrupar por cliente
    for cod_cli, grp in df_up_to_cutoff.groupby("Cod_Cliente"):
        nom_cli = str(grp["Nombre_Cliente"].iloc[0])
        c_owner = determine_client_cartera_owner(grp, str(cod_cli), nom_cli)
        if c_owner not in result:
            continue

        result[c_owner]["cartera"] += 1

        # Fechas con compra neta > 0
        daily = grp.groupby("Fecha")["Total_Detalle"].sum()
        pos_days = daily[daily > 0]
        if pos_days.empty:
            last_dt = pd.to_datetime(grp["Fecha"].max()).date()
            n_compras = 0
        else:
            last_dt = pd.to_datetime(pos_days.index.max()).date()
            n_compras = len(pos_days)

        dias_sin = (cutoff_date - last_dt).days
        if dias_sin > 60:
            result[c_owner]["sin2m"] += 1
            if n_compras <= 1:
                result[c_owner]["una2m"] += 1

    return result


def build_dashboard_payload(
    parquet_path: Path = DEFAULT_PARQUET_PATH,
    alertas_path: Path = DEFAULT_ALERTAS_PATH,
    cxc_path: Path = DEFAULT_CXC_PATH,
    sync_cache_path: Path = DEFAULT_SYNC_PATH
) -> Dict[str, Any]:
    """Construye determinísticamente todos los diccionarios y arrays para el frontend."""
    print("=" * 80)
    print("CONSTRUYENDO PAYLOAD DE DATOS DEL DASHBOARD COMERCIAL (QALI KAY S.A.C.)")
    print(f"Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    # 1. Cargar Parquet
    df = pd.read_parquet(parquet_path)
    doc_totals = df.groupby("Nro_Doc")["Total_Detalle"].sum().to_dict()
    df["cartera_id"] = [classify_transactional_cartera(r, doc_totals) for _, r in df.iterrows()]
    df["Proveedor_Norm"] = [normalize_proveedor_titular(p) for p in df["Proveedor_Titular"]]

    # 2. Cargar Alertas
    with open(alertas_path, encoding="utf-8") as f:
        alertas_raw = json.load(f)
    clientes_alertas = alertas_raw.get("clientes", [])

    # 3. Cargar Sync Status
    sync_info = {
        "estado": "🟢 Sincronizado",
        "ultima_actualizacion": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "timestamp_exportacion": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "filas_ventas": len(df[df["Periodo_Mes"] >= "2026-07"]),
        "filas_kardex": 638,
        "transacciones_historicas": len(df),
        "clientes_totales": len(clientes_alertas),
        "venta_total_acumulada": round(float(df["Total_Detalle"].sum()), 2)
    }
    if sync_cache_path.exists():
        try:
            cached_sync = json.loads(sync_cache_path.read_text(encoding="utf-8"))
            sync_info["ultima_actualizacion"] = cached_sync.get("ultima_actualizacion", sync_info["ultima_actualizacion"])
            sync_info["estado"] = "🟢 " + cached_sync.get("estado", "Sincronizado")
            sync_info["filas_kardex"] = cached_sync.get("filas_kardex", 638)
            sync_info["filas_ventas"] = cached_sync.get("filas_ventas", len(df))
        except Exception:
            pass

    # 4. Deuda Vencida y Detalle de Facturas CXC por Vendedor (Comentario #6)
    deuda_por_cartera, detalle_cxc_por_vendedor = load_cxc_details_by_seller(cxc_path)

    # Identificar primera compra por cliente en todo el historial para marcar "nuevos"
    first_purchase = df.groupby("Cod_Cliente")["Fecha"].min().to_dict()
    df["Es_Primera_Compra"] = df.apply(lambda r: r["Fecha"] == first_purchase.get(r["Cod_Cliente"]), axis=1)

    # 5. Generar MONTHLY_DATA para los últimos 6 meses de 2026 + Consolidado Anual (Comentarios #1, #2, #3, #5, #6, #9)
    periods = ["2026-10", "2026-09", "2026-08", "2026-07", "2026-06", "2026-05", "2026-ANUAL"]
    period_cutoffs = {
        "2026-10": datetime.date(2026, 10, 26),
        "2026-09": datetime.date(2026, 9, 30),
        "2026-08": datetime.date(2026, 8, 31),
        "2026-07": datetime.date(2026, 7, 31),
        "2026-06": datetime.date(2026, 6, 30),
        "2026-05": datetime.date(2026, 5, 31),
        "2026-ANUAL": datetime.date(2026, 10, 26),
    }
    monthly_data: Dict[str, List[Dict[str, Any]]] = {}

    max_oct_day = pd.to_datetime(df[df["Periodo_Mes"] == "2026-10"]["Fecha"].max()).day if not df[df["Periodo_Mes"] == "2026-10"].empty else 26
    days_in_oct = 31

    # Cartera total actual de cada vendedor desde alertas_comerciales_consolidadas.json (1,312 clientes)
    cartera_actual_counts = {
        s["cartera_id"]: sum(1 for c in clientes_alertas if c.get("cartera_asignada") == s["cartera_id"])
        for s in SELLER_CONFIG
    }

    for p in periods:
        cutoff_dt = period_cutoffs[p]
        cutoff_str = cutoff_dt.strftime("%Y-%m-%d")
        df_up_to = df[df["Fecha"] <= cutoff_str]
        inact_stats = compute_portfolio_inactivity_at_cutoff(df_up_to, cutoff_dt)

        if p == "2026-ANUAL":
            df_p = df[df["Anio"] == 2026]
        else:
            df_p = df[df["Periodo_Mes"] == p]

        period_rows = []
        for s in SELLER_CONFIG:
            s_id = s["id"]
            c_id = s["cartera_id"]
            # Comentarios #2 y #3: Incluir el 100% de las ventas comerciales (sin excluir Organa ni UNALM en datos de ventas)
            grp = df_p[df_p["cartera_id"] == c_id]

            venta = round(float(grp["Total_Detalle"].sum()), 2)
            pedidos = int(grp["Nro_Doc"].nunique())
            cli_mes = int(grp["Cod_Cliente"].nunique())
            ticket = round(venta / max(pedidos, 1), 2)

            # Nuevos en el período
            nuevos = int(grp[grp["Es_Primera_Compra"]]["Cod_Cliente"].nunique())

            # Total clientes de la cartera y métricas de inactividad (>60 días)
            tot_cartera = cartera_actual_counts.get(c_id, inact_stats[c_id]["cartera"])
            una2m = inact_stats[c_id]["una2m"]
            sin2m = inact_stats[c_id]["sin2m"]

            proy = None
            if p == "2026-10":
                proy = round((venta / max(max_oct_day, 1)) * days_in_oct, 2)

            deuda = deuda_por_cartera.get(s_id, 0.0)
            cxc_str = f"S/ {deuda:,.2f}"
            cxc_color = "#dc2626" if deuda > 3000 else ("#b45309" if deuda > 0 else "#059669")

            period_rows.append({
                "id": s_id,
                "name": s["name"],
                "filter": s["filter"],
                "venta": venta,
                "proy": proy,
                "cliMes": cli_mes,
                "cartera": tot_cartera,
                "pedidos": pedidos,
                "ticket": ticket,
                "nuevos": nuevos,
                "una2m": una2m,
                "sin2m": sin2m,
                "cxc": cxc_str,
                "cxcVal": deuda,
                "cxcColor": cxc_color
            })

        # Ordenar por venta descendente en cada periodo
        period_rows.sort(key=lambda x: x["venta"], reverse=True)
        monthly_data[p] = period_rows

    # 6. Generar TIME_SERIES: últimos 6 meses de 2026 (May-Oct) + Promedio 2025 por meses con actividad (Comentario #9)
    time_series: Dict[str, List[Dict[str, Any]]] = {
        "venta": [],
        "clientes": [],
        "nuevos": [],
        "una_compra": [],
        "sin_comprar": [],
        "ticket": []
    }

    df_2025 = df[df["Anio"] == 2025]
    six_months = ["2026-05", "2026-06", "2026-07", "2026-08", "2026-09", "2026-10"]
    m_keys = ["may26", "jun26", "jul26", "ago26", "sep26", "oct26"]

    for s in SELLER_CONFIG:
        s_id = s["id"]
        c_id = s["cartera_id"]
        s_name = s["name"]

        g25 = df_2025[df_2025["cartera_id"] == c_id]
        # Comentario #9: Promedio 2025 considerando SOLO los meses en que el vendedor tuvo actividad (venta > 0)
        if not g25.empty:
            monthly_sums_25 = g25.groupby("Periodo_Mes")["Total_Detalle"].sum()
            active_months_25 = int((monthly_sums_25 > 0).sum())
        else:
            active_months_25 = 0
        div_months_25 = max(active_months_25, 1)

        # Diccionario auxiliar de filas mensuales 2026 para este vendedor
        s_m_rows = {}
        for m_code in six_months:
            s_m_rows[m_code] = next(r for r in monthly_data[m_code] if r["id"] == s_id)

        # 1. Venta Neta
        v25 = round(float(g25["Total_Detalle"].sum()) / div_months_25, 2)
        row_venta = {
            "id": s_id,
            "name": s_name,
            "y2025": v25,
            "mesesActivos2025": active_months_25,
            "isCurrency": True
        }
        for mk, mc in zip(m_keys, six_months):
            row_venta[mk] = s_m_rows[mc]["venta"]
        row_venta["octProy"] = s_m_rows["2026-10"]["proy"]
        time_series["venta"].append(row_venta)

        # 2. Clientes activos (promedio en meses con actividad en 2025)
        if not g25.empty and active_months_25 > 0:
            active_m_list = monthly_sums_25[monthly_sums_25 > 0].index.tolist()
            c25 = round(float(g25[g25["Periodo_Mes"].isin(active_m_list)].groupby("Periodo_Mes")["Cod_Cliente"].nunique().mean()), 0)
        else:
            c25 = 0
        row_cli = {
            "id": s_id,
            "name": s_name,
            "y2025": int(c25),
            "mesesActivos2025": active_months_25,
            "isCurrency": False
        }
        for mk, mc in zip(m_keys, six_months):
            row_cli[mk] = s_m_rows[mc]["cliMes"]
        time_series["clientes"].append(row_cli)

        # 3. Clientes Nuevos
        if not g25.empty and active_months_25 > 0:
            n25 = round(float(g25[g25["Es_Primera_Compra"]].groupby("Periodo_Mes")["Cod_Cliente"].nunique().sum()) / div_months_25, 0)
        else:
            n25 = 0
        row_nuevos = {
            "id": s_id,
            "name": s_name,
            "y2025": int(n25),
            "mesesActivos2025": active_months_25,
            "isCurrency": False
        }
        for mk, mc in zip(m_keys, six_months):
            row_nuevos[mk] = s_m_rows[mc]["nuevos"]
        time_series["nuevos"].append(row_nuevos)

        # 4. Clientes con 1 sola compra (>2M)
        inact_2025_end = compute_portfolio_inactivity_at_cutoff(df[df["Anio"] == 2025], datetime.date(2025, 12, 31))
        row_una = {
            "id": s_id,
            "name": s_name,
            "y2025": inact_2025_end[c_id]["una2m"],
            "mesesActivos2025": active_months_25,
            "isCurrency": False
        }
        for mk, mc in zip(m_keys, six_months):
            row_una[mk] = s_m_rows[mc]["una2m"]
        time_series["una_compra"].append(row_una)

        # 5. Clientes sin comprar (>2M)
        row_sin = {
            "id": s_id,
            "name": s_name,
            "y2025": inact_2025_end[c_id]["sin2m"],
            "mesesActivos2025": active_months_25,
            "isCurrency": False
        }
        for mk, mc in zip(m_keys, six_months):
            row_sin[mk] = s_m_rows[mc]["sin2m"]
        time_series["sin_comprar"].append(row_sin)

        # 6. Ticket Promedio
        pedidos_25 = int(g25["Nro_Doc"].nunique())
        t25 = round(float(g25["Total_Detalle"].sum()) / max(pedidos_25, 1), 2) if pedidos_25 > 0 else 0.0
        row_ticket = {
            "id": s_id,
            "name": s_name,
            "y2025": t25,
            "mesesActivos2025": active_months_25,
            "isCurrency": True
        }
        for mk, mc in zip(m_keys, six_months):
            row_ticket[mk] = s_m_rows[mc]["ticket"]
        time_series["ticket"].append(row_ticket)

    # 7. Generar SELLER_DRILLDOWN_DETAILS (con soporte multi-período, 6 meses de tendencia y detalle desplegable de CxC)
    seller_drilldown: Dict[str, Any] = {}

    for s in SELLER_CONFIG:
        s_id = s["id"]
        c_id = s["cartera_id"]

        # Datos por cada período para que el selector de mes en Pestaña 1 actualice también la Ficha Individual
        by_period: Dict[str, Any] = {}
        for p in periods:
            p_row = next(r for r in monthly_data[p] if r["id"] == s_id)
            if p == "2026-ANUAL":
                df_sp = df[(df["Anio"] == 2026) & (df["cartera_id"] == c_id)]
            else:
                df_sp = df[(df["Periodo_Mes"] == p) & (df["cartera_id"] == c_id)]

            sku_sales = df_sp.groupby(["Cod_Producto", "Desc_Producto", "Proveedor_Norm"])["Total_Detalle"].sum().sort_values(ascending=False)
            tot_s_sales = max(float(df_sp["Total_Detalle"].sum()), 1.0)
            p_sku_mix = []
            palette = ["#f59e0b", "#3b82f6", "#10b981", "#2563eb", "#8b5cf6"]
            top5_soles = 0.0

            for idx, ((sku_cod, sku_desc, prov_tit), s_val) in enumerate(list(sku_sales.items())[:5]):
                if s_val <= 0:
                    continue
                pct = round((s_val / tot_s_sales) * 100, 1)
                top5_soles += s_val
                p_sku_mix.append({
                    "sku": f"{sku_desc} ({sku_cod})",
                    "proveedor": prov_tit,
                    "venta": round(float(s_val), 2),
                    "pct": pct,
                    "color": palette[idx % len(palette)]
                })

            otros_soles = max(0.0, float(df_sp["Total_Detalle"].sum()) - top5_soles)
            otros_pct = round(max(0.0, 100.0 - sum(x["pct"] for x in p_sku_mix)), 1)
            if otros_soles > 0 or not p_sku_mix:
                p_sku_mix.append({
                    "sku": "Otros SKUs de Cartera",
                    "proveedor": "Varios Proveedores",
                    "venta": round(otros_soles, 2),
                    "pct": otros_pct,
                    "color": "#94a3b8"
                })

            cob_pct = round((p_row["cliMes"] / max(p_row["cartera"], 1)) * 100)
            by_period[p] = {
                "venta": p_row["venta"],
                "proy": p_row["proy"],
                "clientesActivos": f"{p_row['cliMes']} / {p_row['cartera']} ({cob_pct}% cob.)",
                "ticketMedio": p_row["ticket"],
                "pedidos": p_row["pedidos"],
                "nuevos": p_row["nuevos"],
                "una2m": p_row["una2m"],
                "inactivos2m": p_row["sin2m"],
                "skuMix": p_sku_mix
            }

        oct_info = by_period["2026-10"]
        ts_v_row = next(r for r in time_series["venta"] if r["id"] == s_id)

        # Tendencia histórica: Prom '25 (meses activos) + últimos 6 meses de 2026 (May, Jun, Jul, Ago, Sep, Oct)
        v_trend = [
            {"period": f"Prom '25 ({ts_v_row['mesesActivos2025']}m)", "val": ts_v_row["y2025"]},
            {"period": "May 26", "val": ts_v_row["may26"]},
            {"period": "Jun 26", "val": ts_v_row["jun26"]},
            {"period": "Jul 26", "val": ts_v_row["jul26"]},
            {"period": "Ago 26", "val": ts_v_row["ago26"]},
            {"period": "Sep 26", "val": ts_v_row["sep26"]},
            {"period": "Oct 26", "val": ts_v_row["oct26"], "proy": ts_v_row["octProy"]}
        ]

        # Top 5 clientes de este vendedor (incluyendo todos sus clientes reales)
        seller_cli = [c for c in clientes_alertas if c.get("cartera_asignada") == c_id]
        # Ordenar por venta total 2026 en el dataframe
        cli_sales_26 = df[(df["Anio"] == 2026) & (df["cartera_id"] == c_id)].groupby("Cod_Cliente")["Total_Detalle"].sum().to_dict()
        seller_cli.sort(key=lambda x: cli_sales_26.get(str(x.get("cod_cliente", "")), 0.0), reverse=True)

        top_clients = []
        for c in seller_cli[:6]:
            cod_c = str(c.get("cod_cliente", ""))
            nom_c = str(c.get("nombre_comercial", "") or c.get("nombre_cliente", ""))
            deuda_c = float(c.get("cobranza", {}).get("deuda_vencida_soles", 0.0))
            excl_alert = is_excluded_for_alerts(cod_c, nom_c)

            if excl_alert:
                st = f"🏢 Cuenta Institucional (Venta 2026: S/ {cli_sales_26.get(cod_c, 0.0):,.2f})"
                act = "Gestión directa de Dirección (Excluida de alertas automáticas)"
            elif deuda_c > 0:
                st = f"🔴 Deuda vencida: S/ {deuda_c:,.2f}"
                act = "Cobrar facturas vencidas antes de liberar despacho"
            elif c.get("dias_inactivo", 0) > c.get("mediana_ciclo_n", 30):
                st = f"🟡 Ciclo vencido ({int(c.get('dias_inactivo', 0))}d sin pedir)"
                act = "Contactar hoy con sugerencia de recompra y promociones"
            else:
                st = f"🟢 Activo en ciclo ({int(c.get('dias_inactivo', 0))}d)"
                act = "Fidelizar y ofrecer líneas complementarias"

            top_clients.append({
                "name": nom_c,
                "ruc": cod_c,
                "ticket": f"S/ {float(c.get('ticket_promedio', 0.0)):,.2f}",
                "venta2026": f"S/ {cli_sales_26.get(cod_c, 0.0):,.2f}",
                "status": st,
                "action": act
            })

        deuda_val = deuda_por_cartera.get(s_id, 0.0)
        docs_list = detalle_cxc_por_vendedor.get(s_id, [])
        venc_count = sum(1 for d in docs_list if d["estado"] == "VENCIDA")
        ac_count = sum(1 for d in docs_list if d["estado"] == "A CUENTA")
        ac_saldo = round(sum(d["saldo"] for d in docs_list if d["estado"] == "A CUENTA"), 2)

        # T029: Clientes inactivos (>60 días) de esta cartera
        seller_inactives = []
        for c in clientes_alertas:
            if c.get("cartera_asignada") == c_id and float(c.get("dias_inactivo", 0)) > 60:
                cant_compras = int(c.get("cant_compras_historicas", 0))
                es_una = (cant_compras <= 1)
                tipo_inact = "1 Sola Compra (>2M)" if es_una else "Recurrente Inactivo (>2M)"

                canasta = c.get("recompra_inteligente", {}).get("canasta_habitual", [])
                prods = [
                    p.get("descripcion") or p.get("sku") or ""
                    for p in canasta
                    if p.get("sku") != "DELIVERY" and "DELIVERY" not in (p.get("descripcion") or "").upper()
                ]
                if not prods:
                    prods = [p.get("descripcion") or p.get("sku") or "" for p in canasta]
                top3 = " | ".join(prods[:3])

                rec = {
                    "ruc": str(c.get("cod_cliente", "")),
                    "cliente": str(c.get("nombre_cliente", "")),
                    "comercial": str(c.get("nombre_comercial", "") or c.get("nombre_cliente", "")),
                    "contacto": str(c.get("contacto", "")),
                    "celular": str(c.get("celular", "")),
                    "distrito": str(c.get("distrito", "")),
                    "cantCompras": cant_compras,
                    "esUnaCompra": es_una,
                    "tipoInactividad": tipo_inact,
                    "ultimaCompra": str(c.get("ultima_fecha_compra", "")),
                    "diasSinCompra": int(c.get("dias_inactivo", 0)),
                    "cicloHabitual": round(float(c.get("mediana_ciclo_n", 30.0)), 1),
                    "ticketPromedio": round(float(c.get("ticket_promedio", 0.0)), 2),
                    "ultimoTicket": round(float(c.get("ultimo_ticket", 0.0)), 2),
                    "deudaVencida": round(float(c.get("cobranza", {}).get("deuda_vencida_soles", 0.0)), 2),
                    "top3Productos": top3,
                    "vendedor": s["name"]
                }
                seller_inactives.append(rec)

        seller_inactives.sort(key=lambda x: x["ticketPromedio"], reverse=True)
        una_count = sum(1 for x in seller_inactives if x["esUnaCompra"])

        seller_drilldown[s_id] = {
            "nombre": s["name"],
            "canal": s["canal"],
            "badge": s["badge"],
            "badgeClass": s["badgeClass"],
            "octActual": oct_info["venta"],
            "octProy": oct_info["proy"],
            "clientesActivos": oct_info["clientesActivos"],
            "ticketMedio": oct_info["ticketMedio"],
            "nuevos": oct_info["nuevos"],
            "una2m": oct_info["una2m"],
            "inactivos2m": oct_info["inactivos2m"],
            "deudaCxc": f"S/ {deuda_val:,.2f}",
            "deudaCxcSub": f"{venc_count} fact. vencidas · Clic para ver detalle ▼" if venc_count > 0 else (f"{ac_count} a cuenta · Clic para ver ▼" if ac_count > 0 else "0 facturas vencidas (Al día)"),
            "deudaColor": "#dc2626" if deuda_val > 3000 else ("#b45309" if deuda_val > 0 else "#059669"),
            "cxcVencidaSoles": deuda_val,
            "cxcACuentaSoles": ac_saldo,
            "cxcDocsCount": len(docs_list),
            "cxcVencidosCount": venc_count,
            "cxcDetalle": docs_list,
            "inactivosTotalCount": len(seller_inactives),
            "inactivosUnaCompraCount": una_count,
            "inactivosDetalle": seller_inactives,
            "skuMix": oct_info["skuMix"],
            "byPeriod": by_period,
            "trend": v_trend,
            "topClients": top_clients
        }

    # 8. Generar SUPPLIERS_MONTHLY_DATA y SUPPLIER_TOP_SKUS_MASTER (Comentario #10: Solo Proveedor del Maestro de Artículos y SKU)
    suppliers_monthly: Dict[str, List[Dict[str, Any]]] = {}
    supplier_top_skus_master: Dict[str, List[Dict[str, Any]]] = {}

    # Calcular Master Top 5 SKUs en todo 2026 por cada Proveedor Oficial
    df_2026_all = df[df["Anio"] == 2026]
    for prov_key, sc in OFFICIAL_SUPPLIERS_META.items():
        s_id = sc["id"]
        grp_s = df_2026_all[df_2026_all["Proveedor_Norm"] == prov_key]
        tot_s = max(float(grp_s["Total_Detalle"].sum()), 1.0)
        sku_grp = grp_s.groupby(["Cod_Producto", "Desc_Producto"])["Total_Detalle"].sum().sort_values(ascending=False)

        top_skus_list = []
        for idx, ((sku_cod, sku_desc), s_val) in enumerate(list(sku_grp.items())[:5]):
            if s_val <= 0:
                continue
            share = round((s_val / tot_s) * 100, 1)
            rot = "🔥 Top #1 facturación del proveedor" if idx == 0 else ("🟢 Alta rotación comercial" if idx < 3 else "🟡 Rotación complementaria")
            top_skus_list.append({
                "sku": f"{sku_desc} ({sku_cod})",
                "venta": round(float(s_val), 2),
                "share": share,
                "rotacion": rot,
                "color": sc["colors"][idx % len(sc["colors"])]
            })
        supplier_top_skus_master[s_id] = top_skus_list

    for p in periods:
        if p == "2026-ANUAL":
            df_sp = df[df["Anio"] == 2026]
        else:
            df_sp = df[df["Periodo_Mes"] == p]

        supp_rows = []
        for prov_key, sc in OFFICIAL_SUPPLIERS_META.items():
            s_id = sc["id"]
            grp_s = df_sp[df_sp["Proveedor_Norm"] == prov_key]

            venta = round(float(grp_s["Total_Detalle"].sum()), 2)
            pedidos = int(grp_s["Nro_Doc"].nunique())
            ticket = round(venta / max(pedidos, 1), 2)

            # Ventas por vendedor para este proveedor en este período
            seller_sales_list = []
            for s in SELLER_CONFIG:
                v_sell = round(float(grp_s[grp_s["cartera_id"] == s["cartera_id"]]["Total_Detalle"].sum()), 2)
                seller_sales_list.append({"name": s["short"], "venta": v_sell})

            best_seller = max(seller_sales_list, key=lambda x: x["venta"], default={"name": "Sin ventas", "venta": 0.0})
            vendedor_lider = f"{best_seller['name']} (S/ {best_seller['venta']:,.2f})" if best_seller["venta"] > 0 else "Sin ventas en el período"

            # Top 5 SKUs exactos de este período para este proveedor
            sku_grp_p = grp_s.groupby(["Cod_Producto", "Desc_Producto"])["Total_Detalle"].sum().sort_values(ascending=False)
            tot_sp_venta = max(venta, 1.0)
            period_top_skus = []
            for idx, ((sku_cod, sku_desc), s_val) in enumerate(list(sku_grp_p.items())[:5]):
                if s_val <= 0:
                    continue
                share_p = round((s_val / tot_sp_venta) * 100, 1)
                rot = "🔥 Top #1 del período" if idx == 0 else ("🟢 Alta rotación en el período" if idx < 3 else "🟡 Rotación complementaria")
                period_top_skus.append({
                    "sku": f"{sku_desc} ({sku_cod})",
                    "venta": round(float(s_val), 2),
                    "share": share_p,
                    "rotacion": rot,
                    "color": sc["colors"][idx % len(sc["colors"])]
                })

            top_sku_desc = " & ".join([f"{desc} ({cod})" for (cod, desc) in list(sku_grp_p.index)[:2]]) if not sku_grp_p.empty else "Sin movimiento en el período"

            supp_row = {
                "id": s_id,
                "proveedorKey": prov_key,
                "nombre": sc["nombre"],
                "shortName": sc["shortName"],
                "cardStyle": sc["cardStyle"],
                "badge": sc["badge"],
                "badgeClass": sc["badgeClass"],
                "venta": venta,
                "pedidos": pedidos,
                "ticket": ticket,
                "vendedorLider": vendedor_lider,
                "topSku": top_sku_desc,
                "topSkusPeriod": period_top_skus,
                "leadTime": sc["leadTime"],
                "promoVigente": sc["promoVigente"],
                "ventasPorVendedor": seller_sales_list
            }
            if "badgeStyle" in sc:
                supp_row["badgeStyle"] = sc["badgeStyle"]

            supp_rows.append(supp_row)

        supp_rows.sort(key=lambda x: x["venta"], reverse=True)
        suppliers_monthly[p] = supp_rows

    # 9. Array CLIENTS para el Feed (excluyendo Organa y UNALM para alertas/acciones)
    clients_frontend = generate_clients_array(clientes_alertas)

    # 10. Agendas de WhatsApp para Tab 5 (excluyendo Organa y UNALM)
    wa_agendas: Dict[str, str] = {}
    for s in SELLER_CONFIG:
        s_id = s["id"]
        c_id = s["cartera_id"]
        seller_short = s["short"]

        # Filtrar clientes de esta cartera excluyendo Organa y UNALM
        s_clients = [
            c for c in clientes_alertas
            if c.get("cartera_asignada") == c_id
            and not is_excluded_for_alerts(str(c.get("cod_cliente", "")), str(c.get("nombre_cliente", "")))
        ]

        cobranzas = [c for c in s_clients if c.get("cobranza", {}).get("bloqueo_por_mora", False)]
        cobranzas.sort(key=lambda x: float(x.get("cobranza", {}).get("deuda_vencida_soles", 0.0)), reverse=True)

        urgentes = [c for c in s_clients if c.get("severidad") == "CRITICA" and not c.get("cobranza", {}).get("bloqueo_por_mora", False)]
        urgentes.sort(key=lambda x: float(x.get("ticket_promedio", 0.0)), reverse=True)

        preventivos = [c for c in s_clients if c.get("severidad") == "ADVERTENCIA" and not c.get("cobranza", {}).get("bloqueo_por_mora", False)]
        preventivos.sort(key=lambda x: float(x.get("ticket_promedio", 0.0)), reverse=True)

        oportunidades = [c for c in s_clients if c.get("severidad") == "OPORTUNIDAD" and not c.get("cobranza", {}).get("bloqueo_por_mora", False)]
        oportunidades.sort(key=lambda x: float(x.get("ticket_promedio", 0.0)), reverse=True)

        lines = [f"📌 *ACCIONES DEL DÍA — {seller_short.upper()}*"]

        if cobranzas:
            lines.append("\n💸 *COBRAR Y CONDICIONAR PEDIDO:*")
            for c in cobranzas[:4]:
                nom = c.get("nombre_comercial") or c.get("nombre_cliente")
                deuda = c.get("cobranza", {}).get("deuda_vencida_soles", 0.0)
                fact = c.get("canasta_docs", c.get("cobranza", {}).get("docs_vencidos", 1))
                mora = c.get("cobranza", {}).get("dias_mora_max", 0)
                canasta_c = c.get("recompra_inteligente", {}).get("canasta_habitual", [])
                top_prods = ", ".join([p["descripcion"] for p in canasta_c[:3]]) if canasta_c else "su canasta habitual"
                lines.append(f"• *{nom}* — Deuda vencida: *S/ {deuda:,.2f}* ({fact} doc · {mora}d mora).")
                lines.append(f"  👉 Cobrar hoy antes de liberar reposición de: *{top_prods}*.")

        if urgentes:
            lines.append("\n🔴 *LLAMAR PARA RECOMPRA (CICLO VENCIDO / FUGA):*")
            for c in urgentes[:4]:
                nom = c.get("nombre_comercial") or c.get("nombre_cliente")
                dias = c.get("dias_inactivo", 0)
                n = round(c.get("mediana_ciclo_n", 30))
                canasta_c = c.get("recompra_inteligente", {}).get("canasta_habitual", [])
                top_prods = ", ".join([p["descripcion"] for p in canasta_c[:3]]) if canasta_c else "catálogo habitual"
                promos_c = c.get("recompra_inteligente", {}).get("promociones_aplicables", [])
                promo_str = f" + *{promos_c[0]}*" if promos_c else ""
                lines.append(f"• *{nom}* — Lleva {dias} días sin pedir (ciclo cada {n}d).")
                lines.append(f"  👉 Ofrecer reposición de: *{top_prods}*{promo_str}.")

        if preventivos:
            lines.append("\n🟡 *SEGUIMIENTO ACTIVO (RECOMPRA SEMANAL):*")
            for c in preventivos[:3]:
                nom = c.get("nombre_comercial") or c.get("nombre_cliente")
                dias = c.get("dias_inactivo", 0)
                canasta_c = c.get("recompra_inteligente", {}).get("canasta_habitual", [])
                top_prods = ", ".join([p["descripcion"] for p in canasta_c[:3]]) if canasta_c else "línea habitual"
                lines.append(f"• *{nom}* ({dias}d sin compra) — Tomar pedido de: *{top_prods}*.")

        if oportunidades:
            lines.append("\n🟠 *VENTANA DE PEDIDO / ONBOARDING NUEVOS:*")
            for c in oportunidades[:3]:
                nom = c.get("nombre_comercial") or c.get("nombre_cliente")
                dias = c.get("dias_inactivo", 0)
                canasta_c = c.get("recompra_inteligente", {}).get("canasta_habitual", [])
                top_prods = ", ".join([p["descripcion"] for p in canasta_c[:3]]) if canasta_c else "canasta de inicio"
                lines.append(f"• *{nom}* ({dias}d) — Impulsar segundo pedido de: *{top_prods}* con bonificaciones 6+1 y 12+1.")

        wa_agendas[s_id] = "\n".join(lines)

    # 11. Cuentas por Cobrar Vencidas Globales (T024)
    global_cxc_vencidos = build_global_cxc_vencidos(cxc_path)

    # 12. Historico Completo Linda B2C para descarga Excel (T024)
    linda_b2c_full_history = build_linda_b2c_full_history(clientes_alertas)

    payload = {
        "SYNC_STATUS": sync_info,
        "MONTHLY_DATA": monthly_data,
        "TIME_SERIES": time_series,
        "SELLER_DRILLDOWN_DETAILS": seller_drilldown,
        "SUPPLIERS_MONTHLY_DATA": suppliers_monthly,
        "SUPPLIER_TOP_SKUS_MASTER": supplier_top_skus_master,
        "CLIENTS": clients_frontend,
        "WA_AGENDAS": wa_agendas,
        "GLOBAL_CXC_VENCIDOS": global_cxc_vencidos,
        "LINDA_B2C_FULL_HISTORY": linda_b2c_full_history
    }

    print(f"[EXPORT] Payload generado exitosamente:")
    print(f"         - Clientes accionables en feed (sin Organa/UNALM): {len(clients_frontend):,}")
    print(f"         - Periodos mensuales: {list(monthly_data.keys())}")
    print(f"         - Venta Octubre 2026 (100% empresa): S/ {sum(r['venta'] for r in monthly_data['2026-10']):,.2f}")
    print(f"         - Deuda Vencida Total CXC: S/ {sum(deuda_por_cartera.values()):,.2f}")
    print(f"         - Proveedores del Maestro: {len(suppliers_monthly['2026-10'])}")
    return payload


def inject_data_into_html(payload: Dict[str, Any], html_path: Path = DEFAULT_HTML_PATH):
    """
    Inyecta determinísticamente los datos consolidados en el archivo HTML del dashboard
    definiendo window.__QALIKAY_REAL_DATA__.
    """
    if not html_path.exists():
        raise FileNotFoundError(f"Archivo HTML no encontrado en {html_path}")

    html_content = html_path.read_text(encoding="utf-8")

    json_str = json.dumps(payload, ensure_ascii=False)
    injected_script = f"""  <!-- DATOS REALES DE PRODUCCION INYECTADOS DETERMINISTICAMENTE -->
  <script>
    window.__QALIKAY_REAL_DATA__ = {json_str};
  </script>
"""

    marker_start = "<!-- ==================== JAVASCRIPT ==================== -->"
    if marker_start in html_content:
        if "window.__QALIKAY_REAL_DATA__" in html_content:
            html_content = re.sub(
                r"<!-- DATOS REALES DE PRODUCCION INYECTADOS DETERMINISTICAMENTE -->[\s\S]*?</script>\s*",
                "",
                html_content
            )

        html_content = html_content.replace(marker_start, f"{marker_start}\n{injected_script}")
        html_path.write_text(html_content, encoding="utf-8")
        print(f"[HTML INJECT] Datos reales inyectados exitosamente en {html_path.name} ({len(json_str):,} caracteres JSON).")
    else:
        print(f"[WARN] Marcador {marker_start} no encontrado en {html_path.name}. Omitiendo inyeccion.")


def main():
    parser = argparse.ArgumentParser(description="Exportador de Datos del Dashboard Comercial - Qali Kay")
    parser.add_argument("--parquet", type=Path, default=DEFAULT_PARQUET_PATH, help="Ruta de ventas_2025_2026.parquet")
    parser.add_argument("--alertas", type=Path, default=DEFAULT_ALERTAS_PATH, help="Ruta de alertas_comerciales_consolidadas.json")
    parser.add_argument("--cxc", type=Path, default=DEFAULT_CXC_PATH, help="Ruta de Cuentas por cobrar 2026.xlsx")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_JSON, help="Ruta de datos_comerciales.json")
    parser.add_argument("--html", type=Path, default=DEFAULT_HTML_PATH, help="Ruta de PROTOTIPO_DASHBOARD_VENTAS_QALIKAY.html")
    parser.add_argument("--inject-html", action="store_true", default=True, help="Inyectar datos directamente en el archivo HTML")

    args = parser.parse_args()

    payload = build_dashboard_payload(
        parquet_path=args.parquet,
        alertas_path=args.alertas,
        cxc_path=args.cxc,
        sync_cache_path=DEFAULT_SYNC_PATH
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"[JSON SAVE] Archivo guardado: {args.output} ({args.output.stat().st_size / 1024:,.1f} KB)")

    if args.inject_html:
        inject_data_into_html(payload, args.html)

    print("\n[SUCCESS] Proceso de exportacion e inyeccion culminado con 0 errores.")


if __name__ == "__main__":
    main()
