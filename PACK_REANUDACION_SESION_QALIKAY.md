# DOSSIER DE RELEVO Y TRASPASO DIRECTIVO: ESTRATEGIA VENTAS QALI KAY
**Fecha:** 23 de Octubre de 2026  
**Empresa:** Qali Kay S.A.C ("Somos tus aliados en salud natural")  
**Director General:** Cristian Gutiérrez  
**Cargo del Agente Entrante:** Director Técnico Comercial y Especialista en Ingeniería de IA  
**Metodología:** Spec-Kit (`constitution` ➔ `specify` ➔ `clarify` (mandatorio) ➔ `plan` ➔ `tasks` ➔ `analyze` (mandatorio) ➔ `implement` ➔ `impeccable`)  
**Modelo de Gobernanza:** Dual-Agent Architecture (Director en Raíz / Ejecutor en `/ejecucion/`)  
**Presupuesto Innegociable:** S/ 0.00 ($0.00 USD)  
**Mandato de Eficiencia:** Ahorro extremo de tokens (cero volcados masivos en prompt; código determinista)

---

## ⚠️ ADVERTENCIA CRÍTICA PARA EL NUEVO AGENTE DIRECTOR
> **NO COMETAS EL ERROR DE VER ESTE PROYECTO COMO UN SIMPLE PROTOTIPO VISUAL HTML.**  
> El dashboard visual es solo la punta del iceberg. Debajo existe una arquitectura técnica y de datos completa con reglas matemáticas deterministas de negocio que debes gobernar con rigor:
> - Base de datos consolidada 2025–2026 en formato Parquet (`data/ventas_2025_2026.parquet`).
> - **Ventana rodante de 90 días (3 meses):** Aprovecha directamente los reportes exportados por la automatización RPA existente de `qalikay-abastecimiento` (en modo solo lectura, sin alterar su código) para absorber Notas de Crédito (NC), devoluciones y anulaciones con `upsert` por clave compuesta `Nombre_Doc + Nro_Doc + Cod_Producto`.
> - **Política de ahorro extremo de tokens:** Prohibido volcar tablas masivas de datos crudos al prompt. El procesamiento se ejecuta en scripts Python locales deterministas. Cero uso de LLMs para cálculos numéricos.
> - **Suite formal de Skills:** Spec-Kit suite (con `clarify` y `analyze` como pasos obligatorios no omitibles), `impeccable` en modo `Operate` para el pulido UX del dashboard, y `gstack` (`gstack-review` y `gstack-browse`).
> - Aislamiento 100% total respecto a `qalikay-abastecimiento`.
> - Motor de 6 carteras comerciales deterministas (Enrique, Walter s/ UNALM, Cristian s/ Organa, Carlos C + ex Joel, Linda/Zully B2B > S/ 400 y Linda/Zully B2C <= S/ 400).
> - Diferenciación estricta entre Proveedor titular (Laboratorio) y Marca (ej. *D'Nattive* es marca, no proveedor).
> - Matriz de lead times por proveedor (1-2 días, entrega semanal miércoles Santiveri, mayores demoras, liquidaciones).
> - Control crediticio cruzado con `CUENTAS POR COBRAR.xlsx` (condicionar despachos a cancelación previa).

---

## 1. LOS PRINCIPIOS INQUEBRANTABLES DE LA CONSTITUCIÓN
1. **Presupuesto $0.00:** Solo tecnologías web y herramientas libres (Python, Parquet, DuckDB, SheetJS, Vercel/GitHub Pages). Cero suscripciones SaaS de pago.
2. **Aislamiento Total de Abastecimiento con Lectura Compartida de 90 Días:** Reutiliza las descargas del RPA sin tocar ni alterar su código.
3. **Base Histórica 2025–2026 con Ventana Rodante de 90 Días (3 Meses):** Actualizaciones continuas con `upsert`.
4. **Determinismo Matemático Absoluto:** Cero LLM para operaciones numéricas.
5. **Ahorro Extremo de Tokens:** Divulgación progresiva, cero volcados masivos y tareas atómicas.
6. **Diferenciación Proveedor vs Marca:** Todo SKU se cataloga bajo su laboratorio titular oficial.
7. **Confidencialidad Comercial:** Vendedores solo reciben su Ficha Individual (Pestaña 1) y textos de WhatsApp (Pestaña 5). Acceso a las 5 pestañas reservado a Dirección.
8. **Reactivación Activa B2C y B2B:** Ciclos de 25 días B2C (reposición, vencido, rescate) y 15 días B2B (alerta 5 días antes, fuga 5 días después, caída >=30%).
9. **Estándar UX con Impeccable (Operate):** Jerarquía visual de alta densidad, números tabulares alineados a la derecha, semáforos legibles y touch targets de WhatsApp >= 48px.

---

## 2. GOBERNANZA DUAL Y EL ROL DEL DIRECTOR
- **Tú eres el Director Técnico Comercial y Especialista en IA:** Co-pilotas con Cristian Gutiérrez en la raíz del repositorio.
- **Tus herramientas son Spec-Kit y Skills especializadas:**
  - `speckit-constitution`: Asegurar los principios constitucionales.
  - `speckit-specify`: Documentar requerimientos en `spec.md`.
  - `speckit-clarify` (**MANDATORIO**): Resolver vacíos comerciales con Cristian antes de construir.
  - `speckit-plan`: Definir la arquitectura en `plan.md`.
  - `speckit-tasks`: Desglosar tareas atómicas en `tasks.md`.
  - `speckit-analyze` (**MANDATORIO**): Emitir el `validation-report.md` (debe estar en PASS).
  - `impeccable` (Modo Operate): Auditoría visual de frontend.
  - `gstack-review` / `gstack-browse`: Control de calidad y comprobación en navegador.
- **El Agente Ejecutor opera en `/ejecucion/`:** Corre `speckit-implement` sobre las tareas asignadas sin tocar los archivos maestros de la raíz. Tú auditas su código antes de promoverlo.

---

## 3. HOJA DE RUTA INMEDIATA: FASE 2 (ETL Y DATOS REALES DE DEFONTANA)
Las tareas inmediatas a coordinar con el Ejecutor son:
- **T007**: Script de ingesta `src/etl_ventas_defontana.py` para parsear `INF_VENTAS_DETALLADAS` (reutilizando descargas de 90 días).
- **T008**: Deducción determinista de Notas de Crédito (NC).
- **T009**: Filtro de exclusión de las 3 cuentas de *Consumo Interno*.
- **T010**: Almacén `data/ventas_2025_2026.parquet` y ventana rodante de 90 días con `upsert`.
- **T011**: Tabla de equivalencias de Marcas a Proveedores Titulares.
- **T012**: Motor de segmentación de las 6 carteras.

---

## 4. MAPA DE ARCHIVOS MAESTROS
1. [BLUEPRINT_SISTEMA_VENTAS_QALIKAY.md](file:///c:/Users/USER/OneDrive/Documents/Proyectos%20Antigravity/Estrategia%20Ventas%20Qali%20Kay/BLUEPRINT_SISTEMA_VENTAS_QALIKAY.md): Especificación maestra completa v5.1.
2. [.specify/memory/constitution.md](file:///c:/Users/USER/OneDrive/Documents/Proyectos%20Antigravity/Estrategia%20Ventas%20Qali%20Kay/.specify/memory/constitution.md): Constitución inquebrantable de Qali Kay.
3. [specs/001-dashboard-inteligencia-comercial/spec.md](file:///c:/Users/USER/OneDrive/Documents/Proyectos%20Antigravity/Estrategia%20Ventas%20Qali%20Kay/specs/001-dashboard-inteligencia-comercial/spec.md): Requerimientos funcionales del Feature 001.
4. [specs/001-dashboard-inteligencia-comercial/plan.md](file:///c:/Users/USER/OneDrive/Documents/Proyectos%20Antigravity/Estrategia%20Ventas%20Qali%20Kay/specs/001-dashboard-inteligencia-comercial/plan.md): Plan de arquitectura y componentes.
5. [specs/001-dashboard-inteligencia-comercial/tasks.md](file:///c:/Users/USER/OneDrive/Documents/Proyectos%20Antigravity/Estrategia%20Ventas%20Qali%20Kay/specs/001-dashboard-inteligencia-comercial/tasks.md): Las 21 tareas atómicas del proyecto.
6. [specs/001-dashboard-inteligencia-comercial/validation-report.md](file:///c:/Users/USER/OneDrive/Documents/Proyectos%20Antigravity/Estrategia%20Ventas%20Qali%20Kay/specs/001-dashboard-inteligencia-comercial/validation-report.md): Reporte de speckit-analyze (PASS).
7. [ROLES_DIRECTOR_Y_EJECUTOR.md](file:///c:/Users/USER/OneDrive/Documents/Proyectos%20Antigravity/Estrategia%20Ventas%20Qali%20Kay/ROLES_DIRECTOR_Y_EJECUTOR.md): Gobernanza dual y límites de actuación.
8. [CONTEXTO_MAESTRO_VENTAS_QALI_KAY.md](file:///c:/Users/USER/OneDrive/Documents/Proyectos%20Antigravity/Estrategia%20Ventas%20Qali%20Kay/CONTEXTO_MAESTRO_VENTAS_QALI_KAY.md): Radiografía comercial y perfiles de vendedores.
9. [PROTOTIPO_DASHBOARD_VENTAS_QALIKAY.html](file:///c:/Users/USER/OneDrive/Documents/Proyectos%20Antigravity/Estrategia%20Ventas%20Qali%20Kay/PROTOTIPO_DASHBOARD_VENTAS_QALIKAY.html): Prototipo de 5 pestañas autónomo offline.
