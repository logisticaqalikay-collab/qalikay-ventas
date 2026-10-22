# Qali Kay Ventas & Inteligencia Comercial Constitution

## Core Principles

### I. Presupuesto $0.00 Adicional
Se utilizan estrictamente herramientas, frameworks y hosting gratuitos. No se emplearán plugins de pago, APIs pagas, ni licencias de software por usuario. El dashboard y sus módulos corren sobre tecnologías web abiertas (HTML5, CSS moderno, JavaScript nativo, SVG) y alojamiento gratuito (Vercel / GitHub Pages).

### II. Aislamiento Total respecto a Otros Proyectos
Queda **terminantemente prohibido** modificar, sobreescribir o alterar códigos, librerías, dependencias o scripts de `qalikay-abastecimiento` o cualquier otro módulo. `qalikay-ventas` es un ecosistema 100% autónomo.

### III. Diferenciación Estricta Proveedor vs Marca
- Un **Proveedor** es el laboratorio farmacéutico, importador o distribuidor titular con quien se negocian plazos de crédito, márgenes y condiciones comerciales (ej. Laboratorios Bagó, Medifarma, Nutrivas, etc.).
- Una **Marca** o línea de producto (ej. *D'Nattive*) pertenece a un proveedor. En los reportes analíticos, KPIs y TOP 5 SKUs, todo producto debe estar catalogado bajo su proveedor titular oficial.

### IV. Confidencialidad Comercial y Segmentación de Vistas
- En la fase de prueba, la fuerza de ventas no tiene acceso al dashboard global consolidado.
- La jefatura o dirección comparte a cada vendedor exclusivamente la captura de su **Ficha Individual (Pestaña 1)** y los textos generados de las **Bandejas de WhatsApp (Pestaña 5)**.
- La totalidad de las 5 pestañas está reservada para el nivel directivo.

### V. Base Histórica 2025 + 2026 con Ventana Incremental de 60 Días
El sistema analiza el histórico consolidado 2025–2026. Las actualizaciones incrementales procesan una **ventana rodante de los últimos 60 días (2 meses)** para capturar de forma automática Notas de Crédito, devoluciones, anulaciones o modificaciones de documentos pasados sin tener que reprocesar los 24 meses completos.

### VI. Gestión Activa de Reactivación B2C y Cartera B2B
El sistema monitorea la frecuencia de compra:
- **Consumidores B2C en ciclo de reposición (25 a 35 días):** Alerta preventiva de fin de frasco.
- **B2C vencidos (> 35 a 60 días) e Inactivos (> 60 días):** Alertas de rescate con ofertas y mensajes listos para WhatsApp sin caracteres deformados.
- **Clientes B2B sin compra (> 60 días):** Alertas rojas de riesgo de fuga.

### VII. Estándar UX/UI con Skill Impeccable (Modo Operate)
El diseño del Dashboard debe cumplir con los principios de diseño de alta densidad de datos: semáforos de alta legibilidad, números tabulares alineados a la derecha, gráficos SVG vectoriales nítidos, interactividad fluida sin dependencias externas (offline-first) y optimización móvil para botones de WhatsApp.

---

## Governance y Roles

- **Agente Director (Especialista en IA y Arquitectura):** Custodio de esta Constitución. Ejecuta las fases de especificación (`speckit-specify`), clarificación (`speckit-clarify`), planificación (`speckit-plan`) y desglose de tareas (`speckit-tasks`).
- **Agente Ejecutor:** Opera en la carpeta `/ejecucion/`. Construye el código ejecutando `speckit-implement` sobre las tareas aprobadas, sin violar ningún principio de esta Constitución.
- **Usuario (Director General):** Soberanía total. Valida y ratifica cada hito y especificación.

**Version**: 1.0.0 | **Ratified**: 2026-10-22
