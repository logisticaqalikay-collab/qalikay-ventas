# Tasks: 001 - Dashboard de Inteligencia Comercial y Estrategia de Ventas B2B

## Fase 1: Arquitectura y Prototipado Base (Completado)
- [x] T001: Diseñar estructura de navegación de 5 pestañas en HTML/CSS.
- [x] T002: Implementar Pestaña 1 "Gestión por Vendedor" con Ficha Individual (HUD 6 KPIs + Mix SKUs y Proveedores + Clientes Clave) y Matriz de Vendedores.
- [x] T003: Implementar Pestaña 2 "Gestión por Proveedor y SKU" con Ficha Individual (TOP 5 Productos con Soles y Share % + Gráfico SVG + Lead time) y Matriz de Proveedores.
- [x] T004: Implementar Pestaña 3 "Comparativa Histórica" con gráfico SVG multi-período y tabla analítica mensual.
- [x] T005: Implementar Pestaña 4 "Feed de Acciones Operativas" con alertas automáticas.
- [x] T006: Implementar Pestaña 5 "Bandejas WhatsApp" con botón de copiado limpio.

## Fase 2: Conexión con Datos Reales de Defontana (Pendiente de Ejecución)
- [ ] T007: Diseñar la interfaz de carga de archivos (Dropzone/Input file) para importar el reporte `INF_VENTAS_DETALLADAS` de Defontana directamente en el Dashboard.
- [ ] T008: Incorporar parser de Excel/CSV en cliente (`xlsx.full.min.js` embebido) para procesar columnas: Fecha, Documento, RUC, Cliente, Vendedor, SKU, Descripción, Monto Neto y Margen.
- [ ] T009: Configurar la tabla de equivalencias para asociar cada marca (ej. *D'Nattive*) a su Proveedor titular oficial.
- [ ] T010: Conectar el cálculo automático de los 6 KPIs y los TOP 5 productos por proveedor con la data parseada de Defontana.

## Fase 3: Despliegue y Validación (Pendiente)
- [ ] T011: Auditar experiencia visual y móvil con estándar de diseño `impeccable`.
- [ ] T012: Publicar prototipo en URL web gratuita (Vercel o GitHub Pages) para acceso directivo sin costo.
