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

## FASE 2: INGESTA, ALMACÉN PARQUET Y VENTANA RODANTE DE 90 DÍAS (EN CURSO 🟡)
- [ ] **T007**: Crear el script de ingesta `src/etl_ventas_defontana.py` para parsear el reporte `INF_VENTAS_DETALLADAS` (.xlsx/.csv exportado por el RPA de abastecimiento en ventana de 90 días), normalizando fechas, tipos numéricos, clientes, RUC y montos netos.
- [ ] **T008**: Implementar la lógica de deducción de Notas de Crédito (NC), restando unidades y montos netos del vendedor y producto correspondiente.
- [ ] **T009**: Implementar el filtro de exclusión estricto para las 3 cuentas catalogadas como *"Consumo Interno"*.
- [ ] **T010**: Construir el módulo de almacenamiento `data/ventas_2025_2026.parquet` y el algoritmo de ventana rodante de **90 días (3 meses)** con `upsert` por clave compuesta `Nombre_Doc + Nro_Doc + Cod_Producto`.
- [ ] **T011**: Configurar el maestro de equivalencias de Marcas a Proveedores Titulares (ej. *D'Nattive* al laboratorio titular, *Oriundos* a *Nutrivas*, *Santiveri* a *Molinos del Mundo*).

---

## FASE 3: MOTOR DE REGLAS DE CARTERAS Y GESTIÓN DE ALERTAS (PENDIENTE ⚪)
- [ ] **T012**: Implementar la segmentación determinista de las 6 carteras comerciales:
  - *Enrique García* (B2B campo).
  - *Walter Gutiérrez* (excluyendo automáticamente la cuenta UNALM).
  - *Cristian Gutiérrez* (excluyendo automáticamente la cuenta Organa; incluyendo *Whitnin Tesen* en Piura).
  - *Carlos Cuadros* (fusionando la cartera histórica de Joel García).
  - *Linda / Zully — B2B* (comprobantes > S/ 400.00).
  - *Linda / Zully — B2C* (comprobantes <= S/ 400.00).
- [ ] **T013**: Implementar el motor de ciclo B2C de 25 días (Alertas Preventivas días 25–35, Seguimiento días 36–60, Rescate > 60 días).
- [ ] **T014**: Implementar el motor de ciclo B2B de 15 días (Alerta preventiva día 10, fuga día 20, anomalía de caída de ventas >= 30%).
- [ ] **T015**: Implementar el cruce de cartera vencida con `CUENTAS POR COBRAR.xlsx` para disparar alertas de cobranza y condición de pago previo.
- [ ] **T016**: Cargar la matriz de Lead Times por proveedor (Rápidos 1-2d, Molinos del Mundo miércoles, demoras mayores, proveedores en liquidación).

---

## FASE 4: VINCULACIÓN AL DASHBOARD (FRONTEND BINDING) (PENDIENTE ⚪)
- [ ] **T017**: Crear el script `src/exportar_datos_dashboard.py` que consolida los cálculos deterministas y genera el snapshot reactivo `data/datos_comerciales.json`.
- [ ] **T018**: Conectar `PROTOTIPO_DASHBOARD_VENTAS_QALIKAY.html` a la lectura de `data/datos_comerciales.json`, reemplazando el objeto mock en memoria.
- [ ] **T019**: Incorporar en el Dashboard un componente visual de carga (Dropzone) con SheetJS embebido (`xlsx.full.min.js` offline) para permitir importar reportes de Defontana directamente desde la interfaz web sin terminal.

---

## FASE 5: AUDITORÍA UX Y DESPLIEGUE CLOUD (PENDIENTE ⚪)
- [ ] **T020**: Auditar el Dashboard utilizando la skill `impeccable` en modo `Operate` (alto contraste, tipografía no menor a 12px, números tabulares alineados a la derecha y touch targets móviles de WhatsApp >= 48px).
- [ ] **T021**: Configurar el despliegue automático gratuito en GitHub Pages / Vercel para acceso directivo en la nube (S/ 0.00).
