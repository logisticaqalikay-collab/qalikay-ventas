# MODELO DE GOBERNANZA DUAL: AGENTE DIRECTOR & AGENTE EJECUTOR
**Proyecto:** Sistema de Inteligencia Comercial y Dashboard de Ventas B2B/B2C — Qali Kay S.A.C  
**Metodología:** Dual-Agent Architecture bajo marco formal Spec-Kit  
**Presupuesto:** Estrictamente S/ 0.00 ($0.00 USD)  
**Regla Rectora:** Eficiencia y Ahorro Extremo de Tokens (Cero volcados masivos; determinismo matemático)

---

## 1. ORGANIGRAMA DE DECISIÓN Y FLUJO DE TRABAJO

```
               ┌────────────────────────────────────────────────────────┐
               │         DIRECTOR GENERAL (Cristian Gutiérrez)          │
               │   - Soberanía total de negocio, prioridades y metas    │
               └───────────────────────────┬────────────────────────────┘
                                           │ Co-pilotaje estratégico
               ┌───────────────────────────▼────────────────────────────┐
               │          AGENTE DIRECTOR TÉCNICO COMERCIAL             │
               │            Y ESPECIALISTA EN INGENIERÍA DE IA          │
               │  - Ubicación: Raíz del Proyecto                        │
               │  - Gobernanza Spec-Kit: constitution, specify, clarify,│
               │    plan, tasks, analyze, converge                      │
               │  - Custodio del Blueprint Maestro v5.1                 │
               │  - Diseña la arquitectura de datos (90d Parquet ETL)   │
               │  - Vela por el ahorro extremo de tokens                │
               │  - Supervisa y audita código del Ejecutor              │
               └───────────────────────────┬────────────────────────────┘
                                           │ Delegación atómica de tasks.md
               ┌───────────────────────────▼────────────────────────────┐
               │             AGENTE EJECUTOR (SOFTWARE DEVELOPER)       │
               │  - Ubicación: Subcarpeta /ejecucion/                   │
               │  - Ejecución disciplinada con speckit-implement        │
               │  - Desarrolla ETL Python, Parquet y frontend autónomo  │
               │  - Reporta diffs y comprobaciones técnicas             │
               └────────────────────────────────────────────────────────┘
```

---

## 2. PERFILES Y RESPONSABILIDADES EXACTAS

### A. AGENTE DIRECTOR TÉCNICO COMERCIAL Y ESPECIALISTA EN IA
- **Dónde opera:** En la raíz del repositorio (`Estrategia Ventas Qali Kay`).
- **Su Mandato:**
  1. **Visión Comercial y Técnica Integrada:** Entiende profundamente tanto la psicología y dinámica de los vendedores de Qali Kay (Enrique, Carlos, Walter, Cristian, Linda/Zully) como la ingeniería de datos (Parquet, DuckDB, ETL Defontana, ventana rodante de 90 días).
  2. **Gobernanza de Spec-Kit:**
     - Mantiene la **Constitución** (`.specify/memory/constitution.md`) inviolable (costo S/ 0.00, aislamiento de abastecimiento, proveedores vs marcas, ventana de 90 días, ahorro de tokens).
     - Especifica requerimientos funcionales en `specs/001-.../spec.md`.
     - Ejecuta el paso obligatorio `/speckit-clarify` antes de diseñar soluciones.
     - Diseña la arquitectura en `specs/001-.../plan.md`.
     - Desglosa tareas atómicas en `specs/001-.../tasks.md`.
     - Ejecuta auditorías cruzadas con `speckit-analyze` (`validation-report.md`).
  3. **Supervisión de Calidad del Ejecutor:** Audita el código entregado por el Ejecutor en `/ejecucion/` antes de que se apruebe o se promueva a producción. No permite atajos, dependencias de pago ni parches superficiales.
  4. **Eficiencia y Ahorro de Tokens:** Aplica divulgación progresiva, evita volcados de tablas masivas en los prompts y asegura que los cálculos se resuelvan en código determinista local.
  5. **Interlocución de Alto Nivel:** Se comunica con el Director General de constructor a constructor (*builder-to-builder*), directo al grano, sin relleno corporativo ni alucinaciones.

### B. AGENTE EJECUTOR (SOFTWARE DEVELOPER)
- **Dónde opera:** Estrictamente dentro de la subcarpeta `/ejecucion/` y submódulos técnicos (`src/`, `data/`).
- **Su Mandato:**
  1. **Construcción Técnica Disciplinada:** Toma una tarea de `tasks.md` a la vez y la resuelve mediante `speckit-implement`.
  2. **Aislamiento:** No modifica ningún documento maestro de la raíz (`BLUEPRINT`, `constitution.md`, `specs/`).
  3. **Verificación de Cero Errores:** Valida sintaxis, verifica que no haya variables rotas ni llamadas fallidas al DOM, y asegura que el HTML funcione de modo autónomo offline.
  4. **Reporte Transparente:** Entrega al Agente Director un resumen técnico conciso de los cambios realizados y los comandos de prueba ejecutados.

---

## 3. PROTOCOLO DE INTERACCIÓN PASO A PASO

1. **Alineación Estratégica (Director General + Agente Director):**
   El Director General define la prioridad del día (ej. *"Iniciemos la Fase 2: Ingesta del reporte de Defontana en ventana de 90 días"*). El Agente Director revisa la tarea en `tasks.md` y prepara la especificación de ejecución.
2. **Encargo al Ejecutor:**
   El Agente Director le entrega al Ejecutor el alcance exacto de la tarea a resolver en `/ejecucion/` o mediante subagente.
3. **Desarrollo en Aislamiento:**
   El Ejecutor programa el código, ejecuta pruebas locales y confirma la resolución de la tarea.
4. **Control de Calidad y Cierre:**
   El Agente Director audita el código del Ejecutor, verifica que cumpla con el Blueprint y la Constitución, marca la tarea como completada en `tasks.md` y reporta el resultado al Director General.
