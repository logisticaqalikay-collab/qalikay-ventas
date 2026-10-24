# Blueprint Maestro: Sistema de Inteligencia Comercial, KPIs y Alertas — Qali Kay (V5.1 Definitiva)
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

1. **Aislamiento Total respecto a `qalikay-abastecimiento` (Aprovechamiento de Ingesta sin Modificar Código):**
   Queda **terminantemente prohibido** modificar, alterar dependencias, sobreescribir scripts o alterar el flujo del bot RPA de abastecimiento (`qalikay-abastecimiento`). `qalikay-ventas` es 100% autónomo. Sin embargo, para no saturar el ERP Defontana con descargas duplicadas, `qalikay-ventas` **lee directamente en modo solo lectura los reportes ya descargados** por la automatización existente.
2. **Base Histórica Consolidada 2025–2026 con Ventana Incremental de 90 Días (3 Meses):**
   El sistema analiza **todo el 2025 y todo el 2026**. Para la actualización diaria incremental se adopta una **ventana rodante de los últimos 90 días (3 meses)** (alineada a la ventana de extracción de abastecimiento). El motor aplica un `upsert` por clave única (`Nombre_Doc + Nro_Doc + Cod_Producto`) sobre el almacén Parquet para capturar automáticamente Notas de Crédito, devoluciones y anulaciones de documentos pasados sin tener que reprocesar los 24 meses completos.
3. **Determinismo Matemático Absoluto (Cero Alucinación Numérica):**
   Todos los cálculos (ventas netas, tickets, márgenes, % share, proyecciones) se ejecutan mediante código determinista puro (Python / DuckDB / JavaScript ES6). Queda **terminantemente prohibido usar Modelos de Lenguaje (LLMs) para calcular sumatorias o promedios matemáticos**.
4. **Política de Eficiencia y Ahorro Extremo de Tokens:**
   - **Cero volcados masivos en el prompt:** Nunca inyectar tablas completas de miles de filas al contexto del LLM. Los scripts procesan la data localmente y el LLM solo recibe esquemas, agregados o resúmenes ejecutivos.
   - **Tareas atómicas y acotadas:** El Director delega al Ejecutor tareas puntuales con alcance exacto de archivos para evitar dispersión y consumo innecesario de tokens.
   - **Persistencia en disco:** La memoria y decisiones se guardan en archivos (`specs/`, `data/`, `BLUEPRINT`), evitando tener que re-explicar el contexto en cada turno.
5. **Presupuesto $0.00 (Zero-Cost Hosting & Tools):**
   Prohibido contratar APIs de pago, software SaaS con licencia por usuario o complementos de pago. El sistema se aloja en hosting gratuito (Vercel / GitHub Pages) y corre localmente o con scripts abiertos.
6. **Diferenciación Estricta Proveedor vs Marca:**
   - **Proveedor:** Laboratorio farmacéutico, importador o distribuidor titular con quien Qali Kay negocia crédito, margen y lead time (ej. Laboratorios Bagó, Medifarma, Nutrivas, Molinos del Mundo).
   - **Marca:** Línea de producto comercial (ej. *D'Nattive*, *Santiveri*, *Oriundos*). En los maestros y análisis, todo SKU se agrupa bajo su **Proveedor Titular Oficial**.
7. **Confidencialidad Comercial y Segmentación:**
   En la fase de prueba/operación, los vendedores **no tienen acceso al dashboard consolidado global**. La dirección o jefatura les despacha capturas de pantalla de su **Ficha Individual (Pestaña 1)** y los textos generados en las **Bandejas de WhatsApp (Pestaña 5)**. La totalidad de las 5 pestañas es de acceso exclusivo directivo.

---

## 3. ARQUITECTURA DE DATOS Y PIPELINE ETL (VENTANA DE 90 DÍAS)

```
┌────────────────────────────────────────────────────────────────────────┐
│                          FUENTES PRIMARIAS                             │
│  1. ERP Defontana (vía descargas RPA existentes de 90 días):           │
│     - 'INF_VENTAS_DETALLADAS' (.xlsx/.csv)                             │
│     - 'Compromisos_Entrega' y 'Kardex Resumido'                        │
│  2. OneDrive: 'CUENTAS POR COBRAR.xlsx' (Facturas vencidas)            │
│  3. Maestro de Clientes: 'Contactos de Farmacias - Consolidado.xlsx'   │
│  4. Google Drive: Prospectos B2B privados (Enrique y Carlos)           │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                 MOTOR ETL & NORMALIZACIÓN (qalikay-ventas)             │
│  - Limpieza de cabeceras, conversión a tipos numéricos deterministas   │
│  - Normalización: Descuento de Notas de Crédito (NC) de ventas netas   │
│  - Mapeo de Marcas a Proveedores Titulares (ej. D'Nattive -> Titular)  │
│  - Filtro y exclusión de las 3 cuentas de 'Consumo Interno'            │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   ALMACENAMIENTO INCREMENTAL (90 DÍAS)                 │
│  - Repositorio Histórico: data/ventas_2025_2026.parquet                │
│  - Clave Única Upsert: [Nombre_Doc] + [Nro_Doc] + [Cod_Producto]       │
│  - Ventana Rodante: Últimos 90 días se sobreescriben automáticamente   │
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

---

## 4. SUITE DE SKILLS, MCPS Y HERRAMIENTAS DE IA SELECCIONADAS

Para asegurar rigor metodológico y control de calidad, el proyecto adopta formalmente la siguiente suite de herramientas de IA:

### A. Spec-Kit Suite (Metodología Formal de Especificación):
1. **`speckit-constitution`**: Gobierno y salvaguarda de los principios no negociables (costo S/ 0.00, aislamiento, marcas vs proveedores).
2. **`speckit-specify`**: Creación formal de requerimientos funcionales y criterios de aceptación en `spec.md`.
3. **`speckit-clarify` (PASO OBLIGATORIO)**: Identificación proactiva de vacíos comerciales, ambigüedades y casos borde antes de escribir código.
4. **`speckit-plan`**: Definición de la arquitectura técnica, esquemas y data contracts en `plan.md`.
5. **`speckit-tasks`**: Desglose de tareas atómicas con dependencias ordenadas en `tasks.md`.
6. **`speckit-analyze` (FILTRO DE CALIDAD OBLIGATORIO)**: Validación cruzada de consistencia entre spec, plan, tasks y constitución antes de autorizar código (`validation-report.md`).
7. **`speckit-implement`**: Ejecución disciplinada de tareas a cargo del Agente Ejecutor en `/ejecucion/`.
8. **`speckit-converge`**: Evaluación del estado del codebase contra las tareas para detectar pendientes.

### B. Impeccable Skill (`impeccable`):
- **Modo `Operate` para Dashboards:** Estándar de diseño para alta densidad de información (números tabulares alineados a la derecha, semáforos de alto contraste, tipografía legible >= 12px, badges informativos, touch targets para móviles en botones de WhatsApp >= 48px).

### C. gstack Suite (Ingeniería de Software & Calidad):
- **`gstack-review`**: Auditoría de diffs y seguridad antes de fusionar cambios del ejecutor al prototipo principal.
- **`gstack-browse` / Chrome DevTools**: Pruebas automáticas de interacción en navegador, validación de eventos táctiles y comprobación de errores en consola.

### D. Herramientas Nativas de Ejecución:
- Uso prioritario de las herramientas nativas de Antigravity (`run_command`, `write_file`, `edit_file`, `read_file`) sin agregar MCPs externos innecesarios que consuman memoria o tokens.

---

## 5. RADIOGRAFÍA DE CARTERAS COMERCIALES (6 SEGMENTOS)

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

## 6. REGLAS DE NEGOCIO, PERIODICIDAD Y ALERTAS OPERATIVAS

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

## 7. MATRIZ MAESTRA DE PROVEEDORES, MARCAS Y LEAD TIMES

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

## 8. ESPECIFICACIÓN TÉCNICA DEL DASHBOARD (5 PESTAÑAS)

1. **Pestaña 1: Gestión por Vendedor**
   - *Ficha Individual (Default):* Selector de vendedor, HUD 6 KPIs (Venta Mes, Meta, % Cumplimiento, Proyección Cierre, Ticket Promedio, Clientes Activos), Mix de SKUs y Proveedores, Top Clientes Clave.
   - *Subvista Matriz Comparativa:* Tabla comparativa consolidada del equipo de ventas.
2. **Pestaña 2: Gestión por Proveedor y SKU**
   - *Ficha Individual (Default):* Selector de proveedor, **TOP 5 SKUs con valor en S/ y % share**, Gráfico de barras SVG de venta por vendedor para ese proveedor, y tarjeta de Lead Time, días de crédito y promociones.
   - *Subvista Matriz de Proveedores:* Tabla consolidada con volumen y share total.
3. **Pestaña 3: Comparativa Histórica**
   - Gráfico multi-período SVG (meses cerrados + mes en curso) y tabla analítica mensual completa.
4. **Pestaña 4: Feed de Acciones Operativas**
   - Alertas en vivo (críticas, advertencias, oportunidades).
5. **Pestaña 5: Bandejas WhatsApp Limpias**
   - Textos formateados limpios listos para pulsar el botón verde **`Copiar Mensaje`** e interactuar con `https://wa.me/...`.

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
│  - Documentos Maestros: BLUEPRINT v5.1, .specify/memory/constitution.md, specs/001-...             │
│  - Ciclo Spec-Kit:                                                                                 │
│    1. speckit-constitution (Gobernar los principios)                                               │
│    2. speckit-specify      (Especificar features comerciales y ETL)                                │
│    3. speckit-clarify      (PASO MANDATORIO: Resolver vacíos y reglas de negocio con Cristian)     │
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

**Version**: 5.1.0 (Master Definitivo) | **Ratificado**: 2026-10-23 | **Qali Kay S.A.C**
