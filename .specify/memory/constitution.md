# Qali Kay Ventas & Inteligencia Comercial Constitution

## Core Principles

### I. Presupuesto $0.00 Adicional
Se utilizan estrictamente herramientas, frameworks y hosting gratuitos. No se emplearán plugins de pago, APIs pagas, ni licencias de software por usuario. El dashboard y sus módulos corren sobre tecnologías web abiertas (HTML5, CSS moderno, JavaScript nativo, SVG) y alojamiento gratuito (Vercel / GitHub Pages).

### II. Aislamiento Total de Abastecimiento con Lectura Compartida de Descargas
Queda **terminantemente prohibido** modificar, sobreescribir o alterar códigos, librerías, dependencias o scripts de `qalikay-abastecimiento`. `qalikay-ventas` es un ecosistema 100% autónomo. Sin embargo, para no sobrecargar el ERP Defontana con descargas duplicadas, `qalikay-ventas` lee en modo de solo lectura los reportes ya descargados por el bot RPA existente.

### III. Base Histórica 2025–2026 con Ventana Incremental de 90 Días (3 Meses)
El sistema analiza el histórico consolidado 2025–2026 en formato Parquet. Las actualizaciones diarias procesan una **ventana rodante de los últimos 90 días (3 meses)** (alineada a la ventana de abastecimiento). El motor aplica `upsert` por clave única (`Nombre_Doc + Nro_Doc + Cod_Producto`) para absorber automáticamente Notas de Crédito, devoluciones y anulaciones pasadas sin tener que reprocesar los 24 meses completos.

### IV. Determinismo Matemático Absoluto (Prohibición de LLM para Cálculos)
Todos los cálculos (ventas netas, tickets promedio, cumplimientos, márgenes, % share, proyecciones) se ejecutan mediante código determinista puro (Python / DuckDB / JavaScript ES6). Queda **estrictamente prohibido usar Modelos de Lenguaje (LLMs) para calcular sumatorias o promedios matemáticos**.

### V. Política de Eficiencia y Ahorro Extremo de Tokens
- **Divulgación Progresiva:** Prohibido volcar tablas masivas de datos crudos en el prompt o contexto del LLM. Los datos masivos se procesan localmente en scripts de Python o Parquet; el LLM solo recibe esquemas, métricas agregadas o resúmenes ejecutivos.
- **Tareas Atómicas y Acotadas:** El Director delega al Ejecutor tareas puntuales con alcance exacto de archivos para evitar dispersión y consumo innecesario de tokens.
- **Persistencia en Disco:** Las decisiones, especificaciones y estado se almacenan en archivos estructurados (`specs/`, `data/`, `BLUEPRINT`), evitando tener que re-explicar el contexto en cada turno.

### VI. Diferenciación Estricta Proveedor vs Marca
- Un **Proveedor** es el laboratorio farmacéutico, importador o distribuidor titular con quien se negocian plazos de crédito, márgenes y condiciones comerciales (ej. Laboratorios Bagó, Medifarma, Nutrivas, Molinos del Mundo).
- Una **Marca** o línea de producto (ej. *D'Nattive*, *Santiveri*, *Oriundos*) pertenece a un proveedor. En los reportes analíticos, KPIs y TOP 5 SKUs, todo producto debe estar catalogado bajo su proveedor titular oficial.

### VII. Confidencialidad Comercial y Segmentación de Vistas
- En la fase de prueba, la fuerza de ventas no tiene acceso al dashboard global consolidado.
- La jefatura o dirección comparte a cada vendedor exclusivamente la captura de su **Ficha Individual (Pestaña 1)** y los textos generados de las **Bandejas de WhatsApp (Pestaña 5)**.
- La totalidad de las 5 pestañas está reservada para el nivel directivo.

### VIII. Gestión Activa de Reactivación B2C y Cartera B2B
El sistema monitorea la frecuencia de compra:
- **Consumidores B2C en ciclo de reposición (25 a 35 días):** Alerta preventiva de fin de frasco.
- **B2C vencidos (> 35 a 60 días) e Inactivos (> 60 días):** Alertas de rescate con ofertas y mensajes listos para WhatsApp sin caracteres deformados.
- **Clientes B2B sin compra (> 60 días):** Alertas rojas de riesgo de fuga.

### IX. Estándar UX/UI con Skill Impeccable (Modo Operate)
El diseño del Dashboard debe cumplir con los principios de diseño de alta densidad de datos: semáforos de alta legibilidad, números tabulares alineados a la derecha, gráficos SVG vectoriales nítidos, interactividad fluida sin dependencias externas (offline-first) y optimización móvil para botones de WhatsApp (touch targets >= 48px).

---

## Suite de Skills y Herramientas Autorizadas

1. **Spec-Kit Suite:**
   - `/speckit-constitution`: Gobernanza de estos principios.
   - `/speckit-specify`: Especificación formal de requerimientos en `spec.md`.
   - `/speckit-clarify`: **PASO MANDATORIO** para resolver dudas y reglas con el Director General antes de codificar.
   - `/speckit-plan`: Diseño de arquitectura técnica en `plan.md`.
   - `/speckit-tasks`: Desglose atómico de tareas en `tasks.md`.
   - `/speckit-analyze`: **FILTRO DE CALIDAD MANDATORIO** previo a implementar (`validation-report.md`).
   - `/speckit-implement`: Ejecución exclusiva de código en `/ejecucion/`.
   - `/speckit-converge`: Evaluación y control de regresión.
2. **Impeccable Skill:**
   - Modo `Operate` para auditoría y pulido del Dashboard comercial.
3. **gstack Suite:**
   - `/gstack-review` para revisión estricta de diffs y `/gstack-browse` para validación en navegador.
4. **Herramientas Nativas de Antigravity:**
   - `run_command`, `write_file`, `edit_file`, `read_file`. Cero MCPs pesados que no aporten valor directo.

---

## Governance y Roles

- **Agente Director (Especialista en IA y Arquitectura):** Custodio de esta Constitución. Ejecuta las fases de especificación, clarificación, planificación y análisis. Gobierna el consumo eficiente de tokens.
- **Agente Ejecutor:** Opera en la carpeta `/ejecucion/`. Construye el código ejecutando `speckit-implement` sobre las tareas aprobadas, sin violar ningún principio de esta Constitución.
- **Usuario (Director General - Cristian Gutiérrez):** Soberanía total. Valida y ratifica cada hito y especificación.

**Version**: 2.0.0 | **Ratified**: 2026-10-23
