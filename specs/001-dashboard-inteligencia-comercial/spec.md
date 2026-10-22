# Feature Specification: 001 - Dashboard de Inteligencia Comercial y Estrategia de Ventas B2B

## 1. Overview y Objetivos
Construir el sistema y dashboard comercial interactivo para Qali Kay S.A.C, permitiendo visibilidad ejecutiva a la dirección y gestión individualizada a la fuerza de ventas con costo $0.00.

## 2. User Stories
- **US1 (Director):** Como Director General, quiero visualizar el avance consolidado de ventas del mes en curso y meses anteriores, con proyección de cierre y margen para tomar decisiones estratégicas.
- **US2 (Vendedor/Jefatura):** Como Jefatura/Vendedor, quiero consultar la Ficha Individual del vendedor con sus 6 KPIs, mix de SKUs y proveedores, y clientes clave sin revelar la información de otros vendedores.
- **US3 (Gestión de Proveedores):** Como Director de Compras/Ventas, quiero analizar en la Ficha del Proveedor su TOP 5 de productos (en S/ y % share) y la venta que cada vendedor aporta a ese proveedor.
- **US4 (Operaciones):** Como equipo comercial, quiero recibir alertas operativas (quiebres, fuga de clientes) y generar mensajes limpios de WhatsApp listos para copiar con 1 clic.

## 3. Requerimientos Funcionales
- **RF1 - 5 Pestañas Obligatorias:**
  1. Gestión por Vendedor (Ficha Individual por defecto con HUD 6 KPIs + Mix SKUs y Proveedores + Clientes Clave; Subvista Matriz).
  2. Gestión por Proveedor y SKU (Ficha Individual con TOP 5 SKUs en S/ y % + Gráfico SVG por vendedor + Lead time/crédito; Subvista Matriz).
  3. Comparativa Histórica (Gráfico evolutivo multi-período SVG + tabla numérica completa).
  4. Feed de Acciones Operativas (Alertas clasificadas por severidad).
  5. Bandejas WhatsApp (Mensajes limpios sin caracteres deformados con botón Copiar).
- **RF2 - Distinción Proveedor vs Marca:** En el modelo de datos, marcas (ej. *D'Nattive*) deben pertenecer a su proveedor titular oficial.
- **RF3 - Modo Offline y Autónomo:** Cero dependencias externas o CDNs.

## 4. Criterios de Aceptación
- [ ] Todas las 5 pestañas cambian fluidamente sin recargar la página.
- [ ] Los selectores de vendedor y proveedor actualizan instantáneamente los KPIs, tablas y gráficos SVG.
- [ ] El botón de WhatsApp copia el texto limpio al portapapeles y abre `https://wa.me/...`.
- [ ] No existen errores en la consola de JavaScript.
