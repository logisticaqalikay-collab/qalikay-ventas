# Blueprint Maestro: Sistema de Inteligencia Comercial, KPIs y Alertas — Qali Kay (V5.0 Definitiva)
**Empresa:** Qali Kay S.A.C — "Aliados en salud natural"  
**Responsable Comercial:** Cristian Gutiérrez (Director General)  
**Rol del Agente:** Director Técnico Comercial y Especialista en Ingeniería de IA  
**Metodología de Desarrollo:** Spec-Kit (`constitution` ➔ `specify` ➔ `clarify` ➔ `plan` ➔ `tasks` ➔ `analyze` ➔ `implement` ➔ `impeccable`)  
**Modelo de Gobernanza:** Dual-Agent Architecture (Director en Raíz / Ejecutor en `/ejecucion/`)  
**Presupuesto:** Estrictamente Costo S/ 0.00 ($0.00 USD)

---

## 1. PROPÓSITO Y ALCANCE DEL SISTEMA

El **Sistema de Inteligencia Comercial y Ventas B2B/B2C de Qali Kay** es una plataforma integral de analítica, monitoreo de cartera y generación de alertas operativas diseñada para:
1. **Brindar Visibilidad Directiva en Tiempo Real:** Seguimiento mensualizado de ventas netas, ticket promedio, cumplimiento de metas, proyección de cierre y margen bruto por cartera, proveedor y producto.
2. **Empoderar a la Fuerza de Ventas:** Generación de bandejas individuales de seguimiento para que cada vendedor consulte su avance sin exponer los datos de sus pares, con mensajes preformateados y limpios para WhatsApp listos para copiar y pegar en 1 clic.
3. **Optimizar la Recompra y Mitigar Fugas:** Detección automática de clientes en riesgo de inactividad, consumidores B2C que terminan frasco (ciclo de 25 días), y alertas de cobranza cruzadas con cuentas por cobrar.
4. **Gobernar el Abastecimiento Comercial:** Visualización de tiempos de entrega (lead times) por proveedor, quiebres de stock y rotación de promociones mensuales sin que el vendedor prometa productos fuera de disponibilidad.

---

## 2. REGLAS INQUEBRANTABLES DE ARQUITECTURA (`CONSTITUTION`)

1. **Aislamiento Total respecto a `qalikay-abastecimiento`:**
   Queda **terminantemente prohibido** modificar, alterar dependencias, sobreescribir scripts o compartir entornos de ejecución con el módulo RPA de abastecimiento (`qalikay-abastecimiento`). `qalikay-ventas` es 100% autónomo y almacena su propia base de datos histórica.
2. **Base Histórica Consolidada 2025–2026 con Ventana Incremental de 60 Días:**
   El sistema analiza **todo el 2025 y todo el 2026**. Para la actualización diaria (programada en 2 cortes: 07:30 AM y 03:30 PM), no se reprocesan los 24 meses; se descarga y procesa una **ventana rodante de los últimos 60 días (2 meses)**, aplicando un `upsert` por clave única (`Nombre_Doc + Nro_Doc + Cod_Producto`) para capturar automáticamente Notas de Crédito, anulaciones o modificaciones de documentos pasados sin costo computacional excesivo.
3. **Determinismo Matemático Absoluto (Prohibido LLM para Cálculos Numéricos):**
   Todos los cálculos (ventas netas, tickets, márgenes, % share, proyecciones) se ejecutan mediante código determinista puro (Python / DuckDB / JavaScript ES6). Los modelos de IA no calculan sumatorias ni promedios matemáticos; su rol es analítico, estratégico y de orquestación.
4. **Presupuesto $0.00 (Zero-Cost Hosting & Tools):**
   Prohibido contratar APIs de pago, software SaaS con licencia por usuario o complementos de pago. El sistema se aloja en hosting gratuito (Vercel / GitHub Pages) y corre localmente o con scripts abiertos.
5. **Diferenciación Estricta Proveedor vs Marca:**
   - **Proveedor:** Laboratorio farmacéutico, importador o distribuidor titular con quien Qali Kay negocia crédito, margen y lead time (ej. Laboratorios Bagó, Medifarma, Nutrivas, Molinos del Mundo).
   - **Marca:** Línea de producto comercial (ej. *D'Nattive*, *Santiveri*, *Oriundos*). En los maestros y análisis, todo SKU se agrupa bajo su **Proveedor Titular Oficial**.
6. **Confidencialidad Comercial y Segmentación:**
   En la fase de prueba/operación, los vendedores **no tienen acceso al dashboard consolidado global**. La dirección o jefatura les despacha capturas de pantalla de su **Ficha Individual (Pestaña 1)** y los textos generados en las **Bandejas de WhatsApp (Pestaña 5)**. La totalidad de las 5 pestañas es de acceso exclusivo directivo.
7. **Privacidad de Prospectos y Bases de Clientes:**
   Los archivos de prospección en Google Drive y las bases de farmacias se mantienen privados en todo momento; ningún link público debe exponer datos sensibles de clientes o precios.

---

## 3. ARQUITECTURA DE DATOS Y PIPELINE ETL

```
┌────────────────────────────────────────────────────────────────────────┐
│                          FUENTES PRIMARIAS                             │
│  1. ERP Defontana: Reporte 'INF_VENTAS_DETALLADAS' (Excel/HTML)        │
│  2. ERP Defontana: 'Compromisos_Entrega' y 'Kardex Resumido'           │
│  3. OneDrive: 'CUENTAS POR COBRAR.xlsx' (Control de facturas vencidas) │
│  4. Maestro de Clientes: 'Contactos de Farmacias - Consolidado.xlsx'   │
│  5. Google Drive: Prospectos B2B privados (Enrique y Carlos)           │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                 MOTOR ETL & NORMALIZACIÓN (qalikay-ventas)             │
│  - Limpieza de cabeceras, conversión a tipos numéricos deterministas   │
│  - Mapeo de Vendedores reales (resolución de alias y carteras)         │
│  - Normalización: Descuento de Notas de Crédito (NC) de ventas netas   │
│  - Mapeo de Marcas a Proveedores Titulares (ej. D'Nattive -> Titular)  │
│  - Filtro y exclusión de las 3 cuentas de 'Consumo Interno'            │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   ALMACENAMIENTO INCREMENTAL (60 DÍAS)                 │
│  - Repositorio Histórico: data/ventas_2025_2026.parquet                │
│  - Clave Única Upsert: [Nombre_Doc] + [Nro_Doc] + [Cod_Producto]       │
│  - Ventana Rodante: Últimos 60 días se sobreescriben automáticamente   │
│  - Exportación para Dashboard: data/datos_comerciales.json             │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│            DASHBOARD INTERACTIVO AUTÓNOMO (HTML5/SVG/JS)               │
│  - 5 Pestañas de Inteligencia Comercial y Operativa                    │
│  - Modo Offline-first (Cero CDNs, 100% estilos y SVGs nativos)         │
│  - Motor de Bandejas WhatsApp limpias (1-click copy)                   │
└────────────────────────────────────────────────────────────────────────┘
```

### Campos Clave del Reporte Defontana (`INF_VENTAS_DETALLADAS`):
- `Fecha`: Fecha de emisión del comprobante (YYYY-MM-DD).
- `Tipo Doc`: Factura, Boleta de Venta, Nota de Crédito.
- `Nro Documento`: Identificador único correlativo.
- `RUC / DNI`: Documento de identidad del comprador.
- `Razón Social / Cliente`: Nombre fiscal o comercial de la farmacia / tienda / consumidor.
- `Vendedor`: Código o nombre del ejecutivo que facturó.
- `Código Producto (SKU)`: Código interno Qali Kay (ej. `NAN-001`, `DNC-038`).
- `Descripción Producto`: Nombre comercial del ítem.
- `Cantidad`: Unidades vendidas (negativo en caso de NC).
- `Precio Unitario Venta`: Valor unitario sin IGV y con IGV.
- `Venta Neta (S/)`: Subtotal neto sin IGV (afectado por NC).
- `Costo Total (S/)`: Costo de adquisición de la mercadería.
- `Margen Bruto (S/)`: `Venta Neta - Costo Total`.
- `Margen %`: `(Margen Bruto / Venta Neta) * 100`.

---

## 4. RADIOGRAFÍA DE CARTERAS COMERCIALES (6 SEGMENTOS)

El motor comercial clasifica todas las transacciones en **6 carteras operativas**, con reglas específicas de negocio:

| # | Cartera / Canal | Titular | Naturaleza y Reglas Específicas |
| :-: | :--- | :--- | :--- |
| **1** | **Enrique García** | Enrique García | Ejecutivo Senior de Campo (B2B). Atiende Lima Sur, Centro y Provincias. Enfoque: prospección en frío, boticas y tiendas naturistas. |
| **2** | **Walter Gutiérrez** | Walter Gutiérrez | Cartera institucional y de afinidad personal. **Regla de Exclusión:** Se analiza **sin la cuenta UNALM** (la UNALM tiene tratamiento especial y diferido). No es vendedor activo de campo. |
| **3** | **Cristian Gutiérrez** | Cristian Gutiérrez (Director) | Cartera de alto valor estratégico (Key Accounts). **Regla de Exclusión:** Se analiza **sin la cuenta Organa** (tratamiento corporativo especial). Incluye cuentas regionales de alto ticket como *Whitnin Tesen* (Piura). Ticket Promedio > S/ 1,200. |
| **4** | **Carlos Cuadros** | Carlos Cuadros | Ejecutivo Junior de Campo (B2B). Atiende Lima Norte, Lima Este, Callao y Provincias. **Regla de Fusión:** Absorbió la cartera del ex-vendedor Joel García (`Carlos C + ex Joel`). |
| **5** | **Linda / Zully — B2B** | Linda (actual) ➔ Zully | Canal Inbound digital y provincias mayoristas. **Criterio de Segmentación:** Factura o boleta **> S/ 400.00**. Captación web/redes derivadas a provincia o zonas sin cobertura presencial. |
| **6** | **Linda / Zully — B2C** | Linda (actual) ➔ Zully | Canal Consumidor Final. **Criterio de Segmentación:** Factura o boleta **<= S/ 400.00**. Compras personales de frascos unitarios atendidas por WhatsApp corporativo. |

> **Exclusiones Mandatorias del Sistema:**  
> Las 3 cuentas registradas en el ERP bajo *"Consumo Interno"* quedan **estrictamente excluidas** de los indicadores de venta neta, tickets y cumplimiento de vendedores.

---

## 5. REGLAS DE NEGOCIO, PERIODICIDAD Y ALERTAS OPERATIVAS

### A. Ciclos de Recompra B2C (Consumidor Final):
- **Ciclo Base:** 25 días (duración promedio de un frasco de 60/100 cápsulas o gomitas).
- **🟢 Ciclo de Reposición (Días 25 a 35):** Alerta Preventiva de *"Fin de Frasco"*. Mensaje de reposición habitual para garantizar continuidad de tratamiento sin quiebre de consumo.
- **🟠 Ciclo Vencido (Días 36 a 60):** Alerta de Seguimiento. Pregunta sobre experiencia/satisfacción y recordatorio de continuidad.
- **🔴 Ciclo Inactivo / Rescate (> 60 días o 1 sola compra histórica):** Alerta de Rescate con oferta especial (descuento en 2da unidad o pack dúo).

### B. Ciclos de Recompra B2B (Farmacias y Tiendas Naturistas):
- **Ciclo Estándar de Reposición:** 15 días promedio entre pedidos de mostrador.
- **🟢 Alerta Preventiva B2B:** Se dispara **5 días antes** de cumplirse el ciclo habitual (día 10).
- **🔴 Alerta de Fuga B2B:** Se dispara **5 días después** de vencido el ciclo sin compra (día 20).
- **Anomalía de Caída de Facturación:** Caída de facturación **>= 30%** en el cliente respecto a su promedio histórico de los últimos 3 meses.
- **Condición Crediticia y 6to Pedido:** Las ventas son 100% al contado (pago anticipado o contra entrega). La evaluación de crédito comercial solo se habilita a solicitud del cliente tras completar **mínimo 6 pedidos pagados puntualmente**. Comprobantes anulados con Nota de Crédito no cuentan para los 6 pedidos.

### C. Control de Cuentas por Cobrar (Cobranzas):
- El sistema cruza las ventas con `CUENTAS POR COBRAR.xlsx`.
- Ante facturas vencidas: Genera alerta de cobranza y **condiciona cualquier nuevo pedido o despacho a la cancelación previa de la deuda pendiente**.

---

## 6. MATRIZ MAESTRA DE PROVEEDORES, MARCAS Y LEAD TIMES

| Proveedor Titular (Laboratorio/Importador) | Marcas Asociadas | Lead Time / Modalidad de Despacho | Observaciones Comerciales |
| :--- | :--- | :--- | :--- |
| **NUTRIVAS S.A.C** | *Nutrivas*, *Oriundos* | **Rápido: 1 a 2 días hábiles** | Si `Stock = 0`, entrega en 4–5 días coordinando con Compras. Alta rotación en aceites y cápsulas. |
| **AMAZON ANDES** | *Amazon Andes* | **Rápido: 1 a 2 días hábiles** | Superfoods, harinas funcionales y cápsulas. |
| **TAURI** | *Tauri* | **Rápido: 1 a 2 días hábiles** | Proveedor bajo demanda. |
| **OLIVO DE ORO** | *Olivo de Oro* | **Rápido: 1 a 2 días hábiles** | Aceites de oliva y derivados. |
| **DEPURATÉ** | *Depuraté* | **Rápido: 1 a 2 días hábiles** | Infusiones y mezclas herbales. |
| **INKA COMEX** | *Inka Comex* | **Rápido: 1 a 2 días hábiles** | Insumos y cápsulas importadas. |
| **ANDES CRISP** | *Andes Crisp* | **Rápido: 2 días hábiles máx.** | Snacks saludables. Cero tolerancia a quiebres mayores a 2 días. |
| **MOLINOS DEL MUNDO** | *Santiveri* | **Entrega Fija Semanal: Miércoles** | Productos dietéticos europeos. Pedidos consolidados los lunes para recepción miércoles. |
| **QORINKA** | *Qorinka* | **Mayor Demora: 4 días hábiles** | Planificar con anticipación. |
| **PECADITOS INTEGRALES** | *Pecaditos* | **Mayor Demora: 1 semana (7 días)** | Panes y repostería integral. Mínimos por SKU aplican. |
| **FIBRA FRUT / VIVAFRUT** | *FibraFrut*, *VivaFrut* | **Mayor Demora: 1 semana (7 días)** | Mínimo por SKU = 12 unidades. |
| **FUNGI AMAZÓNICA** | *Fungi Amazónica* | **Producción Propia / Controlado** | Hongos adaptógenos (Melena de León, Reishi, Cordyceps). |
| **PROVEEDORES EN LIQUIDACIÓN** | *Qori*, *Noa Life*, *Inka Prime* | **Agotar Existencias (Cero Recompra)** | *Qori* está en Ayacucho (MOQ alto, vencimientos); *Noa Life* e *Inka Prime* se venden hasta liquidar stock actual. |
| **LÍNEA D'NATTIVE** | *D'Nattive* (Tocosh, Aloe, etc.) | **Clasificar bajo su Proveedor Titular** | *D'Nattive es una MARCA*, no un proveedor. En la data real se asocia al laboratorio titular que la fabrica. |

---

## 7. ESPECIFICACIÓN TÉCNICA DEL DASHBOARD (5 PESTAÑAS)

El frontend se materializa en [PROTOTIPO_DASHBOARD_VENTAS_QALIKAY.html](file:///c:/Users/USER/OneDrive/Documents/Proyectos%20Antigravity/Estrategia%20Ventas%20Qali%20Kay/PROTOTIPO_DASHBOARD_VENTAS_QALIKAY.html), operando como Single Page Application autónoma con estilos CSS y gráficos SVG embebidos:

### Pestaña 1: "Gestión por Vendedor"
- **Ficha Individual (Vista por defecto):**
  - Selector dinámico por vendedor (Enrique, Walter, Cristian, Carlos C, Linda/Zully B2B, Linda/Zully B2C).
  - **HUD de 6 KPIs:** 1. Venta Mes en Curso (S/), 2. Meta Comercial (S/), 3. % Cumplimiento, 4. Proyección de Cierre a Fin de Mes (S/), 5. Ticket Promedio (S/), 6. Clientes Activos del Mes.
  - **Mix de SKUs y Proveedores:** Tabla de concentración de productos y proveedores colocados por ese vendedor en el mes.
  - **Top Clientes Clave:** Ranking de clientes principales con su volumen acumulado, último pedido y semáforo de recurrencia.
- **Matriz Comparativa de Vendedores (Subvista):** Tabla tabular completa que compara en una sola pantalla a todo el equipo de ventas.

### Pestaña 2: "Gestión por Proveedor y SKU"
- **Ficha Individual por Proveedor (Vista por defecto):**
  - Selector dinámico por proveedor titular.
  - **TOP 5 Productos por Proveedor:** Muestra para cada SKU su **Venta Neta en Soles (S/)** y su **Participación Porcentual (% Share)** sobre el total del proveedor.
  - **Gráfico SVG de Barras Interactivo:** Desglose visual de cuánto vendió cada vendedor para ese proveedor seleccionado.
  - **Tarjeta de Condiciones Operativas:** Lead time promedio (días), días de crédito acordados, política de despacho y promociones vigentes del mes.
- **Matriz General de Proveedores (Subvista):** Tabla consolidada con volumen total facturado por proveedor y % de share sobre las ventas globales de Qali Kay.

### Pestaña 3: "Comparativa Histórica"
- **Gráfico SVG Multi-período:** Curva evolutiva comparativa entre los meses cerrados históricos y el avance del mes en curso.
- **Tabla Analítica Mensual:** Resumen numérico mes a mes de ventas totales, variación intermensual (MoM %), ticket promedio y número de pedidos.

### Pestaña 4: "Feed de Acciones Operativas"
- Motor reactivo de alertas categorizadas por criticidad:
  - 🔴 **Crítico:** Quiebre inminente de stock en SKUs de alta rotación, o clientes B2B clave con > 20 días sin comprar.
  - 🟠 **Advertencia:** Proveedores con margen bruto reducido (< 25%), o pedidos retenidos por deuda vencida en cuentas por cobrar.
  - 🟢 **Oportunidad:** Clientes B2C listos para recompra preventiva (25 a 35 días) y promociones de venta cruzada.

### Pestaña 5: "Bandejas WhatsApp Limpias"
- Generador de mensajes personalizados para vendedores.
- Selector por vendedor con filtros por tipo de gestión (Cobranza, Reactivación B2C, Oferta B2B, Preventiva).
- Textos limpios sin caracteres deformados, listos para pulsar el botón verde **`Copiar Mensaje`** e interactuar con `https://wa.me/...`.

---

## 8. INTEGRACIÓN CON PROSPECTOS Y CRM EXTERNO

1. **Prospectos Actuales en Google Drive:**
   - 2 archivos en Google Drive privado: uno asignado a Enrique García y otro a Carlos Cuadros (`Contactos de Farmacias`).
   - El sistema analiza la tasa de conversión (leads contactados vs primeras compras cerradas con Pack S/ 533 o Plan B S/ 300).
2. **Futuro CRM en Servidores Web (`qalikay.pe`):**
   - El modelo de datos de clientes y carteras de este sistema se desacopla mediante contratos JSON limpios para que, cuando el CRM propio en `qalikay.pe` entre en producción, la ingesta de pedidos se conecte sin rediseñar la analítica.

---

## 9. MODELO DE GOBERNANZA DUAL Y FLUJO SPEC-KIT

```
                    ┌────────────────────────────────────────────────────────┐
                    │           DIRECTOR GENERAL (Cristian Gutiérrez)        │
                    └───────────────────────────┬────────────────────────────┘
                                                │ Mandato y Prioridades
                                                ▼
┌────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                    AGENTE DIRECTOR TÉCNICO COMERCIAL Y ESPECIALISTA EN IA                          │
│  - Workspace: Raíz del Proyecto (Estrategia Ventas Qali Kay)                                       │
│  - Documentos Maestros: BLUEPRINT, .specify/memory/constitution.md, specs/001-...                  │
│  - Ciclo Spec-Kit:                                                                                 │
│    1. speckit-constitution (Gobernar los 7 principios)                                             │
│    2. speckit-specify      (Especificar features comerciales y ETL)                                │
│    3. speckit-clarify      (Resolver vacíos y reglas de negocio con el Director General)          │
│    4. speckit-plan         (Diseñar arquitectura modular, data contracts y esquemas)              │
│    5. speckit-tasks        (Desglosar tareas atómicas ordenadas por dependencia)                   │
│    6. speckit-analyze      (Validar consistencia y emitir validation-report.md)                    │
│    7. speckit-converge     (Verificar cobertura continua y control de regresión)                   │
└───────────────────────────────────────────────┬────────────────────────────────────────────────────┘
                                                │ Entrega de tasks.md aprobadas
                                                ▼
┌────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   AGENTE EJECUTOR (DEVELOPER)                                      │
│  - Workspace: Carpeta /ejecucion/                                                                  │
│  - Misión Técnica:                                                                                 │
│    1. speckit-implement   (Programar código HTML/JS/CSS, parsers ETL y scripts sin salir de /ejec/)│
│    2. impeccable polish   (Pulir contraste, números tabulares, semáforos y accesibilidad mobile)   │
│  - Restricción: No puede alterar la Constitución ni modificar archivos de la raíz                  │
└────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

**Version**: 5.0.0 (Master Definitivo) | **Ratificado**: 2026-10-23 | **Qali Kay S.A.C**
