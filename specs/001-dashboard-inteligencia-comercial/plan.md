# Feature Plan: 001 - Dashboard de Inteligencia Comercial y Estrategia de Ventas B2B

## 1. Arquitectura Técnica
- **Frontend:** SPA (Single Page Application) en archivo autónomo HTML5 (`PROTOTIPO_DASHBOARD_VENTAS_QALIKAY.html`).
- **Estilos:** CSS embebido en `<style>`, variables CSS para paleta ejecutiva (navy, emerald, crimson, slate).
- **Interactividad & Gráficos:** JavaScript ES6 nativo, renderizado dinámico de SVG para gráficos de barras y líneas evolutivas.
- **Data Engine:**
  - Capa 1: Modelo reactivo en memoria (`datosComerciales`).
  - Capa 2 (Siguiente fase): Parser de reportes de Defontana (`INF_VENTAS_DETALLADAS`) vía Excel/CSV con SheetJS o script de ingesta.

## 2. Componentes del Dashboard
- **HUD Global y Selectores:** Dropdowns accesibles para alternar Vendedor y Proveedor.
- **Renderers SVG:**
  - `renderSellerChart()`: Barras de distribución de ventas por proveedor para el vendedor activo.
  - `renderSupplierSellerChart()`: Barras de aporte por vendedor para el proveedor activo.
  - `renderEvolutionChart()`: Gráfico multi-período interactivo de meses cerrados + mes en curso.
- **Módulo WhatsApp:** Función de codificación limpia de URI y `navigator.clipboard.writeText()`.

## 3. Control de Calidad y Puertas de Aprobación
- Validación de sintaxis JS sin dependencias rotas.
- Modo Operate de `impeccable`: legibilidad numérica, badges de estado y diseño mobile-friendly.
