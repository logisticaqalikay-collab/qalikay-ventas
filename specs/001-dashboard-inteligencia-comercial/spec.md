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
- **FR-01 (Consolidado Histórico 2025–2026):** Almacenar y consultar el histórico completo de ventas desde `01/01/2025` hasta el día en curso en formato Parquet (`data/ventas_2025_2026.parquet`).
- **FR-02 (Ventana Rodante Incremental de 90 Días):** Procesar diariamente los comprobantes de los últimos 90 días (3 meses) para absorber Notas de Crédito, devoluciones y anulaciones de documentos pasados, aplicando un `upsert` por clave compuesta `Nombre_Doc + Nro_Doc + Cod_Producto`.
- **FR-03 (Ingesta de Reportes Defontana Existentes):** Ingerir en modo solo lectura el reporte `INF_VENTAS_DETALLADAS` (.xlsx/.csv exportado de Defontana por el RPA de abastecimiento), extrayendo fecha, documento, RUC, cliente, vendedor, SKU, cantidad, venta neta sin IGV, costo y margen.
- **FR-04 (Deducción Estricta de Notas de Crédito):** Toda Nota de Crédito (NC) debe restar automáticamente del volumen de ventas netas del vendedor y del cliente. Los comprobantes anulados con NC quedan invalidados para el cómputo de pedidos de evaluación crediticia.
- **FR-05 (Aislamiento Total de Abastecimiento):** Cero dependencia de código ni alteración de scripts de `qalikay-abastecimiento`.
- **FR-06 (Exclusión de Consumo Interno):** Las 3 cuentas catalogadas como *"Consumo Interno"* deben ser filtradas y excluidas de los cómputos comerciales.

### MÓDULO 2: SEGMENTACIÓN DE CARTERAS Y REGLAS DE NEGOCIO
- **FR-07 (Motor de las 6 Carteras):**
  1. *Enrique García:* Ventas B2B campo.
  2. *Walter Gutiérrez:* Clientes por afinidad personal (**excluyendo estrictamente la cuenta UNALM**).
  3. *Cristian Gutiérrez (Mi Cartera):* Cuentas estratégicas clave (**excluyendo estrictamente la cuenta Organa**; incluye *Whitnin Tesen* en Piura).
  4. *Carlos Cuadros:* Ventas B2B campo (**fusionando su cartera con la del ex-vendedor Joel García**).
  5. *Linda / Zully — B2B:* Pedidos inbound web/redes con comprobante **> S/ 400.00**.
  6. *Linda / Zully — B2C:* Pedidos de consumidor final con comprobante **<= S/ 400.00**.
- **FR-08 (Maestro de Proveedores vs Marcas):** Mapear marcas a su proveedor titular (ejemplo: *D'Nattive* debe asociarse a su laboratorio fabricante titular; *Oriundos* a *Nutrivas*; *Santiveri* a *Molinos del Mundo*).
- **FR-09 (Parámetros de Lead Time por Proveedor):**
  - *Rápidos (1–2 días):* Nutrivas, Amazon Andes, Tauri, Olivo de Oro, Depuraté, Inka Comex, Andes Crisp (máx 2 días). Si stock = 0, plazo de 4–5 días coordinando con Compras.
  - *Entrega Semanal:* Molinos del Mundo (Miércoles).
  - *Mayor Demora:* Qorinka (4 días), Pecaditos (1 semana), FibraFrut/VivaFrut (1 semana, MOQ 12 unids), Fungi Amazónica (propio).
  - *En Liquidación:* Qori (Ayacucho), Noa Life, Inka Prime (vender hasta agotar stock).
- **FR-10 (Control de Cobranza y Crédito):** Cruzar con `CUENTAS POR COBRAR.xlsx`. Clientes con deuda vencida disparan alerta de cobranza y condicionan nuevos despachos. Evaluación de crédito solo a partir del 6to pedido pagado al contado.

### MÓDULO 3: GESTIÓN DE RECOMPRA Y ALERTAS
- **FR-11 (Ciclo B2C de 25 Días):** Alerta preventiva de fin de frasco entre días 25 y 35; alerta de seguimiento entre días 36 y 60; alerta de rescate para inactivos > 60 días o compradores de 1 sola vez.
- **FR-12 (Ciclo B2B de 15 Días):** Alerta preventiva 5 días antes (día 10); alerta de fuga 5 días después (día 20); alerta de caída de facturación >= 30%.

### MÓDULO 4: PRESENTACIÓN Y DASHBOARD (5 PESTAÑAS)
- **FR-13 (Pestaña 1 - Gestión por Vendedor):**
  - *Ficha Individual (Default):* Selector por vendedor, HUD 6 KPIs (Venta Mes, Meta, % Cumplimiento, Proyección Cierre, Ticket Promedio, Clientes Activos), Mix de SKUs y Proveedores, Top Clientes Clave.
  - *Subvista Matriz:* Tabla consolidada comparativa de todo el equipo de ventas.
- **FR-14 (Pestaña 2 - Gestión por Proveedor y SKU):**
  - *Ficha Individual (Default):* Selector por proveedor, **TOP 5 SKUs con valor en S/ y % share**, Gráfico SVG interactivo de barras de venta por vendedor para ese proveedor, tarjeta de Lead Time, días de crédito y promociones.
  - *Subvista Matriz:* Tabla global de volumen y share por proveedor.
- **FR-15 (Pestaña 3 - Comparativa Histórica):** Gráfico evolutivo multi-período SVG (meses cerrados + mes en curso) y tabla analítica mensual completa.
- **FR-16 (Pestaña 4 - Feed de Acciones Operativas):** Alertas en vivo (críticas, advertencias, oportunidades).
- **FR-17 (Pestaña 5 - Bandejas WhatsApp Limpias):** Mensajes formateados limpios listos para copiar con 1 clic (`Copiar Mensaje`) sin caracteres deformados.

### MÓDULO 5: EFICIENCIA DE TOKENS Y ESTÁNDARES METODOLÓGICOS (NFR)
- **NFR-01 (Eficiencia de Tokens):** Ningún script o prompt volcará tablas crudas al contexto de IA. Los cálculos numéricos son 100% deterministas en código local.
- **NFR-02 (Gobernanza Spec-Kit):** El proyecto sigue rigurosamente el ciclo `constitution` ➔ `specify` ➔ `clarify` (mandatorio) ➔ `plan` ➔ `tasks` ➔ `analyze` (mandatorio) ➔ `implement` ➔ `impeccable`.
- **NFR-03 (Calidad UX Impeccable):** El Dashboard se audita en modo `Operate` para visualización ejecutiva densa y accesible en móvil.
