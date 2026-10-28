# Tasks: 001 - Sistema de Inteligencia Comercial y Dashboard de Ventas B2B/B2C

**Código:** `QK-VENTAS-001`  
**Metodología:** Spec-Kit (`tasks` ➔ `analyze` ➔ `implement`)  
**Regla de Eficiencia:** Ahorro extremo de tokens (cero volcados masivos en prompt; código determinista en Python/JS).

---

## FASE 1: ARQUITECTURA Y PROTOTIPADO VISUAL BASE (COMPLETADO ✅)
- [x] **T001**: Diseñar la estructura de navegación de las 5 pestañas operativas en HTML5 y CSS3 autónomo.
- [x] **T002**: Implementar Pestaña 1 "Gestión por Vendedor" con Ficha Individual (HUD 6 KPIs + Mix SKUs y Proveedores + Clientes Clave) y Matriz de Vendedores.
- [x] **T003**: Implementar Pestaña 2 "Gestión por Proveedor y SKU" con Ficha Individual (TOP 5 SKUs en S/ y % share + Gráfico SVG + Lead time) y Matriz de Proveedores.
- [x] **T004**: Implementar Pestaña 3 "Comparativa Histórica" con gráfico evolutivo SVG multi-período y tabla analítica mensual.
- [x] **T005**: Implementar Pestaña 4 "Feed de Acciones Operativas" con categorización de alertas por severidad.
- [x] **T006**: Implementar Pestaña 5 "Bandejas WhatsApp" con generador de textos limpios y botón `Copiar Mensaje`.

---

## FASE 2: INGESTA, ALMACÉN PARQUET Y VENTANA RODANTE DE 90 DÍAS (COMPLETADO ✅)
- [x] **T007**: Crear el script de ingesta `src/etl_ventas_defontana.py` para parsear los reportes de Defontana en `data/` (formato HTML `cp1252`) de 2025 (20,435 filas) y 2026 (17,598 filas), descartando la columna 15 duplicada (`Nombre del Vendedor`) y normalizando fechas, tipos numéricos, clientes, RUC y montos netos.
- [x] **T008**: Implementar la lógica de deducción de Notas de Crédito (NC), aplicando suma algebraica directa ($\sum \text{Total Detalle}$ y $\sum \text{Cantidad}$) dado que el 100% de las NC en Defontana ya traen signo negativo en origen.
- [x] **T009**: Implementar el filtro de exclusión estricto para las 6 cuentas catalogadas como *"Consumo Interno"* (Cristian Gutiérrez, Walter Gutiérrez, Carlos Cuadros, Linda Ríos, Luis Gamarra y Carlos Antonio Ureta — 322 transacciones).
- [x] **T010**: Construir el módulo de almacenamiento `data/ventas_2025_2026.parquet` consolidando las 37,711 transacciones comerciales netas (de las 38,033 brutas) y el algoritmo de ventana rodante de **90 días (3 meses)** con `upsert` por clave compuesta cuádruple `Nombre_Doc + Nro_Doc + Cod_Producto + Línea`.
- [x] **T011**: Conectar el **Maestro de Artículos de Abastecimiento** (`RAW_ARTICULOS`, 454 SKUs activos sincronizados por el RPA + snapshot local `data/maestro_articulos_abastecimiento.csv`) para asignación oficial determinista de Proveedor Titular a cada SKU y normalización de marcas.

---

## FASE 3: MOTOR DE REGLAS DE CARTERAS Y GESTIÓN DE ALERTAS (COMPLETADO ✅)
- [x] **T012**: Implementar en `src/motor_reglas_carteras.py` la segmentación determinista de las 6 carteras comerciales y atribución al último vendedor con venta positiva:
  - *Enrique García* (B2B campo).
  - *Walter Gutiérrez* (excluyendo UNALM `20101259014` en Pestaña 1 y Alertas; manteniéndola en Pestañas 2 y 3).
  - *Cristian Gutiérrez* (excluyendo Organa/CHYP en Pestaña 1 y Alertas, manteniéndolas en Pestañas 2 y 3; incluyendo *Whitnin Tesen* tanto con DNI `48517168` como RUC `10485171687`).
  - *Carlos Cuadros* (fusionando el 100% de la cartera histórica de Joel García).
  - *Linda / Zully — B2B* (`Rep. Comercial` + `Zully Rios`, comprobantes `Nro_Doc` > S/ 400.00; en alertas clientes con RUC 20 o >= 1 compra > S/ 400).
  - *Linda / Zully — B2C* (`Rep. Comercial` + `Zully Rios`, comprobantes `Nro_Doc` <= S/ 400.00).
- [x] **T013**: Implementar el motor de ciclo B2C de 25 días (Alertas Preventivas días 25–35, Seguimiento días 36–60, Rescate > 60 días).
- [x] **T014**: Implementar el motor de Frecuencia B2B definiendo "Compra" como **Día Único de Facturación Neta Positiva** ($\sum_{\text{día}} \text{Total\_Detalle} > 0$):
  - *Clientes Nuevos (1 a 3 compras históricas):* Protocolo de seguimiento escalonado a los 7 días (post-venta/recepción), 15 días (rotación inicial y promos) y 30 días (rescate/cierre).
  - *Clientes Recurrentes (a partir de la 4ta compra registrada):* Cálculo de frecuencia dinámica individual ($N$) con Alerta Preventiva en $[N - 3 \text{ a } N \text{ días}]$, Alerta de Fuga a los $\ge N + 5 \text{ días}$ y Alerta de Contracción de Volumen $\ge 30\%$.
- [x] **T014b**: Crear `data/promociones_vigentes.json` e implementar el Motor de Recompra B2B Inteligente que cruza la Canasta habitual del cliente (`ventas_2025_2026.parquet`), el Stock actual de almacén (`../qalikay-abastecimiento/descargas_erp/Kardex_Resumido_*.xlsx`), los Lead Times del proveedor y las promociones vigentes para generar sugerencias comerciales en Ficha y WhatsApp.
- [x] **T015**: Implementar el cruce en vivo (modo solo lectura) con `C:\Users\cguti\OneDrive\Inka Comex\CUENTAS POR COBRAR\QALI KAY\2026\Cuentas por cobrar 2026.xlsx` (hoja `'CXC'` `skiprows=10` para saldos vencidos/a cuenta y evaluación de 6 pedidos al contado, y hoja `'Clientes (usar)'` para nombre comercial, contacto y celular de WhatsApp).
- [x] **T016**: Cargar la matriz determinista de Lead Times por proveedor (Rápidos 1-2d, Molinos del Mundo miércoles, demoras mayores, proveedores en liquidación).

---

## FASE 4: VINCULACIÓN AL DASHBOARD Y ACTUALIZACIÓN AUTOMÁTICA EN 3 NIVELES (COMPLETADO ✅)
- [x] **T017**: Conectar la sincronización automática en vivo con el RPA en nube (`RAW_VENTAS`, `RAW_KARDEX` y `PANEL_CONTROL` de Google Sheets `16KcBYTetx0IQFiv2832gUgekrzKT93wghlaBrOxPg9Q`) y crear el script `src/exportar_datos_dashboard.py` que consolida todos los cálculos deterministas y genera `data/datos_comerciales.json` (absorbiendo las ventas hasta el último corte del RPA).
- [x] **T018**: Conectar `ejecucion/PROTOTIPO_DASHBOARD_VENTAS_QALIKAY.html` a la data real certificada de `data/datos_comerciales.json` (incluyendo inyección embebida para apertura directa `file://` sin bloqueo CORS y visualización del timestamp de `PANEL_CONTROL` del RPA en la cabecera), reemplazando los mocks en las 5 pestañas.
- [x] **T019**: Incorporar en el Dashboard un componente interactivo de carga manual (**Dropzone / Modal de Importación** con SheetJS `xlsx.full.min.js` local/offline) para permitir arrastrar reportes de Defontana o Cuentas por Cobrar directamente desde el navegador sin usar consola.
- [x] **T019b**: Crear el orquestador automático de 1 clic `actualizar_dashboard.bat` (que ejecuta en cadena: `etl_ventas_defontana.py --sync-rpa` $\to$ `motor_reglas_carteras.py` $\to$ `exportar_datos_dashboard.py`) y registrar la tarea programada en Windows (`07:30` y `15:30` hora Lima, 20 min después del RPA de GitHub Actions).

---

## FASE 5: AUDITORÍA UX Y DESPLIEGUE CLOUD SEGURO (COMPLETADO ✅)
- [x] **T020**: Auditar y pulir `ejecucion/PROTOTIPO_DASHBOARD_VENTAS_QALIKAY.html` utilizando la skill `impeccable` en modo `Operate`: elevar las 56 ocurrencias de tipografía sub-12px a `>= 12px`, fijar touch targets móviles `>= 48px`, activar `font-variant-numeric: tabular-nums` global con alineación derecha estricta e implementar paginación progresiva de 50 en 50 en el Feed de Alertas (`Todos (1,312)`).
- [x] **T021**: Implementar pantalla de bloqueo por **único PIN Directivo (SHA-256)** en el Dashboard (Principio VII), configurar `.gitignore` estricto (excluyendo `.xls`, `.parquet`, `.venv` y cachés), crear `vercel.json` para despliegue gratuito en **Vercel Hobby (S/ 0.00)** sobre Repositorio Privado de GitHub e integrar auto-push condicional en `actualizar_dashboard.bat`.

---

## FASE 6: REFINAMIENTO EJECUTIVO DE REGLAS DE NEGOCIO V2 Y EXPORTACIONES EXCEL (COMPLETADO ✅)
- [x] **T022**: Actualizar los artefactos oficiales de Spec-Kit (`spec.md`, `plan.md`, `tasks.md`) con las 11 mejoras ejecutivas previas (clientes inactivos reales, 100% de ventas en HUD y matrices, exclusión de Organa/UNALM solo en alertas/WA, universo real de carteras, últimos 6 meses de 2026 + promedio 2025 por meses activos, proveedores oficiales del Maestro de Artículos sin marcas, y diseño responsive móvil con PIN táctil) y los 6 nuevos requerimientos.
- [x] **T023**: Actualizar `src/motor_reglas_carteras.py` para:
  1. Reclasificar a los clientes de Linda (`Rep. Comercial` + `Zully Rios`) en **B2B vs B2C considerando únicamente el monto neto por Factura o Boleta (`Nro_Doc > S/ 400.00` = B2B; `<= S/ 400.00` = B2C)**, eliminando la regla por prefijo RUC 20 y suma diaria.
  2. Garantizar que `generate_smart_repurchase_recommendation()` recomiende siempre **3 productos (Top 3 SKUs) por cliente** (completando con los SKUs líderes en stock del catálogo si el cliente compró $<3$ productos distintos en su historia) e incluya los 3 productos en el copy de WhatsApp.
- [x] **T024**: Actualizar `src/exportar_datos_dashboard.py` para:
  1. Recomendar **3 productos por cliente** tanto en las Bandejas de Salida de WhatsApp (`WA_AGENDAS`, Pestaña 5) como en las sugerencias del Feed Operativo (`CLIENTS`, Pestaña 4).
  2. Exportar el objeto `GLOBAL_CXC_VENCIDOS` con el resumen y listado completo de los **54 clientes con deuda vencida real (`Estado == "VENCIDA"` y `Saldo > 0`)** de todo Qali Kay (`S/ 162,464.07`), agrupados por cliente y por documento.
  3. Para **Linda B2C**, filtrar el arreglo visible `CLIENTS` del Feed de Acciones Operativas únicamente a los clientes con compras en los **últimos 3 meses (90 días)** que requieran acción ($\ge 25$ días de inactividad o deuda vencida), y exportar además `LINDA_B2C_FULL_HISTORY` con todos los clientes históricos de Linda B2C (2025–2026, 877 clientes) para su descarga en Excel.
- [x] **T025**: Actualizar `ejecucion/PROTOTIPO_DASHBOARD_VENTAS_QALIKAY.html` para:
  1. Mostrar en la 4ta tarjeta del HUD Ejecutivo exclusivamente los **Clientes con Deuda Vencida (`54 Clientes · S/ 162,464.07`)** y su desglose por cartera; al hacer clic en la tarjeta, desplegar un panel/modal con la tabla completa de clientes con deuda vencida de Qali Kay y un botón **`📥 Descargar Excel Deuda Vencida Total (.xlsx)`** usando SheetJS (`XLSX.writeFile`).
  2. Agregar en el panel desplegable de Deuda Vencida CxC de la Ficha Individual de cada vendedor (Pestaña 1) el botón **`📥 Descargar Excel Deuda Vencida del Vendedor (.xlsx)`**.
- [x] **T026**: Actualizar `ejecucion/PROTOTIPO_DASHBOARD_VENTAS_QALIKAY.html` en la Pestaña 4 (Feed de Acciones Operativas) para:
  1. Mostrar para Linda B2C únicamente los clientes accionables de los últimos 90 días (con indicador claro en la botonera y cabecera).
  2. Agregar el botón **`📥 Descargar Análisis Histórico Completo Linda B2C (.xlsx)`** que genera y descarga un archivo Excel con todos los clientes de Linda B2C de todo el tiempo (`LINDA_B2C_FULL_HISTORY`).
- [x] **T027**: Ejecutar `.\actualizar_dashboard.bat`, verificar que todas las aserciones matemáticas e inyección en HTML pasen con 0 errores y emitir reporte de auditoría al Director.
- [x] **T028**: Actualizar `spec.md` y `tasks.md` bajo metodología Spec-Kit para incorporar el panel desplegable de **Detalle de Clientes Inactivos (>2 Meses) por Vendedor** y su exportación a Excel (`.xlsx`).
- [x] **T029**: Implementar en `src/exportar_datos_dashboard.py` y `ejecucion/PROTOTIPO_DASHBOARD_VENTAS_QALIKAY.html` el listado completo `inactivosDetalle` por vendedor (clientes con `dias_inactivo > 60`, indicando si son de `1 Sola Compra` o `Recurrente Inactivo`, fecha última compra, días sin comprar, compras históricas, ticket promedio, venta total y Top 3 productos), hacer clicables tanto la tarjeta KPI `🔴 Inactivos >2 Meses` en la Ficha Individual como las columnas `1 Sola Compra (>2M)` y `Sin Comprar (>2M)` en la Matriz de Vendedores para desplegar `#seller-inactivos-detail-panel`, e incluir los botones **`📥 Descargar Excel Inactivos de este Vendedor (.xlsx)`** y **`📥 Descargar Excel Inactivos Consolidado (6 Carteras) (.xlsx)`**, ejecutando luego `.\actualizar_dashboard.bat`.
- [x] **T030**: Configurar y activar el despliegue automático Opción B (Git + GitHub + Vercel Hobby / GitHub Pages a Costo Cero S/ 0.00): auditar credenciales de Git/GitHub en el equipo (revisando configuración existente en `..\qalikay-abastecimiento`), inicializar el repositorio Git local en `Estrategia Ventas Qali Kay`, asegurar compatibilidad directa en raíz (`index.html` / `vercel.json`), vincular el repositorio remoto y verificar el flujo de auto-publicación `[4/4]` en `actualizar_dashboard.bat`.

