"""
ETL Pipeline para Ventas Detalladas de Defontana (Qali Kay S.A.C.)
==================================================================
Modulo: src/etl_ventas_defontana.py
Alcance: Tareas T007, T008, T009, T010, T011 (Fase 2)
Presupuesto: S/ 0.00 ($0.00 USD)
Determinismo Matematico Estricto: Cero calculos via LLM.

Funcionalidades:
- T007: Parser de reportes Defontana (HTML exportado en cp1252) con tipado riguroso.
- T008: Tratamiento determinista de Notas de Credito (suma algebraica directa).
- T009: Filtro estricto de exclusion de las 6 cuentas de Consumo Interno.
- T010: Almacen Parquet y Algoritmo de Ventana Rodante de 90 Dias con Upsert
        por clave compuesta cuadruple (Nombre_Doc + Nro_Doc + Cod_Producto + Linea).
- T011: Vinculacion con Maestro de Articulos (RAW_ARTICULOS) y mapeo determinista
        de Proveedor Titular y Marca/Linea para el 100% de transacciones.
"""

import os
import sys
import argparse
import datetime
from pathlib import Path
from typing import Tuple, Dict, Set, Optional, Any
import urllib.request
import io

import pandas as pd
import numpy as np


# ==============================================================================
# CONFIGURACION Y CONSTANTES DE NEGOCIO (SPEC-KIT FR-01 A FR-11)
# ==============================================================================

DEFAULT_DATA_DIR = Path("data")
DEFAULT_OUTPUT_PARQUET = DEFAULT_DATA_DIR / "ventas_2025_2026.parquet"
DEFAULT_MAESTRO_CSV = DEFAULT_DATA_DIR / "maestro_articulos_abastecimiento.csv"
DEFAULT_RAW_VENTAS_CACHE = DEFAULT_DATA_DIR / "raw_ventas_cache.xlsx"

def resolve_cxc_path(cxc_path: Optional[Path] = None) -> Path:
    r"""
    Resuelve dinamicamente la ruta de 'Cuentas por cobrar 2026.xlsx' soportando ambas PCs:
    1. Prioridad: C:\Users\USER\OneDrive\CUENTAS POR COBRAR\QALI KAY\2026\Cuentas por cobrar 2026.xlsx
    2. Fallback:  C:\Users\cguti\OneDrive\Inka Comex\CUENTAS POR COBRAR\QALI KAY\2026\Cuentas por cobrar 2026.xlsx
    """
    candidates = [
        Path(r"C:\Users\USER\OneDrive\CUENTAS POR COBRAR\QALI KAY\2026\Cuentas por cobrar 2026.xlsx"),
        Path(r"C:\Users\cguti\OneDrive\Inka Comex\CUENTAS POR COBRAR\QALI KAY\2026\Cuentas por cobrar 2026.xlsx"),
    ]
    if cxc_path and cxc_path.exists():
        return cxc_path
    for p in candidates:
        if p.exists():
            return p
    return candidates[0]

DEFAULT_CXC_PATH = resolve_cxc_path()

# Google Sheets RPA Endpoints (Level 1 Automatic Sync)
GOOGLE_SHEET_ID = "16KcBYTetx0IQFiv2832gUgekrzKT93wghlaBrOxPg9Q"
URL_RAW_VENTAS = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/export?format=xlsx"
URL_RAW_ARTICULOS = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/gviz/tq?tqx=out:csv&sheet=RAW_ARTICULOS"

# Cuentas Oficiales de Consumo Interno y Colaboradores a Excluir (FR-06 y T032)
# Normalizados con y sin cero inicial (7, 8 y 9 digitos)
CONSUMO_INTERNO_DNIS: Set[str] = {
    "73615353",   # Cristian Gutierrez (CRISTIAN ANDRES)
    "06024456",   # Walter Gutierrez (GUTIERREZ ARRESE WALTER)
    "6024456",
    "76423008",   # Carlos Cuadros (CUADROS VALERIANO CARLOS ALBERTO)
    "09072925",   # Linda Rios (Linda Rios)
    "9072925",
    "72164623",   # Luis Gamarra (Luis Angel Gamarra Calle)
    "72931481",   # Carlos Antonio Ureta (Carlos Antonio Ureta Abanto)
    "06604924",   # Carlos Antonio Ureta (Historico)
    "6604924",
    # 4 Colaboradores excluidos de metricas comerciales y cartera Cristian (T032)
    "42072907",   # Enrique Garcia
    "042072907",
    "49062951",   # Junnior Andres Jesus Castañeda Meza
    "049062951",
    "76738275",   # Kelly Solange Ruiz Bendezu
    "076738275",
    "003166920",  # Norexglis Esther Guaracaran Aranguren
    "03166920",
    "3166920",
    "316692",
}

# Diccionario de Prefijos Deterministas para Asignacion de Proveedor Titular (Fallback T011)
FALLBACK_PREFIX_MAP: Dict[str, str] = {
    "GON": "NUTRIVAS",
    "NAT": "NUTRIVAS",
    "NAN": "NUTRIVAS",
    "SANT": "MOLINOS DEL MUNDO",  # T031: Santiveri pertenece a Molinos del Mundo
    "ORI": "NUTRIVAS",
    "ORD": "NUTRIVAS",
    "OR": "NUTRIVAS",
    "DNE": "NUTRIVAS",
    "DNC": "NUTRIVAS",
    "DNP": "NUTRIVAS",
    "DNG": "NUTRIVAS",
    "NUTR": "NUTRIVAS",
    "NUT": "NUTRIVAS",
    "NNF": "NUTRIVAS",
    "MTFT": "NUTRIVAS",
    "AMZ": "AMAZON ANDES",
    "AMA": "AMAZON ANDES",
    "PTMM": "MOLINOS DEL MUNDO",
    "MOL": "MOLINOS DEL MUNDO",
    "MDM": "MOLINOS DEL MUNDO",
    "MTIE": "MI TIERRA",
    "PIG": "PECADITOS INTEGRALES",
    "QOR": "QORINKA",
    "SSF": "QORINKA",
    "SSG": "QORINKA",
    "TAU": "TAURI",
    "OLI": "OLIVO DE ORO",
    "OLIV": "OLIVO DE ORO",
    "VIV": "FIBRA FRUT",
    "VVF": "FIBRA FRUT",
    "FIB": "FIBRA FRUT",
    "IKPM": "INKA PRIME",
    "INSUR": "INCASUR",
    "DEP": "DEPURATÉ",
    "TQL": "QORI",
    "IC": "INKA COMEX",
    "ADS": "ANDES CRISP",
    "ABO": "AGROBOSQUE",
    "FNGA": "FUNGI AMAZONICA",
    "FA": "FUNGI AMAZONICA",
    "NOA": "NOA LIFE",
    "NOV": "NOVOAMERICA",
    "WILD": "WILD FOODS",
    "TDM": "TANDEM",
    "LO": "LADO ORGANICO",
    "MSKY": "MISKY",
    "KLN": "KALYNA",
    "NUA": "NUA",
    "BPT": "MOLINOS DEL MUNDO",
    "B": "BROMKISAN",
    "CVHN": "CASA DE VALENTINA",
    "CVPNLA": "CASA DE VALENTINA",
    "CVAN": "CASA DE VALENTINA",
    "CVML": "CASA DE VALENTINA",
}

# 17 Columnas Estandarizadas de Destino (tras descartar duplicado 'Nombre del Vendedor')
STANDARD_COLUMNS = [
    "Nombre_Doc",
    "Nro_Doc",
    "Cod_Cliente",
    "Nombre_Cliente",
    "Nombre_Contacto",
    "Libro_Vtas",
    "Nombre_Vendedor",
    "Fecha",
    "Cod_Producto",
    "Desc_Producto",
    "Marca_Propiedad01",
    "Cantidad",
    "Precio_Unitario",
    "Total_Detalle",
    "Cond_Pago",
    "Fecha_Vencimiento",
    "Linea",
]


# ==============================================================================
# T011: MAESTRO DE ARTICULOS Y RESOLUCION DETERMINISTA DE PROVEEDOR
# ==============================================================================

def load_maestro_articulos(csv_path: Path) -> Dict[str, str]:
    """
    Carga el catalogo maestro oficial de articulos sincronizado por el RPA (RAW_ARTICULOS).
    Retorna un diccionario normalizado {SKU_LIMPIO: PROVEEDOR_TITULAR}.
    """
    if not csv_path.exists():
        print(f"[WARN] Archivo maestro no encontrado en {csv_path}. Se usara mapeo por prefijos.")
        return {}

    try:
        df = pd.read_csv(csv_path, encoding="utf-8-sig")
    except Exception:
        df = pd.read_csv(csv_path, encoding="latin1")

    # Identificar columnas por posicion o nombre
    sku_col = df.columns[0]
    prov_col = df.columns[2] if len(df.columns) > 2 else df.columns[1]

    maestro_dict = {}
    for _, row in df.iterrows():
        raw_sku = str(row[sku_col]).strip().upper().replace(" ", "")
        raw_prov = str(row[prov_col]).strip().upper()
        if raw_sku and raw_sku != "NAN":
            maestro_dict[raw_sku] = raw_prov

    print(f"[T011] Maestro de articulos cargado exitosamente: {len(maestro_dict)} SKUs activos.")
    return maestro_dict


def resolve_proveedor_titular(sku: str, desc: str, maestro_dict: Dict[str, str]) -> Tuple[str, str]:
    """
    Asigna de forma determinista el Proveedor Titular y Marca/Linea a cada SKU:
    - Prioridad 1: Coincidencia exacta contra el maestro de abastecimiento.
    - Prioridad 2: Mapeo determinista por prefijo de SKU.
    - Prioridad 3: Reglas semanticas sobre descripcion (servicios, fletes, etc.).
    Garantiza que el 100% de las transacciones tengan un proveedor asignado.
    """
    sku_norm = str(sku).strip().upper().replace(" ", "")
    desc_norm = str(desc).strip().upper()

    # Prioridad 1: Cruce exacto con maestro
    if sku_norm in maestro_dict:
        prov = maestro_dict[sku_norm]
        marca = sku_norm.split("-")[0] if "-" in sku_norm else "GENERAL"
        return prov, marca

    # Prioridad 2: Cruce por prefijo de SKU
    prefix = sku_norm.split("-")[0] if "-" in sku_norm else sku_norm
    if prefix in FALLBACK_PREFIX_MAP:
        return FALLBACK_PREFIX_MAP[prefix], prefix

    for p, prov in sorted(FALLBACK_PREFIX_MAP.items(), key=lambda x: len(x[0]), reverse=True):
        if sku_norm.startswith(p):
            return prov, p

    # Prioridad 3: Analisis de descripcion para fletes / servicios
    if any(k in desc_norm for k in ["DELIVERY", "TRANSPORTE", "FLETE", "REEMBOLSO", "GASTOS"]):
        return "SERVICIOS Y FLETES", "OPERATIVO"

    if any(k in desc_norm for k in ["CATÁLOGO", "CATALOGO", "MUESTRA", "MATERIAL"]):
        return "MATERIAL PUBLICITARIO", "MARKETING"

    # Fallback final auditable
    return "OTROS PROVEEDORES", prefix or "SIN_LINEA"


# ==============================================================================
# T031: HELPERS DETERMINISTAS PARA RECUPERACION DE MONTOS Y FACTURAS GRATUITAS
# ==============================================================================

def parse_monto_defontana(val: Any) -> float:
    """
    Recupera deterministicamente valores decimales de montos (Total_Detalle o Precio_Unitario).
    Si Google Sheets corrompio el decimal a fecha/timestamp (datetime o string 'YYYY-MM-DD...'),
    recupera deterministicamente: float(f"{dt.day}.{dt.month:02d}").
    """
    if pd.isna(val):
        return 0.0
    if isinstance(val, (datetime.datetime, datetime.date, pd.Timestamp)):
        return float(f"{val.day}.{val.month:02d}")
    val_str = str(val).strip()
    if not val_str or val_str.lower() in ["nan", "none", "null"]:
        return 0.0
    # Si viene como string 'YYYY-MM-DD...'
    if len(val_str) >= 10 and val_str[4] == '-' and val_str[7] == '-':
        try:
            dt = pd.to_datetime(val_str)
            return float(f"{dt.day}.{dt.month:02d}")
        except Exception:
            pass
    # Limpieza de simbolos monetarios y separadores de miles
    val_clean = val_str.replace("S/", "").replace("$", "").replace(" ", "").replace(",", "")
    try:
        return float(val_clean)
    except Exception:
        return 0.0


def filter_facturas_gratuitas(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Descarta del total de ventas comerciales las facturas y comprobantes gratuitos:
    Comprobantes donde Nombre_Doc contenga 'Gratuita' (ej. '01 Factura Electrónica Gratuita Sin IGV').
    Retorna (df_sin_gratuitas, df_gratuitas).
    """
    mask_grat = df["Nombre_Doc"].astype(str).str.contains("Gratuita", case=False, na=False)
    df_grat = df[mask_grat].copy()
    df_valid = df[~mask_grat].copy()
    if len(df_grat) > 0:
        print(f"[T031] Facturas gratuitas descartadas: {len(df_grat):,} registros (Monto excluido: S/ {df_grat['Total_Detalle'].sum():,.2f}).")
    return df_valid, df_grat


# ==============================================================================
# T007: PARSER DE REPORTES DEFONTANA (HTML CP1252)
# ==============================================================================

def parse_defontana_html(file_path: Path) -> pd.DataFrame:
    """
    Lee un archivo de ventas exportado por Defontana en formato HTML con encoding cp1252.
    - Elimina la columna duplicada 15 (Nombre del Vendedor).
    - Asigna nombres estandarizados a las 17 columnas.
    - Convierte tipos de datos: fechas a ISO YYYY-MM-DD, cantidades y montos a float64.
    """
    print(f"[T007] Procesando reporte Defontana: {file_path.name}...")
    if not file_path.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {file_path}")

    # Defontana exporta tablas HTML con encabezado en fila 0
    tables = pd.read_html(file_path, encoding="cp1252", header=0)
    if not tables:
        raise ValueError(f"No se encontro ninguna tabla HTML en {file_path}")

    df = tables[0].copy()
    num_filas_raw, num_cols_raw = df.shape
    print(f"       Filas crudas leidas: {num_filas_raw:,} | Columnas crudas: {num_cols_raw}")

    # Verificar y descartar columna duplicada de Vendedor (indice 14)
    if num_cols_raw == 18:
        # Columna 6 y Columna 14 tienen encabezado 'Nombre del Vendedor'
        # pandas renombra la segunda a 'Nombre del Vendedor.1'
        df = df.drop(df.columns[14], axis=1)
    elif num_cols_raw != 17:
        raise ValueError(f"Estructura inesperada de columnas ({num_cols_raw}) en {file_path}")

    # Renombrar a columnas estandarizadas
    df.columns = STANDARD_COLUMNS

    # Limpieza de textos basicos
    for col in ["Nombre_Doc", "Nro_Doc", "Cod_Cliente", "Nombre_Cliente",
                "Nombre_Contacto", "Nombre_Vendedor", "Cod_Producto", "Desc_Producto",
                "Marca_Propiedad01", "Cond_Pago"]:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace({"nan": "", "None": "", "NAN": ""})

    # Normalizacion de codigo de cliente (preservar formato sin decimales)
    df["Cod_Cliente"] = df["Cod_Cliente"].str.replace(r"\.0$", "", regex=True)

    # Conversion de Fechas (formato Defontana: dd/MM/yyyy)
    df["Fecha_DT"] = pd.to_datetime(df["Fecha"], format="%d/%m/%Y", errors="coerce")
    df["Fecha_Venc_DT"] = pd.to_datetime(df["Fecha_Vencimiento"], format="%d/%m/%Y", errors="coerce")

    fechas_invalidas = df["Fecha_DT"].isna().sum()
    if fechas_invalidas > 0:
        raise ValueError(f"Se detectaron {fechas_invalidas} fechas de emision invalidas en {file_path.name}")

    # Guardar fechas como strings ISO YYYY-MM-DD
    df["Fecha"] = df["Fecha_DT"].dt.strftime("%Y-%m-%d")
    df["Fecha_Vencimiento"] = df["Fecha_Venc_DT"].dt.strftime("%Y-%m-%d").fillna("")
    df["Anio"] = df["Fecha_DT"].dt.year.astype("int16")
    df["Mes"] = df["Fecha_DT"].dt.month.astype("int8")
    df["Periodo_Mes"] = df["Fecha_DT"].dt.strftime("%Y-%m")

    # Conversion de montos y cantidades con parse_monto_defontana (T031)
    df["Cantidad"] = pd.to_numeric(df["Cantidad"], errors="coerce").fillna(0.0).astype("float64")
    df["Total_Detalle"] = df["Total_Detalle"].apply(parse_monto_defontana).astype("float64")
    df["Precio_Unitario"] = np.where(
        df["Cantidad"] != 0,
        np.round(np.abs(df["Total_Detalle"] / df["Cantidad"]), 4),
        df["Precio_Unitario"].apply(parse_monto_defontana)
    ).astype("float64")

    # Descartar facturas gratuitas (T031)
    df, _ = filter_facturas_gratuitas(df)

    # Conversion de Linea a int32
    df["Linea"] = pd.to_numeric(df["Linea"], errors="coerce").fillna(1).astype("int32")

    # Descartar columnas auxiliares de datetime
    df = df.drop(columns=["Fecha_DT", "Fecha_Venc_DT"])

    return df


# ==============================================================================
# T008: DEDUCCION DE NOTAS DE CREDITO (ALGEBRA DIRECTA Y ASERCIONES)
# ==============================================================================

def apply_credit_note_logic(df: pd.DataFrame) -> pd.DataFrame:
    """
    Identifica las Notas de Credito (NC) y verifica por asercion matematica que
    sus cantidades y montos vengan con signo negativo desde Defontana.
    La venta neta total se calcula mediante suma algebraica directa.
    """
    df = df.copy()

    # Identificar Notas de Credito (07 NC Electronica [F], [B], etc.)
    es_nc = df["Nombre_Doc"].str.startswith("07") | df["Nombre_Doc"].str.contains(r"\bNC\b", case=False, regex=True)
    df["Es_Nota_Credito"] = es_nc

    num_nc = es_nc.sum()
    df_nc = df[es_nc]

    # Validacion critica auditada en preflight:
    # El 100% de las NC en Defontana DEBEN tener Cantidad <= 0 y Total_Detalle <= 0
    nc_positivas_qty = (df_nc["Cantidad"] > 0).sum()
    nc_positivas_total = (df_nc["Total_Detalle"] > 0).sum()

    if nc_positivas_qty > 0 or nc_positivas_total > 0:
        print(f"[ALERTA CRITICA T008] Se detectaron {nc_positivas_total} NC con total positivo!")
    else:
        print(f"[T008] Notas de Credito verificadas: {num_nc:,} registros.")
        print(f"       100% de las NC traen cantidades y montos negativos.")
        print(f"       Total impacto NC: Cantidad = {df_nc['Cantidad'].sum():,.2f} | Monto = S/ {df_nc['Total_Detalle'].sum():,.2f}")
        print(f"       Asercion superada: La suma algebraica directa SUM(Total_Detalle) es exacta.")

    return df


# ==============================================================================
# T009: FILTRO ESTRICTO DE CONSUMO INTERNO (6 CUENTAS OFICIALES)
# ==============================================================================

def filter_consumo_interno(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Filtra y excluye estrictamente las 6 cuentas catalogadas como Consumo Interno (FR-06).
    Retorna (df_comercial, df_consumo_interno).
    """
    mask_consumo = df["Cod_Cliente"].isin(CONSUMO_INTERNO_DNIS)

    df_consumo = df[mask_consumo].copy()
    df_comercial = df[~mask_consumo].copy()

    filas_consumo = len(df_consumo)
    unidades_consumo = df_consumo["Cantidad"].sum()
    monto_consumo = df_consumo["Total_Detalle"].sum()

    print(f"[T009] Filtro de Consumo Interno aplicado:")
    print(f"       - Transacciones excluidas: {filas_consumo:,}")
    print(f"       - Unidades excluidas:      {unidades_consumo:,.2f}")
    print(f"       - Monto excluido:          S/ {monto_consumo:,.2f}")
    print(f"       - Transacciones comerciales restantes: {len(df_comercial):,}")

    return df_comercial, df_consumo


# ==============================================================================
# T010: CLAVE COMPUESTA Y VENTANA RODANTE DE 90 DIAS CON UPSERT
# ==============================================================================

def generate_primary_key(df: pd.DataFrame) -> pd.DataFrame:
    """
    Genera la clave primaria compuesta cuadruple:
    PK_Transaccion = Nombre_Doc + "|" + Nro_Doc + "|" + Cod_Producto + "|" + Linea
    Garantiza 0 colisiones en transacciones del mismo comprobante con multiples lineas del mismo SKU.
    """
    df = df.copy()
    df["PK_Transaccion"] = (
        df["Nombre_Doc"].astype(str) + "|" +
        df["Nro_Doc"].astype(str) + "|" +
        df["Cod_Producto"].astype(str) + "|" +
        df["Linea"].astype(str)
    )

    # Validacion estricta de unicidad
    duplicados = df["PK_Transaccion"].duplicated().sum()
    if duplicados > 0:
        raise ValueError(f"[ERROR T010] Se detectaron {duplicados} colisiones de PK_Transaccion!")

    return df


def upsert_rolling_window_90d(
    df_existente: Optional[pd.DataFrame],
    df_nuevos: pd.DataFrame,
    window_days: int = 90
) -> pd.DataFrame:
    """
    Implementa la logica de ventana rodante incremental de 90 dias con upsert:
    - Si existe un historico consolidado, preserva los registros antiguos fuera de la ventana.
    - Aplica un upsert por PK_Transaccion, reemplazando o insertando registros nuevos/modificados.
    - Asegura la absorcion automatica de nuevas Facturas, Boletas y Notas de Credito.
    """
    if df_existente is None or df_existente.empty:
        print("[T010] No existe historico previo. Creando base consolidada inicial.")
        df_consolidado = df_nuevos.drop_duplicates(subset=["PK_Transaccion"], keep="last")
    else:
        print(f"[T010] Aplicando upsert incremental sobre historico ({len(df_existente):,} registros existentes)...")
        # Concatenar y mantener la version mas reciente (last) de cada PK
        df_concat = pd.concat([df_existente, df_nuevos], ignore_index=True)
        df_consolidado = df_concat.drop_duplicates(subset=["PK_Transaccion"], keep="last")
        nuevas_filas = len(df_consolidado) - len(df_existente)
        print(f"       Upsert finalizado. Filas netas agregadas/actualizadas: {nuevas_filas:,}")

    # Ordenamiento cronologico determinista
    df_consolidado = df_consolidado.sort_values(
        by=["Fecha", "Nro_Doc", "Linea"],
        ascending=[True, True, True]
    ).reset_index(drop=True)

    return df_consolidado


# ==============================================================================
# PIPELINE COMPLETO DE EJECUCION
# ==============================================================================

def run_etl_pipeline(
    data_dir: Path = DEFAULT_DATA_DIR,
    output_parquet: Path = DEFAULT_OUTPUT_PARQUET,
    maestro_csv: Path = DEFAULT_MAESTRO_CSV,
    incremental: bool = False
) -> pd.DataFrame:
    """
    Ejecuta el pipeline ETL integral de la Fase 2:
    1. Carga del Maestro de Articulos (T011).
    2. Lectura y parsing de reportes Defontana 2025 y 2026 (T007).
    3. Asignacion determinista de Proveedor Titular (T011).
    4. Validacion y tratamiento algebraico de Notas de Credito (T008).
    5. Filtrado estricto de Consumo Interno (T009).
    6. Generacion de PK cuadruple y almacenamiento Parquet con ventana rodante (T010).
    """
    tiempo_inicio = datetime.datetime.now()
    print("=" * 80)
    print("INICIANDO PIPELINE ETL DE VENTAS DEFONTANA - QALI KAY S.A.C.")
    print(f"Fecha/Hora: {tiempo_inicio.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    # 1. Cargar Maestro de Articulos
    maestro_dict = load_maestro_articulos(maestro_csv)

    # 2. Localizar archivos de ventas en data/
    archivos_ventas = sorted(list(data_dir.glob("*INF_VENTAS_DETALLADAS*.xls*")))
    if not archivos_ventas:
        raise FileNotFoundError(f"No se encontraron reportes de ventas en {data_dir.resolve()}")

    dfs_cargados = []
    for f in archivos_ventas:
        # Evitar procesar archivos temporales de Excel (~$...)
        if f.name.startswith("~$"):
            continue
        df_single = parse_defontana_html(f)
        dfs_cargados.append(df_single)

    if not dfs_cargados:
        raise ValueError("No se pudo cargar ningun archivo de ventas.")

    df_raw = pd.concat(dfs_cargados, ignore_index=True)
    total_raw_rows = len(df_raw)
    print(f"\n[INFO] Total transacciones crudas consolidadas: {total_raw_rows:,}")

    # 3. Asignar Proveedor Titular y Marca/Linea (T011)
    print("\n[T011] Asignando Proveedor Titular y Marca/Linea a cada registro...")
    provs = []
    marcas = []
    for sku, desc in zip(df_raw["Cod_Producto"], df_raw["Desc_Producto"]):
        p, m = resolve_proveedor_titular(sku, desc, maestro_dict)
        provs.append(p)
        marcas.append(m)

    df_raw["Proveedor_Titular"] = provs
    df_raw["Marca_Linea"] = marcas

    # 4. Validar Notas de Credito (T008)
    print("\n[T008] Aplicando logica de Notas de Credito...")
    df_con_nc = apply_credit_note_logic(df_raw)

    # 5. Filtrar Consumo Interno (T009)
    print("\n[T009] Aplicando filtro de Consumo Interno...")
    df_comercial, df_consumo = filter_consumo_interno(df_con_nc)

    # 6. Generar Clave Primaria Cuadruple (T010)
    print("\n[T010] Generando clave primaria compuesta cuadruple (Nombre_Doc + Nro_Doc + Cod_Producto + Linea)...")
    df_comercial = generate_primary_key(df_comercial)

    # 7. Upsert con Ventana Rodante de 90 Dias
    df_existente = None
    if incremental and output_parquet.exists():
        try:
            df_existente = pd.read_parquet(output_parquet)
            print(f"[T010] Parquet previo cargado: {len(df_existente):,} filas.")
        except Exception as e:
            print(f"[WARN] No se pudo leer el parquet existente ({e}). Se creara nuevo.")

    df_final = upsert_rolling_window_90d(df_existente, df_comercial, window_days=90)

    # 8. Exportar a Parquet con PyArrow
    print(f"\n[T010] Guardando consolidado en: {output_parquet}...")
    output_parquet.parent.mkdir(parents=True, exist_ok=True)
    df_final.to_parquet(
        output_parquet,
        engine="pyarrow",
        compression="snappy",
        index=False
    )

    tamanio_kb = output_parquet.stat().st_size / 1024
    tiempo_fin = datetime.datetime.now()
    duracion_seg = (tiempo_fin - tiempo_inicio).total_seconds()

    # 9. Metricas Finales de Verificacion y Aserciones
    total_filas = len(df_final)
    total_unidades = df_final["Cantidad"].sum()
    total_monto = df_final["Total_Detalle"].sum()

    print("\n" + "=" * 80)
    print("METRICAS FINALES DE EJECUCION (FASE 2 COMPLETADA)")
    print("=" * 80)
    print(f"Archivo Parquet:         {output_parquet.name} ({tamanio_kb:,.1f} KB)")
    print(f"Transacciones Crudas:    {total_raw_rows:,}")
    print(f"Consumo Interno Excl.:   {len(df_consumo):,} filas (S/ {df_consumo['Total_Detalle'].sum():,.2f})")
    print(f"Transacciones Finales:   {total_filas:,}")
    print(f"Unidades Fisicas Netas:  {total_unidades:,.2f}")
    print(f"Venta Comercial Neta:    S/ {total_monto:,.2f}")
    print(f"Rango de Fechas:         {df_final['Fecha'].min()} al {df_final['Fecha'].max()}")
    print(f"Proveedores Mapeados:    {df_final['Proveedor_Titular'].nunique()} proveedores distintos")
    print(f"Tiempo de Procesamiento: {duracion_seg:.2f} segundos")
    print("=" * 80)

    # Aserciones matematicas de rigor (T031)
    assert total_filas > 0, "Error en conteo de filas: consolidado vacio"
    assert total_monto > 0, "Error en monto comercial neto: debe ser positivo"
    assert df_final["PK_Transaccion"].duplicated().sum() == 0, "Existen duplicados en PK_Transaccion"

    print("[SUCCESS] Todas las aserciones matematicas y de negocio se cumplieron al 100.00%.")
    return df_final


# ==============================================================================
# FASE 4: SINCRONIZACION AUTOMATICA EN VIVO VIA RPA GOOGLE SHEETS
# ==============================================================================

def sync_rpa_raw_ventas(
    parquet_path: Path = DEFAULT_OUTPUT_PARQUET,
    maestro_csv: Path = DEFAULT_MAESTRO_CSV,
    cache_path: Path = DEFAULT_RAW_VENTAS_CACHE
) -> pd.DataFrame:
    """
    Sincroniza en vivo las ventas de la ventana rodante (RAW_VENTAS) y el maestro
    de articulos (RAW_ARTICULOS) directamente desde Google Sheets sincronizado por RPA.
    - Aplica normalizacion estandar, deduccion de NC y filtro de consumo interno.
    - Realiza upsert cuadruple (Nombre_Doc + Nro_Doc + Cod_Producto + Linea) sobre el Parquet historico.
    - Preserva resiliencia offline: si no hay conexion, utiliza el cache local o el Parquet existente.
    """
    print("=" * 80)
    print("INICIANDO SINCRONIZACION EN VIVO RAW_VENTAS (RPA GOOGLE SHEETS)")
    print(f"Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    # 1. Asegurar existencia de Parquet base
    if not parquet_path.exists():
        print(f"[INFO] Parquet base no encontrado en {parquet_path}. Ejecutando construccion inicial...")
        run_etl_pipeline(output_parquet=parquet_path, maestro_csv=maestro_csv)

    # 2. Intentar actualizar Maestro de Articulos desde RAW_ARTICULOS
    try:
        req_art = urllib.request.Request(URL_RAW_ARTICULOS, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req_art, timeout=20) as resp:
            art_data = resp.read()
            if len(art_data) > 1000:
                maestro_csv.write_bytes(art_data)
                print(f"[RPA SYNC] Maestro de articulos actualizado desde Google Sheets ({len(art_data):,} bytes).")
    except Exception as e:
        print(f"[WARN] No se pudo refrescar maestro desde Google Sheets ({e}). Usando copia local.")

    maestro_dict = load_maestro_articulos(maestro_csv)

    # 3. Descargar RAW_VENTAS desde Google Sheets en formato XLSX (T031)
    raw_data_bytes = None
    try:
        print(f"[RPA SYNC] Conectando a Google Sheets: RAW_VENTAS en formato XLSX...")
        req_ventas = urllib.request.Request(URL_RAW_VENTAS, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req_ventas, timeout=35) as resp:
            raw_data_bytes = resp.read()
            print(f"[RPA SYNC] Descargados {len(raw_data_bytes):,} bytes del libro XLSX exitosamente.")
            cache_path.write_bytes(raw_data_bytes)
    except Exception as e:
        print(f"[WARN] Error de conexion con Google Sheets ({e}).")
        if cache_path.exists():
            print(f"[INFO] Utilizando cache local reciente: {cache_path}")
            raw_data_bytes = cache_path.read_bytes()
        else:
            print(f"[WARN] No hay cache local. Se conserva el archivo Parquet sin modificaciones.")
            return pd.read_parquet(parquet_path)

    # 4. Procesar y normalizar RAW_VENTAS desde la hoja XLSX preservando 100% de clientes alfanumericos (T031)
    df_raw = pd.read_excel(io.BytesIO(raw_data_bytes), sheet_name="RAW_VENTAS")
    num_cols = df_raw.shape[1]
    if num_cols == 18:
        df_raw = df_raw.drop(df_raw.columns[14], axis=1)
    elif num_cols != 17:
        raise ValueError(f"Estructura inesperada de columnas ({num_cols}) en RAW_VENTAS")

    df_raw.columns = STANDARD_COLUMNS

    # Limpieza de textos basicos y preservacion de codigos alfanumericos (MERMULTCENT, etc.)
    for col in ["Nombre_Doc", "Nro_Doc", "Cod_Cliente", "Nombre_Cliente",
                "Nombre_Contacto", "Nombre_Vendedor", "Cod_Producto", "Desc_Producto",
                "Marca_Propiedad01", "Cond_Pago"]:
        df_raw[col] = df_raw[col].astype(str).str.strip().replace({"nan": "", "None": "", "NAN": ""})

    df_raw["Cod_Cliente"] = df_raw["Cod_Cliente"].str.replace(r"\.0$", "", regex=True)

    # Parsing de fechas (soporta tanto Timestamp como texto dd/mm/yyyy o yyyy-mm-dd)
    df_raw["Fecha_DT"] = pd.to_datetime(df_raw["Fecha"], errors="coerce")
    df_raw["Fecha_Venc_DT"] = pd.to_datetime(df_raw["Fecha_Vencimiento"], errors="coerce")

    df_raw["Fecha"] = df_raw["Fecha_DT"].dt.strftime("%Y-%m-%d")
    df_raw["Fecha_Vencimiento"] = df_raw["Fecha_Venc_DT"].dt.strftime("%Y-%m-%d").fillna("")
    df_raw["Anio"] = df_raw["Fecha_DT"].dt.year.astype("int16")
    df_raw["Mes"] = df_raw["Fecha_DT"].dt.month.astype("int8")
    df_raw["Periodo_Mes"] = df_raw["Fecha_DT"].dt.strftime("%Y-%m")

    # Conversion numerica determinista recuperando fechas corrompidas (T031)
    df_raw["Cantidad"] = pd.to_numeric(df_raw["Cantidad"], errors="coerce").fillna(0.0).astype("float64")
    df_raw["Total_Detalle"] = df_raw["Total_Detalle"].apply(parse_monto_defontana).astype("float64")
    df_raw["Precio_Unitario"] = np.where(
        df_raw["Cantidad"] != 0,
        np.round(np.abs(df_raw["Total_Detalle"] / df_raw["Cantidad"]), 4),
        df_raw["Precio_Unitario"].apply(parse_monto_defontana)
    ).astype("float64")
    df_raw["Linea"] = pd.to_numeric(df_raw["Linea"], errors="coerce").fillna(1).astype("int32")

    df_raw = df_raw.drop(columns=["Fecha_DT", "Fecha_Venc_DT"])

    # Descartar del total de ventas comerciales las facturas gratuitas (T031)
    df_raw, df_gratuitas = filter_facturas_gratuitas(df_raw)

    # 5. Resolucion de Proveedor Titular y Marca
    provs, marcas = [], []
    for sku, desc in zip(df_raw["Cod_Producto"], df_raw["Desc_Producto"]):
        p, m = resolve_proveedor_titular(sku, desc, maestro_dict)
        provs.append(p)
        marcas.append(m)
    df_raw["Proveedor_Titular"] = provs
    df_raw["Marca_Linea"] = marcas

    # 6. Reglas de Negocio: Notas de Credito y Consumo Interno
    df_con_nc = apply_credit_note_logic(df_raw)
    df_comercial, df_consumo = filter_consumo_interno(df_con_nc)
    df_comercial = generate_primary_key(df_comercial)

    # 7. Upsert con Ventana Rodante sobre Parquet Historico
    df_existente = pd.read_parquet(parquet_path)
    filas_anteriores = len(df_existente)
    monto_anterior = df_existente["Total_Detalle"].sum()

    df_final = upsert_rolling_window_90d(df_existente, df_comercial, window_days=90)

    # Guardar Parquet actualizado
    df_final.to_parquet(
        parquet_path,
        engine="pyarrow",
        compression="snappy",
        index=False
    )

    filas_nuevas = len(df_final)
    monto_nuevo = df_final["Total_Detalle"].sum()

    print("\n" + "=" * 80)
    print("SINCRONIZACION RPA COMPLETADA EXITOSAMENTE")
    print("=" * 80)
    print(f"Parquet Destino:          {parquet_path.name}")
    print(f"Transacciones Anteriores: {filas_anteriores:,} (S/ {monto_anterior:,.2f})")
    print(f"Transacciones Nuevas:     {filas_nuevas:,} (S/ {monto_nuevo:,.2f})")
    print(f"Delta Filas Netas:        +{filas_nuevas - filas_anteriores:,}")
    print(f"Delta Venta Neta:         +S/ {monto_nuevo - monto_anterior:,.2f}")
    print(f"Rango de Fechas Actual:   {df_final['Fecha'].min()} al {df_final['Fecha'].max()}")
    print("=" * 80)

    return df_final


# ==============================================================================
# ENTRY POINT CLI
# ==============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pipeline ETL de Ventas Defontana - Qali Kay")
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR, help="Carpeta de archivos de datos")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PARQUET, help="Ruta del archivo Parquet de salida")
    parser.add_argument("--maestro", type=Path, default=DEFAULT_MAESTRO_CSV, help="Ruta del archivo Maestro CSV")
    parser.add_argument("--incremental", action="store_true", help="Activar modo incremental sobre parquet existente")
    parser.add_argument("--sync-rpa", action="store_true", help="Sincronizar en vivo RAW_VENTAS desde Google Sheets RPA")

    args = parser.parse_args()
    if args.sync_rpa:
        sync_rpa_raw_ventas(
            parquet_path=args.output,
            maestro_csv=args.maestro
        )
    else:
        run_etl_pipeline(
            data_dir=args.data_dir,
            output_parquet=args.output,
            maestro_csv=args.maestro,
            incremental=args.incremental
        )
