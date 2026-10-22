# PAQUETE MAESTRO DE REANUDACIÓN DE SESIÓN - ESTRATEGIA VENTAS QALI KAY
**Fecha:** 22 de Octubre de 2026  
**Empresa:** Qali Kay S.A.C  
**Proyecto:** Sistema y Dashboard de Gestión Comercial y Estrategia de Ventas B2B  
**Estado:** Prototipo interactivo 100% funcional y ajustado con 5 pestañas operativas.

---

## 📌 INSTRUCCIÓN PARA EL AGENTE DE ANTIGRAVITY EN LA LAPTOP
> Si estás abriendo un nuevo chat en tu laptop, adjunta o copia este archivo y dile al agente:  
> **"Lee este archivo y continuemos inmediatamente el proyecto de Ventas de Qali Kay donde lo dejamos"**.  
> El agente entenderá el 100% del contexto, decisiones y arquitectura sin que tengas que repetir nada.

---

## 1. OBJETIVO DEL PROYECTO
Construir una solución comercial y directiva integral para Qali Kay S.A.C (distribuidora farmacéutica/nutracéutica) que permita:
1. **A la Dirección:** Visibilidad en tiempo real de ventas, cumplimiento de metas, margen, desempeño por vendedor, concentración por proveedor y SKUs clave.
2. **A la Fuerza de Ventas:** Herramienta ágil y personalizada para consultar metas, avance del mes en curso, proyección, cartera de clientes y mensajes listos para WhatsApp.
3. **Estrategia Piloto (Fase de Prueba):** 
   - **Directivos:** Acceso mediante un enlace web o archivo HTML interactivo completo.
   - **Vendedores:** La dirección o jefatura les despacha capturas de su Ficha Individual (Pestaña 1) y los bloques de texto de las Bandejas de WhatsApp (Pestaña 5) para mantener confidencialidad entre pares.
4. **Restricción Innegociable:** Costo S/ 0.00 (sin software de pago, sin licencias caras).

---

## 2. ARQUITECTURA DE LAS 5 PESTAÑAS (ÚLTIMA VERSIÓN APROBADA)

### Pestaña 1: "Gestión por Vendedor"
- **Ficha Individual (Vista principal):**
  - Selector dinámico por vendedor (Junio, Jefferson, etc.).
  - HUD con 6 KPIs clave: Venta Mes en Curso, Meta del Mes, Cumplimiento %, Proyección de Cierre, Ticket Promedio y Clientes Activos.
  - **Mix de SKUs y Proveedores:** Desglose del catálogo vendido por ese vendedor (se ajustó para mostrar SKUs y Proveedores en lugar de marcas).
  - **Top Clientes Clave:** Cartera prioritaria con montos y frecuencia.
- **Matriz de Vendedores (Subvista):** Tabla comparativa de todos los vendedores con avance, cumplimiento y ranking.
*(Nota: La subpestaña de tarjetas se eliminó a solicitud del usuario).*

### Pestaña 2: "Gestión por Proveedor y SKU"
- **Ficha Individual por Proveedor (Vista principal):**
  - Selector por proveedor.
  - **TOP 5 Productos por Proveedor:** Muestra para cada SKU su valor vendido en Soles (S/) y su participación porcentual (**share %**).
  - Gráfico de barras SVG interactivo con la venta que cada vendedor aportó a dicho proveedor.
  - Indicadores operativos: Lead Time promedio (días), días de crédito comercial y promociones activas.
- **Matriz de Proveedores (Subvista):** Tabla consolidada de todos los proveedores con volumen en soles y % de share total.
*(Nota: Se eliminó el cuadro general y tarjetas de esta pestaña).*

### Pestaña 3: "Comparativa Histórica"
- Gráfico SVG multi-período para ver la evolución de ventas a lo largo de los meses cerrados y el mes en curso.
- Tabla numérica mensualizada completa.
*(Nota: Se eliminó la ficha por proveedor de esta pestaña).*

### Pestaña 4: "Feed de Acciones Operativas"
- Motor de alertas prioritarias clasificadas por criticidad (Crítico, Advertencia, Oportunidad).
- Alertas de: quiebre de stock inminente, clientes con riesgo de fuga (+30 días sin comprar), proveedores con margen bajo y pedidos retenidos por crédito.

### Pestaña 5: "Bandejas de WhatsApp"
- Generador de mensajes operativos limpios para vendedores.
- Formato limpio sin caracteres raros, listo para copiar con un botón verde (`Copiar Mensaje`) y pegar directamente en WhatsApp Web o celular.

---

## 3. APRENDIZAJES Y REGLAS DE NEGOCIO IDENTIFICADAS
1. **Diferenciación Proveedor vs Marca:** En la versión final, no confundir marcas con proveedores (ejemplo: *D'Nattive* es una marca de producto; el proveedor es el laboratorio o fabricante titular). En el prototipo actual los datos son ficticios para validar la UX; en la fase de implementación se alimentarán del ERP Defontana / Google Sheets.
2. **Mes en Curso vs Meses Cerrados:** El sistema debe evaluar tanto el avance vivo del mes corriente (proyección) como los históricos cerrados.
3. **Respeto a otros módulos:** Este proyecto convive con `qalikay-abastecimiento` (automatización RPA de compras y kardex) en el mismo ecosistema. No se deben sobreescribir ni mezclar sus dependencias.

---

## 4. ARCHIVOS DEL PROYECTO
1. `PROTOTIPO_DASHBOARD_VENTAS_QALIKAY.html`: Archivo HTML standalone interactivo (160 KB) con estilos embebidos, sin dependencias externas pesadas.
2. `BLUEPRINT_SISTEMA_VENTAS_QALIKAY.md`: Especificación técnica del sistema comercial.
3. `CONTEXTO_MAESTRO_VENTAS_QALI_KAY.md`: Reglas del proceso B2B y categorización.
4. `Manual_Proceso_Comercial_B2B_QK_COM_01.md`: Manual operativo para el equipo.
5. `Guia_Rapida_Proceso_Comercial_QK_COM_01.docx`: Guía rápida para el vendedor.
6. `Contactos de Farmacias - Consolidado Final.xlsx`: Base de datos de clientes y contactos.

---

## 5. ESTADO DE LAS CUENTAS Y MIGRACIÓN PENDIENTE
- **PC Actual:** Conectada a OneDrive `aa.inkacomex@outlook.com`.
- **Cuenta Definitiva del Usuario:** `cgutierrez_r@hotmail.com` (la que está en la laptop).
- **Tarea programada para después:** Cambiar la sesión de OneDrive de la PC a `cgutierrez_r@hotmail.com` y consolidar las carpetas sin perder historial ni configuraciones.
