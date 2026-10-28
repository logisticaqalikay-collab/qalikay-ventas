# Feature Specification: 001 - Sistema de Inteligencia Comercial y Dashboard de Ventas B2B/B2C

**Código:** `QK-VENTAS-001`  
**Área:** Dirección Comercial y Operaciones  
**Responsable:** Cristian Gutiérrez (Director General)  
**Metodología:** Spec-Kit (`constitution` ➔ `specify` ➔ `clarify` ➔ `plan` ➔ `tasks` ➔ `analyze` ➔ `implement` ➔ `impeccable`)  
**Presupuesto:** S/ 0.00 ($0.00 USD)

---

## 1. Overview y Objetivos de Negocio
Construir el sistema integral de inteligencia comercial de Qali Kay S.A.C, que consolide las ventas de los años **2025 y 2026**, procese actualizaciones incrementales mediante una **ventana rodante de 90 días (3 meses)** aprovechando los reportes de Defontana descargados por el bot RPA existente (sin alterar su código), segmente a las **6 carteras comerciales** (incluyendo la bifurcación B2B vs B2C de Linda/Zully y la absorción de la cartera de Joel por Carlos Cuadros), evalúe los lead times de proveedores y genere alertas operativas y bandejas de WhatsApp limpias sin caracteres deformados, bajo una estricta política de **ahorro y eficiencia extrema de tokens**.

---

## 2. Requerimientos Funcionales (FR)

### MÓDULO 1: ARQUITECTURA DE DATOS Y ETL (BACKEND & STORAGE)
- **FR-01 (Consolidado Histórico 2025–2026):** Almacenar y consultar el histórico completo de ventas desde `01/01/2025` hasta el día en curso en formato Parquet (`data/ventas_2025_2026.parquet`). Los datos fuente se cargan desde los archivos oficiales en `data/`: `INF_VENTAS_DETALLADAS` 2025 (20,435 transacciones) y 2026 (17,598 transacciones), sumando 38,033 transacciones base.
- **FR-02 (Ventana Rodante Incremental de 90 Días):** Procesar diariamente los comprobantes de los últimos 90 días (3 meses) para absorber Notas de Crédito, devoluciones y anulaciones de documentos pasados, aplicando un `upsert` por clave compuesta cuádruple `Nombre_Doc + Nro_Doc + Cod_Producto + Línea` (garantizando 0 colisiones en líneas múltiples de un mismo SKU por comprobante).
- **FR-03 (Ingesta de Reportes Defontana Existentes):** Ingerir en modo solo lectura el reporte `INF_VENTAS_DETALLADAS` (.xls/.xlsx/.csv exportado de Defontana por el RPA de abastecimiento), extrayendo fecha, documento, RUC, cliente, vendedor, SKU, cantidad, venta neta sin IGV, condición de pago, fecha de vencimiento y línea. Formato de origen: tabla HTML codificada en `cp1252` (`windows-1252`) exportada por Defontana.
- **FR-04 (Deducción Estricta de Notas de Crédito):** Toda Nota de Crédito (NC, tipo `07 NC...`) resta automáticamente del volumen de ventas netas y unidades del vendedor, cliente y producto. Dado que Defontana exporta el 100% de las NC con cantidades y montos en signo negativo nativo, la deducción se realiza mediante suma algebraica directa ($\sum \text{Total Detalle}$ y $\sum \text{Cantidad}$), prohibiendo la inversión de signo para evitar doble resta. Los comprobantes anulados con NC quedan invalidados para el cómputo de pedidos de evaluación crediticia.
- **FR-05 (Aislamiento Total de Abastecimiento):** Cero dependencia de código ni alteración de scripts de `qalikay-abastecimiento`.
- **FR-06 (Exclusión de Consumo Interno):** Se filtran y excluyen estrictamente las 6 cuentas catalogadas como *"Consumo Interno"* para no distorsionar ventas ni ticket medio:
  1. DNI `73615353` — Cristian Gutiérrez (`CRISTIAN ANDRES`)
  2. DNI `06024456` — Walter Gutiérrez (`GUTIERREZ ARRESE WALTER`)
  3. DNI `76423008` — Carlos Cuadros (`CUADROS VALERIANO CARLOS ALBERTO`)
  4. DNI `09072925` — Linda Ríos (`Linda Ríos`)
  5. DNI `72164623` — Luis Gamarra (`Luis Angel Gamarra Calle`)
  6. DNI `72931481` — Carlos Antonio (`Carlos Antonio Ureta Abanto`)

### MÓDULO 2: SEGMENTACIÓN DE CARTERAS Y REGLAS DE NEGOCIO
- **FR-07 (Motor de las 6 Carteras y Reglas de Atribución):**
  1. *Enrique García:* Ventas B2B campo (`222` clientes en cartera).
  2. *Walter Gutiérrez:* Clientes por afinidad personal (**la cuenta UNALM / FUNDEAGRO RUC `20101259014` se incluye al 100% en métricas de venta, HUD general, Pestaña 1, Pestaña 2 y Pestaña 3; se excluye únicamente de las Alertas en Pestaña 4 y Bandejas WhatsApp en Pestaña 5**).
  3. *Cristian Gutiérrez (Mi Cartera):* Cuentas estratégicas clave (**las 9 franquicias/RUCs de ORGANA se incluyen al 100% en métricas de venta, HUD general, Pestaña 1, Pestaña 2 y Pestaña 3; se excluyen únicamente de las Alertas en Pestaña 4 y Bandejas WhatsApp en Pestaña 5**; **incluye a *Whitnin Tesen* en Piura tanto con DNI `48517168` como con RUC `10485171687`**).
  4. *Carlos Cuadros:* Ventas B2B campo (**fusionando su cartera con el 100% de la cartera histórica del ex-vendedor Joel García**).
  5. *Linda / Zully — B2B (`Rep. Comercial` + `Zully Rios`):* Clasificación **exclusivamente por el monto neto de la Factura o Boleta (`Nro_Doc`) > S/ 400.00** (sin clasificar por prefijo RUC 20 ni por suma de varios comprobantes del día). Un cliente de la cartera de Linda se clasifica como **B2B** si y solo si registra al menos una Factura o Boleta (`Nro_Doc`) con venta neta **> S/ 400.00**.
  6. *Linda / Zully — B2C (`Rep. Comercial` + `Zully Rios`):* Comprobantes (`Nro_Doc`) con venta neta **<= S/ 400.00**. Un cliente de la cartera de Linda se clasifica como **B2C** si ninguna de sus Facturas o Boletas (`Nro_Doc`) supera **S/ 400.00**.
  - *Regla Clientes Multi-Vendedor (D2):* Para seguimiento y alertas actuales, el cliente se asigna al **último vendedor que le facturó venta neta positiva** (aplicando overrides de ley: Joel $\to$ Carlos Cuadros; Whitnin DNI/RUC 10 $\to$ Cristian; Rep. Comercial $\to$ Linda/Zully).
- **FR-08 (Maestro de Proveedores Oficial desde RPA de Abastecimiento — Sin Marcas):** La relación oficial de cada SKU con su Proveedor Titular (laboratorio fabricante o importador) se obtiene estrictamente del **Maestro de Artículos de Abastecimiento** (`RAW_ARTICULOS` en `data/maestro_articulos_abastecimiento.csv`). Queda prohibido listar marcas comerciales (*D'Nattive*, *Nanita / NNF*, *VivaFrut*) como proveedores en la Pestaña 2; únicamente se listan los Proveedores Oficiales del Maestro (`NUTRIVAS`, `MOLINOS DEL MUNDO`, `PECADITOS INTEGRALES`, `AMAZON ANDES`, `WILD FOODS`, `QORINKA`, `ANDES CRISP`, `INKA COMEX`, `OLIVO DE ORO`, `DEPURATÉ`, `NOA LIFE`, `FIBRA FRUT`, `QORI`, `TAURI`, `OTROS PROVEEDORES`) y sus SKUs.
- **FR-09 (Parámetros de Lead Time por Proveedor):**
  - *Rápidos (1–2 días):* Nutrivas, Amazon Andes, Tauri, Olivo de Oro, Depuraté, Inka Comex, Andes Crisp (máx 2 días). Si stock = 0, plazo de 4–5 días coordinando con Compras.
  - *Entrega Semanal:* Molinos del Mundo (Miércoles).
  - *Mayor Demora:* Qorinka (4 días), Pecaditos (1 semana), FibraFrut/VivaFrut (1 semana, MOQ 12 unids), Fungi Amazónica (propio).
  - *En Liquidación:* Qori (Ayacucho), Noa Life, Inka Prime (vender hasta agotar stock).
- **FR-10 (Control de Cobranza y Crédito en Vivo desde OneDrive + Descarga Excel):** Lectura directa en modo solo lectura de `C:\Users\cguti\OneDrive\Inka Comex\CUENTAS POR COBRAR\QALI KAY\2026\Cuentas por cobrar 2026.xlsx` (hoja `'CXC'` con `skiprows=10` normalizando DNIs de 7 dígitos y filtrando Consumo Interno; y hoja `'Clientes (usar)'`).
  - **Tarjeta 4 del HUD Ejecutivo ("Clientes con Deuda Vencida - Total Qali Kay"):** Contabiliza **exclusivamente la cantidad de clientes que tienen deuda vencida real (`Estado == "VENCIDA"` y `Saldo > 0`)** en todo Qali Kay (`53 clientes · S/ 162,464.07`), con desglose por vendedor. Al hacer clic en la tarjeta, se despliega una tabla consolidada de los clientes y comprobantes con deuda vencida y un botón **`📥 Descargar Excel (.xlsx)`** generado localmente con SheetJS.
  - **Tarjeta "Deuda Vencida CxC" en Ficha Individual de Vendedor (Pestaña 1):** Muestra la deuda vencida real de los clientes del vendedor, al hacer clic despliega la tabla detallada de comprobantes vencidos/pendientes del vendedor e incluye el botón **`📥 Descargar Excel CxC del Vendedor (.xlsx)`**.

### MÓDULO 3: GESTIÓN DE RECOMPRA Y ALERTAS
- **FR-11 (Ciclo B2C de 25 Días y Ventana Operativa de 90 Días en Feed para Linda B2C):**
  - Alerta preventiva de fin de frasco entre días 25 y 35; alerta de seguimiento entre días 36 y 60; alerta de rescate para inactivos > 60 días.
  - **Filtro Visual de 90 Días en Feed Operativo para Linda B2C:** Para no saturar el dashboard con cientos de consumidores finales históricos inactivos de 2025, en la **Pestaña 4 (Feed de Acciones Operativas)** solo se muestran visiblemente para **Linda B2C** los clientes con compra dentro de los **últimos 3 meses (90 días)** que requieran acción comercial ($\ge 25$ días sin comprar o con deuda vencida).
  - **Botón de Descarga Histórica Completa Linda B2C:** En el Feed se incluye un botón **`📥 Descargar Excel Completo Linda B2C (Histórico Total)`** para exportar en `.xlsx` la tabla analítica con el 100% de los clientes históricos de Linda B2C de todo el tiempo (2025–2026).
- **FR-12 (Motor de Frecuencia B2B: Nuevos vs Recurrentes a la 4ta Compra):**
  - *Definición Matemática de "Compra" (D4):* Día Único de Facturación Neta Positiva ($\sum_{\text{día}} \text{Total\_Detalle} > 0$).
  - *Clientes Nuevos (1 a 3 compras históricas):* Seguimiento Día 7 (post-venta), Día 15 (rotación) y Día 30 (rescate).
  - *Clientes Recurrentes ($\ge 4$ compras):* Frecuencia Dinámica Individualizada ($N_{cliente}$): Preventiva $[N - 3, N]$, Fuga $\ge N + 5$, Contracción de Volumen $\ge 30\%$.
- **FR-12b (Motor de Recompra Inteligente con Recomendación Obligatoria de 3 Productos por Cliente):**
  - Generación automática de recomendaciones accionables en Pestaña 1, Pestaña 4 (Feed) y Pestaña 5 (Bandejas de Salida de WhatsApp), recomendando **3 productos (Top 3 SKUs) por cliente** (extraídos de su historial de compras; si el cliente compró $<3$ SKUs distintos en su historia, se completan hasta 3 con los SKUs líderes en stock del catálogo Qali Kay), cruzados con stock en `Kardex_Resumido`, Lead Times (`FR-09`) y promociones vigentes (`data/promociones_vigentes.json`).

### MÓDULO 4: PRESENTACIÓN Y DASHBOARD (5 PESTAÑAS)
- **FR-13 (Pestaña 1 - Gestión por Vendedor):**
  - *Ficha Individual (Default):* Selector por vendedor y por período (últimos 6 meses de 2026 + Anual), HUD 6 KPIs:
    - Tarjeta clicable **`🔴 Inactivos >2 Meses`**: muestra el total de clientes inactivos ($>60$ días sin comprar) y el subgrupo con 1 sola compra; al hacer clic despliega el panel **`#seller-inactivos-detail-panel`** con la tabla detallada de todos los clientes inactivos del vendedor (filtro por *Todos*, *1 Sola Compra* o *Recurrentes Inactivos*) y botón **`📥 Descargar Excel Clientes Inactivos del Vendedor (.xlsx)`** (más opción de descarga consolidada de las 6 carteras).
    - Tarjeta clicable **`💳 Deuda Vencida CxC`**: muestra la deuda vencida real y al hacer clic despliega la tabla detallada de comprobantes vencidos/pendientes y botón **`📥 Descargar Excel CxC del Vendedor (.xlsx)`**.
    - Evolución Gráfica (Prom. 2025 activo vs May–Oct 2026), Mix de SKUs y Proveedores Oficiales, Top Clientes Clave.
  - *Subvista Matriz:* Tabla consolidada comparativa de todo el equipo de ventas (incluyendo el 100% de las ventas comerciales y acceso directo en 1 clic al detalle de Inactivos y CxC de cada vendedor).
- **FR-14 (Pestaña 2 - Gestión por Proveedor y SKU):**
  - *Ficha Individual (Default):* Selector de Proveedor Oficial (extraído del Maestro de Artículos, sin marcas), **TOP 5 SKUs reales del período con valor en S/ y % share**, Gráfico SVG de barras de venta por vendedor para ese proveedor, Lead Time y promociones.
  - *Subvista Matriz:* Tabla global de volumen y share por proveedor oficial.
- **FR-15 (Pestaña 3 - Comparativa Histórica 6 Meses 2026 + Promedio 2025 por Meses Activos):**
  - Analiza los **últimos 6 meses de 2026 (`Mayo`, `Junio`, `Julio`, `Agosto`, `Septiembre`, `Octubre 2026`)** frente al **Promedio Mensual 2025 calculado dividiendo únicamente entre los meses de 2025 en que cada vendedor tuvo actividad real (`venta > 0`)**.
- **FR-16 (Pestaña 4 - Feed de Acciones Operativas):** Alertas en vivo con sugerencia comercial completa (3 productos recomendados + estado CxC + ciclo), botón de WhatsApp funcional, filtro de 90 días para Linda B2C en pantalla y botón de descarga Excel del histórico completo de Linda B2C.
- **FR-17 (Pestaña 5 - Bandejas WhatsApp Limpias):** Selección jerárquica de acciones del día por vendedor (1. Cobranza por mora, 2. Fuga crítica, 3. Seguimiento activo, 4. Ventana preventiva/onboarding) recomendando **3 productos por cliente**, listos para copiar con 1 clic.

### MÓDULO 5: EFICIENCIA DE TOKENS Y ESTÁNDARES METODOLÓGICOS (NFR)
- **NFR-01 (Eficiencia de Tokens):** Ningún script o prompt volcará tablas crudas al contexto de IA. Los cálculos numéricos son 100% deterministas en código local.
- **NFR-02 (Gobernanza Spec-Kit):** El proyecto sigue rigurosamente el ciclo `constitution` ➔ `specify` ➔ `clarify` (mandatorio) ➔ `plan` ➔ `tasks` ➔ `analyze` (mandatorio) ➔ `implement` ➔ `impeccable`, delegando la ejecución de código al Agente Ejecutor (`agente_ejecutor`).
- **NFR-03 (Calidad UX Impeccable y Responsive Mobile):** El Dashboard y la pantalla de bloqueo por PIN (`#lock-screen`) son 100% responsivos en teléfonos móviles (teclado numérico nativo `type="tel"` con auto-desbloqueo instantáneo, grillas adaptativas y touch targets $\ge 48\text{px}$).
