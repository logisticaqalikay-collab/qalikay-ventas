# Feature Plan: 001 - Sistema de Inteligencia Comercial y Dashboard de Ventas B2B/B2C

**Código:** `QK-VENTAS-001`  
**Área:** Arquitectura de Software e Ingeniería de Datos  
**Metodología:** Spec-Kit (`plan` ➔ `tasks` ➔ `analyze` ➔ `implement`)  
**Presupuesto:** S/ 0.00 ($0.00 USD)

---

## 1. Arquitectura del Sistema (3 Capas Desacopladas)

```
┌────────────────────────────────────────────────────────────────────────┐
│                        CAPA 1: INGESTA & ETL                           │
│  - Parser de reportes Defontana ('INF_VENTAS_DETALLADAS' .xlsx / .csv) │
│  - Ingesta incremental de ventana rodante de 60 días                   │
│  - Deducción determinista de Notas de Crédito                          │
│  - Mapeo de Carteras (6 segmentos) y Maestro de Proveedores vs Marcas │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│               CAPA 2: ALMACENAMIENTO & MOTOR ANALÍTICO                 │
│  - Almacén consolidado: data/ventas_2025_2026.parquet                  │
│  - Motor de agregación: DuckDB / Python pandas determinista            │
│  - Exportación de snapshot liviano: data/datos_comerciales.json        │
│  - Cruce con cuentas por cobrar: data/cuentas_por_cobrar.json          │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   CAPA 3: DASHBOARD & PRESENTACIÓN                     │
│  - Frontend SPA: PROTOTIPO_DASHBOARD_VENTAS_QALIKAY.html               │
│  - Arquitectura autónoma Offline-first (Cero CDNs externas)            │
│  - Renderizado SVG dinámico (Barras, curvas multi-período)             │
│  - Módulo WhatsApp con codificación de texto limpia y copy en 1 clic   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Pila Tecnológica y Decisiones de Diseño

| Componente | Tecnología Seleccionada | Justificación Técnica | Costo |
| :--- | :--- | :--- | :---: |
| **ETL & Data Processing** | Python 3.11 (`pandas`, `openpyxl`, `pyarrow`) | Determinismo matemático estricto, manipulación eficiente de Parquet e ingesta de Excel sin dependencias pagas. | S/ 0.00 |
| **Almacenamiento Histórico** | Parquet (`data/ventas_2025_2026.parquet`) | Formato columnar ultraliviano, compresión alta (>80%), consultas instantáneas por ventana de tiempo. | S/ 0.00 |
| **Data Contract / Interfaz** | JSON (`data/datos_comerciales.json`) | Desacopla el backend de datos del frontend; permite alimentar el dashboard tanto en local como en web. | S/ 0.00 |
| **Frontend UI / UX** | HTML5 semántico, CSS3 moderno con variables CSS | Cero dependencias por CDN; funciona 100% offline; renderiza en cualquier navegador (Chrome, Edge, Safari). | S/ 0.00 |
| **Gráficos y Visualización** | SVG nativo generado por JavaScript | Gráficos vectoriales nítidos y livianos sin librerías pesadas tipo Chart.js ni D3.js. | S/ 0.00 |
| **Despliegue / Hosting** | GitHub Pages / Vercel (Hobby) | Despliegue en la nube con HTTPS gratuito para acceso de directivos desde celulares o laptops. | S/ 0.00 |

---

## 3. Estructura de Directorios del Proyecto

```
📁 Estrategia Ventas Qali Kay/
│   ├── AGENTS.md                                   <-- Reglas del Director y del Negocio QK
│   ├── BLUEPRINT_SISTEMA_VENTAS_QALIKAY.md          <-- Master Blueprint v5.0
│   ├── CONTEXTO_MAESTRO_VENTAS_QALI_KAY.md         <-- Glosario comercial y carteras
│   ├── ROLES_DIRECTOR_Y_EJECUTOR.md                <-- Modelo de Gobernanza Dual
│   ├── PACK_REANUDACION_SESION_QALIKAY.md          <-- Resumen ejecutivo de traspaso
│   ├── PROTOTIPO_DASHBOARD_VENTAS_QALIKAY.html     <-- Dashboard en producción/raíz
│   │
│   ├── 📁 .specify/                                <-- Infraestructura Spec-Kit
│   │   ├── memory/constitution.md                  <-- Constitución de Ventas (7 principios)
│   │   ├── templates/                              <-- Plantillas de spec, plan, tasks
│   │   └── feature.json                            <-- Puntero a la feature activa
│   │
│   ├── 📁 specs/001-dashboard-inteligencia-comercial/
│   │   ├── spec.md                                 <-- Especificación de requerimientos
│   │   ├── plan.md                                 <-- Este plan de arquitectura
│   │   ├── tasks.md                                <-- Tareas atómicas ordenadas
│   │   └── validation-report.md                    <-- Reporte de speckit-analyze (PASS)
│   │
│   ├── 📁 src/                                     <-- Scripts y pipelines (Backend ETL)
│   │   ├── etl_ventas_defontana.py                 <-- Ingesta de INF_VENTAS_DETALLADAS
│   │   ├── ventana_rodante_60d.py                  <-- Upsert de comprobantes y NC
│   │   └── exportar_datos_dashboard.py             <-- Generador de datos_comerciales.json
│   │
│   ├── 📁 data/                                    <-- Repositorio de datos
│   │   ├── ventas_2025_2026.parquet                <-- Base histórica consolidada
│   │   └── datos_comerciales.json                  <-- Snapshot reactivo para el dashboard
│   │
│   └── 📁 ejecucion/                               <-- Espacio de trabajo del Agente Ejecutor
│       ├── AGENTS.md                               <-- Reglas técnicas para el programador
│       └── PROTOTIPO_DASHBOARD_VENTAS_QALIKAY.html <-- Taller de desarrollo
```

---

## 4. Fases de Implementación Técnica

### Fase 1: Arquitectura y Prototipado Base (Completado ✅)
- Construcción de la Single Page Application con las 5 pestañas completas.
- Creación de los HUDs, selectores, matrices tabulares y gráficos SVG interactivos.
- Creación del generador de bandejas de WhatsApp limpias con botón de copiado.

### Fase 2: Pipeline ETL y Almacén Histórico 2025–2026 (En curso 🟡)
- Script Python para ingesta del reporte `INF_VENTAS_DETALLADAS` de Defontana.
- Normalización de tipos de datos, descuento de Notas de Crédito y filtro de *Consumo Interno*.
- Implementación de la ventana rodante de 60 días sobre `data/ventas_2025_2026.parquet`.
- Maestro de mapeo de marcas hacia proveedores titulares (ej. *D'Nattive* al laboratorio titular).

### Fase 3: Motor de Reglas Comerciales y Carteras (En curso 🟡)
- Segmentación determinista de las 6 carteras:
  - Enrique (B2B campo).
  - Walter (s/ UNALM).
  - Cristian (s/ Organa; con Whitnin Tesen).
  - Carlos C (fusión con ex Joel).
  - Linda/Zully B2B (> S/ 400).
  - Linda/Zully B2C (<= S/ 400).
- Motor de alertas B2C (ciclos de 25 días, preventivas 25-35d, vencidas 36-60d, rescate >60d).
- Motor de alertas B2B (15 días de reposición, preventivas a los 10d, fuga a los 20d, caída >=30%).
- Cruce con `CUENTAS POR COBRAR.xlsx` para alertas de cobranza.

### Fase 4: Enlace de Datos Reales al Dashboard (Frontend Binding)
- Sustitución del mock data en JavaScript por la lectura dinámica de `data/datos_comerciales.json`.
- Dropzone / botón de carga en el dashboard para que el usuario pueda arrastrar directamente el archivo de Defontana en el navegador (usando SheetJS embebido) si desea operar sin consola Python.

### Fase 5: Auditoría UX con Impeccable y Despliegue en la Nube
- Auditoría UX con skill `impeccable` en modo `Operate` (alto contraste, jerarquía visual ejecutiva, touch targets de WhatsApp > 48px en móvil).
- Despliegue en GitHub Pages o Vercel para enlace web directivo permanente.
