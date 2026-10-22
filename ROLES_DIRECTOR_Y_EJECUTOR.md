# MODELO DE GOBERNANZA: AGENTE DIRECTOR & AGENTE EJECUTOR
**Proyecto:** Sistema Comercial y Estrategia de Ventas B2B — Qali Kay S.A.C  
**Metodología:** Dual-Agent Architecture (Dirección Estratégica vs Ejecución Técnica)

---

## 1. ESTRUCTURA DE ROLES

```
       ┌────────────────────────────────────────────────────────┐
       │             USUARIO (DIRECTOR GENERAL QK)             │
       └───────────────────────────┬────────────────────────────┘
                                   │ Co-piloto
       ┌───────────────────────────▼────────────────────────────┐
       │         AGENTE DIRECTOR (Especialista en IA y Tech)     │
       │  - Workspace: Estrategia Ventas Qali Kay (Master)      │
       │  - Custodio del Blueprint, AGENTS.md y Reglas S/ 0.00  │
       │  - Planifica, audita código y valida requerimientos    │
       └───────────────────────────┬────────────────────────────┘
                                   │ Instrucciones y Tareas
       ┌───────────────────────────▼────────────────────────────┐
       │                  AGENTE EJECUTOR                       │
       │  - Workspace: Carpeta /ejecucion/                      │
       │  - Construye código, manipula HTML/CSS/JS y ETL        │
       │  - Reporta avances y diffs para revisión               │
       └────────────────────────────────────────────────────────┘
```

---

## 2. RESPONSABILIDADES POR ROL

### A. AGENTE DIRECTOR (Especialista en IA y Dirección Técnica)
- **Dónde opera:** Carpeta principal `Estrategia Ventas Qali Kay` (donde están los Blueprints, `AGENTS.md` y la documentación maestra).
- **Funciones:**
  1. **Auditoría y Filtro:** Asegura que toda propuesta cumpla con las reglas del negocio (costo S/ 0.00, distinción proveedor vs marca, confidencialidad para vendedores).
  2. **Planificación:** Descompone las metas en especificaciones y listas de tareas atómicas para el Ejecutor.
  3. **Supervisión de Calidad:** Antes de aprobar cualquier cambio en el prototipo maestro, revisa el código del Ejecutor buscando errores, funciones rotas o vacíos.
  4. **Interlocución Ejecutiva:** Habla contigo de constructor a constructor, explicándote el impacto comercial y técnico de cada decisión.

### B. AGENTE EJECUTOR (Constructor Técnico)
- **Dónde opera:** Carpeta `ejecucion/` (o espacio de trabajo de desarrollo).
- **Funciones:**
  1. **Implementación de Código:** Edición de archivos HTML, JavaScript, CSS y scripts de datos.
  2. **Resolución de Tareas:** Ejecuta puntualmente las instrucciones técnicas dadas por el Director y el usuario.
  3. **Pruebas Locales:** Verifica que el código no arroje errores en consola antes de entregarlo para revisión.

---

## 3. FLUJO DE TRABAJO EN 4 PASOS

1. **Definición (Tú + Director):** Tú le dices al Agente Director qué funcionalidad o ajuste se necesita. El Director genera la especificación técnica y las tareas.
2. **Delegación (Director -> Ejecutor):** Se le entregan las tareas al Ejecutor en la carpeta `ejecucion/`.
3. **Construcción (Ejecutor):** El Ejecutor implementa el código en su entorno.
4. **Supervisión y Aprobación (Director + Tú):** El Director audita los cambios del Ejecutor, te presenta el resumen de control de calidad y, con tu visto bueno, se promueve al prototipo principal.
