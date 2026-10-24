# Feature Specification: 001 - Sistema de Inteligencia Comercial y Dashboard de Ventas B2B/B2C

**Código:** `QK-VENTAS-001`  
**Área:** Dirección Comercial y Operaciones  
**Responsable:** Cristian Gutiérrez (Director General)  
**Metodología:** Spec-Kit (`constitution` ➔ `specify` ➔ `clarify` ➔ `plan` ➔ `tasks` ➔ `analyze` ➔ `implement`)  
**Presupuesto:** S/ 0.00 ($0.00 USD)

---

## 1. Overview y Objetivos de Negocio
Construir el sistema integral de inteligencia comercial de Qali Kay S.A.C, que consolide las ventas de los años **2025 y 2026**, procese actualizaciones incrementales mediante una **ventana rodante de 60 días** desde los reportes del ERP Defontana, segmente a las **6 carteras comerciales** (incluyendo la bifurcación B2B vs B2C de Linda/Zully y la absorción de la cartera de Joel por Carlos Cuadros), evalúe los lead times de proveedores y genere alertas operativas y bandejas de WhatsApp limpias sin caracteres deformados.

---

## 2. Requerimientos Funcionales (FR)

### MÓDULO 1: ARQUITECTURA DE DATOS Y ETL (BACKEND & STORAGE)
- **FR-01 (Consolidado Histórico 2025–2026):** El sistema debe almacenar y consultar el histórico completo de ventas desde `01/01/2025` hasta el día en curso.
- **FR-02 (Ventana Rodante Incremental de 60 Días):** El pipeline ETL debe procesar diariamente los comprobantes de los últimos 60 días para absorber Notas de Crédito, devoluciones y anulaciones de documentos pasados, aplicando un `upsert` por clave compuesta `Nombre_Doc + Nro_Doc + Cod_Producto`.
- **FR-03 (Ingesta de Reportes Defontana):** El motor debe ingerir y normalizar el reporte `INF_VENTAS_DETALLADAS` (Excel/CSV/HTML exportado del ERP), extrayendo fecha, documento, RUC, cliente, vendedor, SKU, cantidad, venta neta sin IGV, costo y margen.
- **FR-04 (Deducción Estricta de Notas de Crédito):** Toda Nota de Crédito (NC) debe restar automáticamente del volumen de ventas netas del vendedor y del cliente. Los comprobantes anulados con NC quedan invalidados para el cómputo de pedidos de evaluación crediticia.
- **FR-05 (Aislamiento de Abastecimiento):** Cero dependencia de código ni alteración de scripts de `qalikay-abastecimiento`.
- **FR-06 (Exclusión de Consumo Interno):** Las 3 cuentas catalogadas como *"Consumo Interno"* deben ser filtradas y excluidas de los cómputos comerciales.

### MÓDULO 2: SEGMENTACIÓN DE CARTERAS Y REGLAS DE NEGOCIO
- **FR-07 (Motor de las 6 Carteras):**
  1. *Enrique García:* Ventas B2B campo.
  2. *Walter Gutiérrez:* Clientes por afinidad personal (**excluyendo estrictamente la cuenta UNALM**).
  3. *Cristian Gutiérrez (Mi Cartera):* Cuentas estratégicas clave (**excluyendo estrictamente la cuenta Organa**; incluye *Whitnin Tesen* en Piura).
  4. *Carlos Cuadros:* Ventas B2B campo (**fusionando su cartera con la del ex-vendedor Joel García**).
  5. *Linda / Zully — B2B:* Pedidos inbound web/redes con comprobante **> S/ 400.00**.
  6. *Linda / Zully — B2C:* Pedidos de consumidor final con comprobante **<= S/ 400.00**.
- **FR-08 (Maestro de Proveedores vs Marcas):**
  - Mapear marcas a su proveedor titular (ejemplo: *D'Nattive* debe asociarse a su laboratorio fabricante titular; *Oriundos* a *Nutrivas*; *Santiveri* a *Molinos del Mundo*).
- **FR-09 (Parámetros de Lead Time por Proveedor):**
  - *Rápidos (1–2 días):* Nutrivas, Amazon Andes, Tauri, Olivo de Oro, Depuraté, Inka Comex, Andes Crisp (máx 2 días). Si stock = 0, plazo de 4–5 días coordinando con Compras.
  - *Entrega Semanal:* Molinos del Mundo (Miércoles).
  - *Mayor Demora:* Qorinka (4 días), Pecaditos (1 semana), FibraFrut/VivaFrut (1 semana, MOQ 12 unids), Fungi Amazónica (propio).
  - *En Liquidación:* Qori (Ayacucho), Noa Life, Inka Prime (vender hasta agotar stock).
- **FR-10 (Control de Cobranza y Crédito):**
  - Cruzar con `CUENTAS POR COBRAR.xlsx`. Clientes con deuda vencida disparan alerta de cobranza y condicionan nuevos despachos. Evaluación de crédito solo a partir del 6to pedido pagado al contado.

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

---

## 3. Criterios de Aceptación y Puertas de Calidad
- [ ] La base histórica 2025–2026 se carga y actualiza mediante ventana rodante de 60 días sin errores de duplicación.
- [ ] La cartera de Linda/Zully se divide matemáticamente en B2B (> S/ 400) y B2C (<= S/ 400).
- [ ] Las cuentas UNALM y Organa quedan excluidas de las carteras de Walter y Cristian respectivamente.
- [ ] Carlos Cuadros tiene consolidados sus clientes y los del ex-vendedor Joel García.
- [ ] El dashboard carga en modo 100% offline (sin dependencias CDN externas).
- [ ] Cada proveedor muestra sus TOP 5 productos con montos exactos en S/ y su % de participación.
- [ ] El botón de WhatsApp copia el mensaje limpio y abre el enlace directo `https://wa.me/...`.
