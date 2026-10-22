# AGENTS.md — Reglas y Guía de Operación para Agentes en Qali Kay

## 1. Ethos y Reglas de Conducta (gstack v1.91)

- **Boil the Ocean**: La completitud es económica. Haz las cosas completas: casos borde, rutas de error, código limpio y robusto. No tomes atajos sin consultarlo explícitamente.
- **Search Before Building**: Conoce qué existe antes de decidir construir. No reinventes la rueda; usa código probado y soluciones de primeros principios.
- **User Sovereignty**: La IA propone y recomienda; el usuario siempre decide. Pide confirmación antes de alterar la dirección establecida por el usuario.
- **The Reuse Ladder**:
  1. Un helper, utilitario o patrón que ya esté en este repositorio.
  2. La biblioteca estándar del lenguaje o plataforma.
  3. Características nativas de la plataforma (CSS moderno sobre JS, HTML semántico).
  4. Una dependencia ya instalada (nunca agregar librerías pesadas si pocas líneas de código nativo lo resuelven).
- **Voz y Comunicación**: Directa, concreta, de constructor a constructor (*builder-to-builder*). Nombra los archivos, funciones, comandos y el impacto visual. Sin relleno ni lenguaje corporativo artificial.

---

## 2. Reglas Específicas de Negocio — Qali Kay S.A.C

- **Costo Cero ($0.00 / S/ 0.00)**: No incorporar servicios, plugins, APIs o herramientas de pago. Todo debe funcionar con tecnologías web abiertas y hosting gratuito (Vercel, GitHub Pages, Google Apps Script, SheetDB / Webhooks gratuitos).
- **Diferenciación Estricta Proveedor vs Marca**:
  - Un **Proveedor** es el laboratorio farmacéutico, importador o distribuidor titular con quien se negocian plazos de pago y márgenes (ej. Laboratorios Bagó, Medifarma, etc.).
  - Una **Marca** o línea de producto (ej. *D'Nattive*) pertenece a un proveedor. En los reportes y análisis, clasificar los SKUs bajo su proveedor oficial.
- **Confidencialidad Comercial**:
  - En la fase de prueba, la fuerza de ventas no accede al dashboard global.
  - La jefatura les comparte su ficha individual de la **Pestaña 1** (captura de pantalla) y los textos generados de la **Pestaña 5** (WhatsApp).
  - Los directivos tienen acceso a la totalidad de las 5 pestañas.
- **Convivencia de Proyectos**: Este proyecto convive con `qalikay-abastecimiento` (módulo RPA de compras y kardex). No modificar ni sobreescribir dependencias de ese u otros módulos.

---

## 3. Estructura Obligatoria del Dashboard Comercial (5 Pestañas)

1. **Pestaña 1: Gestión por Vendedor**:
   - *Ficha Individual (Por defecto)*: Selector por vendedor, HUD de 6 KPIs (Ticket Promedio, Venta Mes en Curso, Meta, Cumplimiento %, Proyección de Cierre, Clientes Activos), Mix de SKUs y Proveedores, y Top Clientes Clave.
   - *Matriz Comparativa*: Tabla consolidada con avance de todo el equipo de ventas.
2. **Pestaña 2: Gestión por Proveedor y SKU**:
   - *Ficha Individual (Por defecto)*: Selector de proveedor, **TOP 5 Productos con su valor en Soles (S/) y su participación (% share)**, Gráfico de barras SVG de venta por vendedor para ese proveedor, y tarjeta de Lead Time, días de crédito y promociones.
   - *Matriz de Proveedores*: Tabla consolidada con volumen y share total.
3. **Pestaña 3: Comparativa Histórica**:
   - Gráfico evolutivo multi-período SVG (meses cerrados + mes en curso) y tabla analítica mensual completa.
4. **Pestaña 4: Feed de Acciones Operativas**:
   - Alertas en vivo de quiebres de stock, fuga de clientes inactivos, márgenes reducidos y créditos retenidos.
5. **Pestaña 5: Bandejas WhatsApp Limpias**:
   - Generación de mensajes listos para copiar con un botón verde (`Copiar Mensaje`) y pegar directo en WhatsApp sin caracteres deformados.
