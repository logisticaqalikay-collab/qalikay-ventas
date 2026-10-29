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
│  - Ingesta incremental de ventana rodante de 90 días (3 meses)         │
│  - Lectura directa de descargas existentes de abastecimiento           │
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

## 2. Pila Tecnológica y Suite de Herramientas IA Seleccionadas

| Componente | Tecnología / Herramienta | Justificación Técnica | Costo |
| :--- | :--- | :--- | :---: |
| **ETL & Data Processing** | Python 3.11 (`pandas`, `openpyxl`, `pyarrow`) | Determinismo matemático estricto, manipulación eficiente de Parquet e ingesta de Excel sin dependencias pagas ni alucinaciones de LLM. | S/ 0.00 |
| **Almacenamiento Histórico** | Parquet (`data/ventas_2025_2026.parquet`) | Formato columnar ultraliviano, compresión alta (>80%), consultas instantáneas en ventana de 90 días. | S/ 0.00 |
| **Data Contract / Interfaz** | JSON (`data/datos_comerciales.json`) | Desacopla el backend de datos del frontend; alimenta el dashboard tanto en local como en web. | S/ 0.00 |
| **Frontend UI / UX** | HTML5 semántico, CSS3 moderno con variables CSS | Cero dependencias por CDN; funciona 100% offline; renderiza en cualquier navegador (Chrome, Edge, Safari). | S/ 0.00 |
| **Gráficos y Visualización** | SVG nativo generado por JavaScript | Gráficos vectoriales nítidos y livianos sin librerías pesadas tipo Chart.js ni D3.js. | S/ 0.00 |
| **Metodología y Gobernanza** | Spec-Kit Suite (`constitution`, `specify`, `clarify`, `plan`, `tasks`, `analyze`, `implement`, `converge`) | Ciclo disciplinado de especificación antes de codificar, garantizando cero ambigüedades y control de calidad estricto. | S/ 0.00 |
| **Auditoría UX / UI** | Skill `impeccable` (Modo `Operate`) | Estándar visual de alta densidad: semáforos de alto contraste, números tabulares alineados a la derecha y touch targets móviles de WhatsApp (>= 48px). | S/ 0.00 |
| **Control de Calidad** | Skill `gstack` (`gstack-review`, `gstack-browse`) | Revisión de diffs, seguridad de código y comprobación en navegador sin errores de consola. | S/ 0.00 |
| **Despliegue / Hosting** | GitHub Pages / Vercel (Hobby) | Despliegue en la nube con HTTPS gratuito para acceso de directivos desde celulares o laptops. | S/ 0.00 |

---

## 3. Estrategia de Eficiencia y Ahorro Extremo de Tokens

1. **Divulgación Progresiva:** Nunca pasar archivos crudos de ventas (miles de filas) al contexto del modelo. El procesamiento se hace mediante scripts deterministas en Python. El LLM solo recibe resúmenes de esquema, diccionarios de datos o errores específicos.
2. **Desacoplamiento de Roles:** El Director define especificaciones en Markdown de alto nivel; el Ejecutor recibe tareas atómicas de `tasks.md` acotadas a un único archivo o función.
3. **Persistencia en Disco:** Toda decisión queda fijada en `specs/` y `BLUEPRINT`, eliminando conversaciones redundantes que quemen tokens en cada sesión.

---

## 4. Fases de Implementación Técnica

### Fase 1: Arquitectura y Prototipado Base (Completado ✅)
- Construcción de la Single Page Application con las 5 pestañas completas.
- Creación de los HUDs, selectores, matrices tabulares y gráficos SVG interactivos.
- Creación del generador de bandejas de WhatsApp limpias con botón de copiado.

### Fase 2: Pipeline ETL y Almacén Histórico 2025–2026 (En curso 🟡)
- Script Python para ingesta del reporte `INF_VENTAS_DETALLADAS` de Defontana (ventana de 90 días).
- Normalización de tipos de datos, deducción de Notas de Crédito y filtro de *Consumo Interno*.
- Implementación de la ventana rodante de 90 días sobre `data/ventas_2025_2026.parquet`.
- Maestro de artículos oficial de abastecimiento (`RAW_ARTICULOS`, 455 SKUs) para asignación determinista de SKU a Proveedor Titular.

### Fase 3: Motor de Reglas Comerciales y Carteras (En curso 🟡)
- Segmentación determinista de las 6 carteras:
  - Enrique (B2B campo).
  - Walter (s/ UNALM).
  - Cristian (s/ Organa; con Whitnin Tesen).
  - Carlos C (fusión con ex Joel).
  - Linda/Zully B2B (> S/ 400).
  - Linda/Zully B2C (<= S/ 400).
- Motor de alertas B2C (ciclos de 25 días, preventivas 25-35d, vencidas 36-60d, rescate >60d).
- Motor de Frecuencia B2B por madurez de compras:
  - Clientes Nuevos (1 a 3 compras históricas): Protocolo de onboarding a los 7 días (post-venta), 15 días (rotación inicial y promos) y 30 días (rescate/cierre).
  - Clientes Recurrentes (después de la 4ta compra registrada): Frecuencia dinámica individual ($N$), alerta preventiva $[N-3 \text{ a } N]$, alerta de fuga $N+5$ días y alerta de caída $\ge 30\%$.
- Motor de Recompra B2B Inteligente: Cruce de Canasta histórica de compras + Stock en almacén (`Kardex_Resumido`) + Lead Time del proveedor + Promociones vigentes de campaña (`promociones_vigentes.json`).
- Cruce con `CUENTAS POR COBRAR.xlsx` para alertas de cobranza y condición de pago.

### Fase 4: Enlace de Datos Reales al Dashboard (Frontend Binding)
- Sustitución del mock data en JavaScript por la lectura dinámica de `data/datos_comerciales.json`.
- Dropzone / botón de carga en el dashboard para que el usuario pueda arrastrar directamente el archivo de Defontana en el navegador (usando SheetJS embebido) si desea operar sin consola Python.

### Fase 5: Auditoría UX con Impeccable y Despliegue en la Nube (Completado ✅)
- Auditoría UX con skill `impeccable` en modo `Operate` (alto contraste, jerarquía visual ejecutiva, touch targets de WhatsApp > 48px en móvil).
- Despliegue en GitHub Pages o Vercel para enlace web directivo permanente.

### Fase 6: Refinamiento Ejecutivo de Reglas de Negocio v2 y Exportaciones Analíticas a Excel (Completado ✅)
- **Reclasificación Estricta Linda B2B vs B2C:** Evaluar exclusivamente si el comprobante (`Nro_Doc`, factura o boleta) supera `S/ 400.00` (eliminando el criterio por RUC 20 o suma por día).
- **Recomendación de 3 Productos por Cliente:** En el motor de recompra (`src/motor_reglas_carteras.py`) y en el generador de Bandejas de Salida de WhatsApp y Feed (`src/exportar_datos_dashboard.py`), garantizar 3 SKUs recomendados por cliente (Top 3 habituales + completado inteligente con SKUs líderes en stock cuando el cliente tiene $<3$ productos en su historial).
- **HUD de Clientes con Deuda Vencida (53 clientes · S/ 162,464.07) + Tabla y Exportación Excel:** Contabilizar exclusivamente clientes con deuda vencida real en `Cuentas por cobrar 2026.xlsx`, desplegar tabla consolidada al hacer clic y permitir descarga en `.xlsx` vía SheetJS (`XLSX.writeFile`), además de un botón de descarga `.xlsx` del detalle de deuda vencida dentro de la Ficha Individual de cada vendedor.
- **Ventana Operativa de 90 Días en el Feed para Linda B2C + Descarga de Histórico Total:** Mostrar en el Feed de Acciones Operativas únicamente los clientes de los últimos 90 días de Linda B2C que requieran acción, y habilitar un botón de exportación `.xlsx` con el análisis completo de los `877` clientes históricos de Linda B2C de todo el tiempo.
- **Evolución de 6 Meses 2026 + Promedio Activo 2025, Proveedores del Maestro y Responsive Móvil:** Consolidado en `src/exportar_datos_dashboard.py` y `ejecucion/PROTOTIPO_DASHBOARD_VENTAS_QALIKAY.html`.

### Fase 7: Sincronización Total, Cero Alucinaciones y Reglas Avanzadas de Negocio (En Curso 🟡)
- **Aislamiento Multi-Ruta de Cuentas por Cobrar:** Soporte dinámico para rutas de OneDrive en PC cguti y PC USER (`C:\Users\USER\OneDrive\CUENTAS POR COBRAR\QALI KAY\2026\Cuentas por cobrar 2026.xlsx`).
- **Ingesta XLSX de Google Sheets:** Descarga `/export?format=xlsx` de `RAW_VENTAS` en `etl_ventas_defontana.py` preservando códigos alfanuméricos (`MERMULTCENT`, `MERSAMARI`, etc.) y recuperando decimales corrompidos a fecha (`float(f"{dt.day}.{dt.month:02d}")`).
- **Exclusión de Facturas Gratuitas:** Descarte de documentos `01 Factura Electrónica Gratuita Sin IGV` en cálculo de ventas comerciales.
- **Detección de Discrepancias CxC vs Defontana:** Identificación de documentos activos en CxC pero anulados/inexistentes en Defontana (ej. `F001-6208`).
- **Regla Documentos A Cuenta Vencidos:** Todo documento con `Estado == "VENCIDA"` o (`Estado == "A CUENTA"` con `Días vencidos > 0` y `Saldo > 0.50`) suma a deuda y conteo de documentos vencidos.
- **Asignación Soberana de PITRU S.A.C.:** RUC `20501997545` fijado a la cartera de Carlos Cuadros (`carlos-cuadros`).
- **Eliminación Total de Alucinaciones en Canasta:** Supresión de `FALLBACK_STAR_SKUS`. Solo se muestran SKUs que el cliente realmente compró.
- **Redacción Desacoplada de Promociones:** Desvincular canasta del cliente de promociones de campaña. Nombrar explícitamente el SKU en bonificación 12+1 o 6+1 (solo B2B).
- **Promoción Estandarizada B2C:** *"20% de descuento en la 2da unidad de tu próxima compra"* para clientes inactivos de Linda B2C.
- **Modal de 9 Campañas en HUD:** Modal interactivo para inspeccionar catálogo completo de promociones vigentes.
- **Filtro y Archivo Inactivos > 120 Días con Reincorporación Manual:** Segregación de inactivos $> 120$d y botón interactivo UI para retornar a acciones diarias.
- **Exclusión de Colaboradores:** Normalización de DNIs con/sin cero inicial y exclusión de Enrique, Junnior, Kelly y Norexglis.
