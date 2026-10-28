# REPORTE DE AUDITORÍA DE PREFLIGHT - FASE 3
## Ambigüedades, Casos Borde y Gobernanza de Reglas Comerciales (Tareas T012 a T016)

**Código de Tarea:** `QK-VENTAS-AUDIT-FASE3`  
**Alcance:** Tareas T012, T013, T014, T014b, T015 y T016 (Motor de Carteras, Frecuencia B2B, Ciclo B2C, Recompra Inteligente y Cobranza)  
**Fecha de Ejecución:** 28 de Octubre de 2026  
**Auditor Responsable:** Agente Ejecutor y Desarrollador de Software  
**Supervisión Directiva:** Director General (Cristian Gutiérrez) & Director Técnico Comercial  
**Base Auditada:** `data/ventas_2025_2026.parquet` (37,711 transacciones comerciales netas consolidadas en Fase 2)

---

## 1. DICTAMEN EJECUTIVO

### **DICTAMEN: APTO CON DECISIONES DE GOBERNANZA PENDIENTES (LISTO TRAS LAUDO DIRECTIVO)**

La auditoría empírica sobre los datos consolidados en Parquet y los archivos del repositorio ha identificado **6 decisiones clave de arquitectura y gobernanza comercial** que deben ser zanjadas formalmente por el Director General antes de escribir el motor de reglas en código.

| Área Auditada | Estado | Hallazgo Técnico Principal |
| :--- | :---: | :--- |
| **Segmentación de Carteras (T012)** | 🟡 **Decisión** | Se identificó que `Rep. Comercial` (3,561 filas) y `Zully Rios` (32 filas) absorben todo el canal inbound/oficina. Se detectaron 14 clientes híbridos con comprobantes `> S/ 400` y `<= S/ 400`. |
| **Whitnin Tesen (T012)** | 🟢 **Resuelto** | Aparece con DNI `48517168` bajo Cristian (29 filas) y con RUC `10485171687` bajo Rep. Comercial (7 filas). Ambos se unifican 100% en Cristian Gutiérrez (S/ 5,606.81). |
| **Ex-Vendedores 2025 (T012)** | 🟢 **Resuelto** | Miguel Ángel Sega y Oswaldo Meléndez solo vendieron a franquicias de Organa en 2025. Alejandra Chávez (5 clientes) migró activamente en 2026 a Carlos Cuadros y Enrique García. |
| **Frecuencia B2B (T014)** | 🟢 **Blindado** | Existen 434 casos de comprobantes múltiples el mismo día. La "Compra" DEBE definirse como **Día Único de Facturación Neta Positiva**, evitando que 42 clientes distorsionen su mediana $N$ con intervalos de 0 días. |
| **Stock Kardex (T014b)** | 🟢 **Excelente** | `Kardex_Resumido_20261002.xlsx` cubre el **92.3% de los SKUs** y el **99.1% de la venta histórica** (S/ 3.26M). Viabilidad total para motor de recompra. |
| **Archivos Faltantes (T015/T014b)** | 🟡 **Requiere Acción** | `CUENTAS POR COBRAR.xlsx` y `promociones_vigentes.json` no existen en disco. Se proponen contratos de datos deterministas y semillas iniciales. |

---

## 2. RADIOGRAFÍA DE AMBIGÜEDADES EN SEGMENTACIÓN DE CARTERAS (T012)

### 2.1 Mapeo de Vendedores en Defontana y Canal Inbound / Oficina
En las 37,711 filas comerciales de `data/ventas_2025_2026.parquet`, los vendedores registrados en el ERP se distribuyen así:

```
┌───────────────────────────────────┬─────────────┬─────────────┬─────────────────┬──────────┐
│ Nombre_Vendedor en Defontana      │ Transac.    │ Unidades    │ Venta Neta S/   │ Clientes │
├───────────────────────────────────┼─────────────┼─────────────┼─────────────────┼──────────┤
│ Cristian Gutierrez                │      20,203 │     104,038 │ S/ 2,101,338.81 │       98 │
│ Walter Gutiérrez                  │       8,323 │      39,002 │ S/   589,977.41 │       49 │
│ ENRIQUE GARCIA VALDERA            │       4,373 │      24,948 │ S/   270,326.98 │      235 │
│ Rep. Comercial                    │       3,561 │       8,923 │ S/   249,363.06 │      919 │
│ JOEL GARCIA ZEVALLOS (Histórico)  │         904 │       4,699 │ S/    53,948.98 │       41 │
│ CUADROS VALERIANO CARLOS ALBERTO  │         235 │         919 │ S/    14,422.85 │       21 │
│ Alejandra Chávez (Ex-vendedora)   │          32 │         230 │ S/     2,760.72 │        5 │
│ MIGUEL ANGEL SEGA ZAMBRANO (Ex)   │          29 │         175 │ S/     3,553.75 │        2 │
│ OSWALDO JEFFERSON MELENDEZ (Ex)   │          19 │          76 │ S/     1,451.26 │        1 │
│ Zully Rios                        │          32 │          54 │ S/       857.47 │        4 │
├───────────────────────────────────┼─────────────┼─────────────┼─────────────────┼──────────┤
│ TOTAL CONSOLIDADO                 │      37,711 │     183,064 │ S/ 3,288,001.29 │    1,310 │
└───────────────────────────────────┴─────────────┴─────────────┴─────────────────┴──────────┘
```

#### Hallazgos y Aclaraciones:
1. **Inexistencia de etiqueta "Linda Ríos" en ventas:** En el ERP no existe ningún registro etiquetado como `Linda Ríos`. Las ventas del canal inbound web/redes y oficina se facturaron bajo `Rep. Comercial` (3,561 filas) y marginalmente bajo `Zully Rios` (32 filas).
2. **Absorción Joel García $\to$ Carlos Cuadros:**
   - Joel García cerró 904 transacciones (62 en 2025 y 842 en 2026, S/ 53,948.98).
   - Carlos Cuadros ingresó en 2026 con 235 transacciones (S/ 14,422.85).
   - **Regla Unificada:** Para la cartera de Carlos Cuadros, se absorbe el 100% del historial de Joel García, consolidando **1,139 transacciones y S/ 68,371.83**.
3. **Destino de los Ex-Vendedores de 2025 (80 transacciones):**
   - *Miguel Ángel Sega* (29 filas) y *Oswaldo Meléndez* (19 filas): Atendieron exclusivamente a sucursales de Organa (`ORGANA PERU S.A.C.` y `HOLDING E INVERSIONES CHYP`). Al ser Organa una cuenta institucional de Cristian, quedan absorbidas en el historial de Organa.
   - *Alejandra Chávez* (32 filas, 5 clientes):
     - `ORTIZ CCANTO CELIA` (`10413975102`): En 2026 fue atendida por **Carlos Cuadros** (7 pedidos, S/ 396.62).
     - `COMERCIAL KALLPA S.A.C.` (`20602396364`): En 2026 fue atendida por **Enrique García** (97 pedidos, S/ 2,597.38).
     - Los otros 3 clientes no volvieron a comprar en 2026.

---

### 2.2 Bifurcación Linda / Zully (> S/ 400 vs <= S/ 400) y el Caso de los Clientes Híbridos
Se agrupó el canal inbound (`Rep. Comercial` + `Zully Rios`, total 3,593 filas) por comprobante fiscal (`Nro_Doc`) para cuantificar el umbral de S/ 400.00:

```
┌─────────────────────────────────┬────────────────┬─────────────────┬──────────────────┐
│ Segmento Comprobante            │ Comprobantes   │ Monto Total S/  │ Clientes Únicos  │
├─────────────────────────────────┼────────────────┼─────────────────┼──────────────────┤
│ Comprobantes B2B (> S/ 400.00)  │            144 │ S/   122,842.08 │               44 │
│ Comprobantes B2C (<= S/ 400.00) │          1,421 │ S/   127,378.45 │              893 │
├─────────────────────────────────┼────────────────┼─────────────────┼──────────────────┤
│ TOTAL CANAL INBOUND             │          1,565 │ S/   250,220.53 │              923 │
└─────────────────────────────────┴────────────────┴─────────────────┴──────────────────┘
```

#### El Problema de los 14 Clientes Híbridos:
Se detectaron **14 clientes** que tienen pedidos tanto mayores a S/ 400 como menores o iguales a S/ 400:
- `CASAFIT S.A.C.` (RUC 20612927406): 5 pedidos (S/ 1,474.07, S/ 529.70, S/ 323.56, S/ 129.30).
- `NOLA PASTELERIA SALUDABLE S.A.C.` (RUC 20614663856): 12 pedidos (desde compras de S/ 607.05 hasta reposiciones de S/ 64.45 y S/ 249.31).
- `Ecotienda Ecokanpu` (RUC 10702858785): 5 pedidos (S/ 783.01, S/ 684.33, S/ 77.97).

> [!IMPORTANT]
> **Decisión Requerida #1 (Bifurcación Transaccional vs Cliente):**  
> - **Nivel Transaccional (HUDs de Venta y Fichas):** Cada comprobante se asigna a *Linda/Zully B2B* (> 400) o *Linda/Zully B2C* (<= 400). Esto cuadra los números al centavo.  
> - **Nivel Alertas Operativas (Pestaña 4 y 5):** ¿Bajo qué motor se alerta a los clientes híbridos?  
>   - **Recomendación Técnica:** Si el cliente tiene **RUC de empresa (RUC 20)** o ha emitido al menos un pedido > S/ 400.00 en su historial, debe tratarse como **Cliente B2B** (Motor T014), ya que sus compras pequeñas son reposiciones de stock comercial y no consumo personal.

---

### 2.3 Tratamiento de Whitnin Tesen (Piura)
- En el análisis empírico se descubrió que Whitnin Scarlet Tesen Chang tiene dos identidades en Defontana:
  1. Con Boleta de Venta: **DNI `48517168`** bajo el vendedor `Cristian Gutierrez` (29 transacciones: 20 en 2025 y 9 en 2026, total S/ 4,562.95).
  2. Con Factura comercial: **RUC `10485171687`** (`TESEN CHANG WHITNIN SCARLET`) bajo el vendedor `Rep. Comercial` (7 transacciones en abril y mayo de 2025, total S/ 1,043.86).
- **Resolución:** Ambos códigos de cliente (`48517168` y `10485171687`) representan a la misma cliente estratégica de Piura y deben asignarse **100% a la cartera de Cristian Gutiérrez**, sumando exactamente **36 transacciones y S/ 5,606.81**.

---

### 2.4 Cuentas Excluidas (Organa y UNALM) en Vistas Globales vs Individuales
Se cuantificó el impacto exacto de las exclusiones:
- **Organa (14,058 filas, S/ 1,578,701.69):** Representa el 48.0% de las ventas de la compañía.
- **UNALM / Fundeagro (1,357 filas, S/ 68,850.98):** Representa el 2.1% de las ventas de la compañía.

```
┌───────────────────────────────────────┬─────────────────────────┬─────────────────────────┐
│ Alcance de Visualización              │ Venta con Exclusiones   │ Venta Neta Real Total   │
├───────────────────────────────────────┼─────────────────────────┼─────────────────────────┤
│ Walter Gutiérrez (Ficha Individual)   │ S/ 521,126.43 (s/ UNALM)│ S/ 589,977.41           │
│ Cristian Gutiérrez (Ficha Individual) │ S/ 527,184.80 (s/Organa)│ S/ 2,101,338.81         │
│ Pestaña 2 (Proveedores y Mix SKUs)    │ S/ 3,288,001.29 (100%)  │ S/ 3,288,001.29 (100%)  │
│ Pestaña 3 (Histórico Global Empresa)  │ S/ 3,288,001.29 (100%)  │ S/ 3,288,001.29 (100%)  │
└───────────────────────────────────────┴─────────────────────────┴─────────────────────────┘
```

> [!TIP]
> **Recomendación Técnica de Visualización:**  
> - En **Pestaña 1 (Vendedores):** Aplicar la exclusión estricta a Walter y Cristian para medir con justicia su gestión comercial ordinaria frente al resto del equipo.  
> - En **Pestaña 2 (Proveedores) y Pestaña 3 (Global Empresa):** **INCLUIR Organa y UNALM al 100%**. Si se excluyeran de la Pestaña 2 o 3, la facturación global de la empresa caería ficticiamente a la mitad (S/ 1.64M en lugar de S/ 3.29M) y los TOP SKUs de proveedores líderes como Nutrivas o Pecaditos quedarían completamente ciegos.

---

### 2.5 Clientes Atendidos por Múltiples Vendedores
- De los 1,310 clientes de la base, **1,259 clientes (96.1%)** siempre fueron atendidos por el mismo vendedor.
- Solo **51 clientes (3.9%)** tienen comprobantes con más de un vendedor en el histórico.
- **Transiciones detectadas:**
  - 14 clientes pasaron de Cristian Gutiérrez a Enrique García (delegación de cuentas a campo).
  - 8 clientes pasaron de Joel García a Carlos Cuadros (traspaso formal de cartera).
  - 3 clientes pasaron de Cristian a Carlos Cuadros.

> [!IMPORTANT]
> **Decisión Requerida #2 (Asignación de Cartera para Alertas):**  
> Para saber a qué vendedor le debe aparecer la alerta de recompra o fuga de un cliente en Pestaña 4 y 5:  
> - **Regla Recomendada:** Asignar al **Último Vendedor que le facturó con venta neta positiva**, aplicando las reglas de override fijadas:  
>   1. Si el último vendedor fue Joel García $\to$ la alerta va a **Carlos Cuadros**.  
>   2. Si el cliente es Whitnin Tesen $\to$ la alerta va a **Cristian Gutiérrez**.  
>   3. Si el último comprobante fue de Rep. Comercial $\to$ la alerta va a **Linda/Zully**.

---

## 3. AUDITORÍA MATEMÁTICA DE FRECUENCIA B2B Y CICLO B2C (T013 Y T014)

### 3.1 El Fenómeno de Facturas Múltiples en el Mismo Día y la Distorsión de $N$
Se descubrió que en **434 ocasiones**, un cliente recibió 2 o más facturas en la misma fecha (llegando hasta 17 comprobantes en un solo día para grandes clientes que piden por sucursal).

- **Efecto Matemático Crítico:**  
  Si el cálculo de días entre compras se hace a nivel de comprobante (`Nro_Doc`), aparecen intervalos artificiales de **`0 días`**.
  - En **42 de los 186 clientes recurrentes (22.6%)**, la mediana de recompra $N$ se deforma hacia abajo.
  - *Caso Real Auditado:* Cliente `07655960`:  
    - Con cálculo por documento: $N = 34.0\text{ días}$.  
    - Con cálculo por fecha única: $N = 41.0\text{ días}$.  
    - **Consecuencia de Negocio:** La alerta de recompra se dispararía una semana antes de tiempo, generando llamadas inoportunas del vendedor cuando la farmacia aún tiene stock en anaquel.

> [!CAUTION]
> **Regla Determinista Mandatoria para T014:**  
> Una "Compra" se define estrictamente como un **Día Único de Facturación con Venta Neta Positiva**:  
> $$\text{Compra Válida} = \left( \text{Cod\_Cliente, Fecha} \right) \quad \text{donde} \quad \sum_{\text{día}} \text{Total\_Detalle} > 0$$  
> Se descartan del conteo los días cuya venta neta sea $\le 0$ (días de anulación o devolución neta).

---

### 3.2 Análisis Empírico de Notas de Crédito: Anulación Total vs Parcial
Sobre los 424 comprobantes únicos de Notas de Crédito en el histórico:
- **98 Notas de Crédito (23.1%):** Fueron anulaciones totales exactas (100% del monto de una factura previa).
- **326 Notas de Crédito (76.9%):** Fueron devoluciones parciales de mercadería o descuentos comerciales por pronto pago/bonificación.
- **Validación del Algoritmo:** Al agrupar por `(Cod_Cliente, Fecha)`, las anulaciones totales quedan neutralizadas automáticamente ($\text{Monto Neto} = 0$), excluyendo la fecha del historial de compras válidas sin requerir lógica heurística compleja.

---

### 3.3 Distribución de Madurez de Cartera y Fecha de Anclaje
Sobre los 1,306 clientes con compras válidas:
- **Clientes Nuevos (1 a 3 compras históricas):** **1,120 clientes (85.8%)**  
  - 1 sola compra: 888 clientes (68.0%)  
  - 2 compras: 161 clientes (12.3%)  
  - 3 compras: 71 clientes (5.4%)  
  $\to$ **Aplican al Protocolo de Onboarding T014 (Día 7, 15 y 30).**
- **Clientes Recurrentes ($\ge 4$ compras históricas):** **186 clientes (14.2%)**  
  - Mediana global de recompra ($N$): **34.5 días**.  
  - Rango intercuartílico: P25 = 22.1 días, P75 = 57.0 días.  
  $\to$ **Aplican al Motor de Frecuencia Dinámica Individual $N_{cliente}$ (Alerta preventiva $[N-3, N]$ y fuga $N+5$).**

- **Fecha de Anclaje (`Fecha_Referencia`):**  
  La fecha máxima registrada en el dataset es el **`24/10/2026`**.  
  Para que los cálculos de pruebas y los snapshots sean deterministas y 100% reproducibles, el motor de alertas tomará como fecha base por defecto `Fecha_Referencia = max(df['Fecha'])`, permitiendo pasar la fecha actual del sistema si se opera en tiempo real.

---

## 4. AUDITORÍA DE ARCHIVOS COMPLEMENTARIOS EN DISCO (T014b, T015, T016)

### 4.1 `Kardex_Resumido_20261002.xlsx` (T014b - Motor de Recompra Inteligente)
- Archivo auditado: `../qalikay-abastecimiento/descargas_erp/Kardex_Resumido_20261002.xlsx`.
- Contenido: 634 SKUs con stock disponible en Almacén Central y costo unitario.
- **Resultado del Cruce con Ventas:**  
  - **549 de los 595 SKUs vendidos históricamente (92.3%)** hacen match exacto con el Kardex.  
  - Los SKUs cruzados representan el **99.1% de la facturación histórica** (S/ 3.26M) y el **98.9% del volumen físico**.
- **Lógica de Alerta:**
  - Si `Saldo_Almacen > 0` $\to$ Mensaje en WhatsApp: *"Stock disponible en almacén Qali Kay: despacho en 24 a 48 horas"*.
  - Si `Saldo_Almacen <= 0` $\to$ Activa el Lead Time oficial del Proveedor Titular (`T016`).

---

### 4.2 `CUENTAS POR COBRAR.xlsx` (T015 - Control de Créditos y Cobranza)
- **Diagnóstico:** El archivo `CUENTAS POR COBRAR.xlsx` **NO existe actualmente en `data/`**.
- **Datos Disponibles en Parquet:**  
  El Parquet consolidado contiene para el 100% de las transacciones:  
  - `Cond_Pago` (01.CONTADO, 03.CREDITO30DIAS, 02.CREDITO15DIAS, etc.)  
  - `Fecha_Vencimiento` (fecha límite de pago según plazo comercial).
- **Lo que falta:** Saber si una factura a crédito emitida hace 45 días ya fue cobrada en banco o sigue pendiente/impaga.

> [!IMPORTANT]
> **Decisión Requerida #3 (Contrato de Cuentas por Cobrar):**  
> Para T015, se propone que el sistema soporte:  
> 1. Ingesta opcional de `data/cuentas_por_cobrar.xlsx` (o `.json`) si Defontana exporta la lista de documentos impagos con columnas `[Nro_Doc, Cod_Cliente, Saldo_Pendiente, Dias_Mora]`.  
> 2. Si el archivo no está presente, el sistema calculará un indicador preventivo basado en facturas con condición crédito cuya `Fecha_Vencimiento < Fecha_Referencia`, emitiendo una alerta condicional: *"Verificar cobranza previa: Factura vencida el YYYY-MM-DD"*.

---

### 4.3 `promociones_vigentes.json` (T014b - Asistente de Promociones)
- **Diagnóstico:** No existe actualmente en `data/`.
- **Propuesta:** Generar el archivo semilla `data/promociones_vigentes.json` extrayendo las reglas ya aprobadas en el prototipo y especificaciones:
  - `NUTRIVAS (Nanita)`: Promoción activa `6+1` en Aceite de Calabaza (`NAN-079`), Selenium Quelado (`NAN-081`) y Colágeno Multipéptidos (`NAN-073`). Promoción `12+1` en NAD+ Resveratrol (`NAN-036`).
  - `MOLINOS DEL MUNDO`: Descuento por compra en caja completa (Pastas y Panes).
  - `FIBRA FRUT / VIVAFRUT`: Pack mixto 6 unidades para puntos nuevos.
  - `QORINKA`: Precio mayorista a partir de display x 12.
  - `AMAZON ANDES`: Bonificación por volumen en Maca y Aguaje.

---

### 4.4 Matriz Oficial de Lead Times por Proveedor (T016)
Se ratifica la tabla de parámetros definida en `spec.md` (FR-09):

```
┌───────────────────────────┬───────────────────┬────────────────────────────────────────────────────────┐
│ Clasificación Lead Time   │ Proveedor Titular │ Plazo de Entrega y Regla Logística                     │
├───────────────────────────┼───────────────────┼────────────────────────────────────────────────────────┤
│ Rápidos (1 a 2 días)      │ NUTRIVAS          │ 24 a 48h con stock. Si stock = 0: 4 a 5 días con Compras│
│ Rápidos (1 a 2 días)      │ AMAZON ANDES      │ 24 a 48h con stock.                                    │
│ Rápidos (1 a 2 días)      │ TAURI             │ 24 a 48h con stock.                                    │
│ Rápidos (1 a 2 días)      │ OLIVO DE ORO      │ 24 a 48h con stock.                                    │
│ Rápidos (1 a 2 días)      │ DEPURATÉ          │ 24 a 48h con stock.                                    │
│ Rápidos (1 a 2 días)      │ INKA COMEX        │ 24 a 48h con stock.                                    │
│ Rápidos (1 a 2 días)      │ ANDES CRISP       │ 24 a 48h con stock.                                    │
│ Entrega Semanal Fija      │ MOLINOS DEL MUNDO │ Entregas exclusivas los Miércoles.                      │
│ Mayor Demora              │ QORINKA           │ Plazo de reposición: 4 días hábiles.                   │
│ Mayor Demora              │ PECADITOS INTEGRAL│ Plazo de reposición: 1 semana.                         │
│ Mayor Demora              │ FIBRA FRUT        │ Plazo de reposición: 1 semana (MOQ: 12 unidades).      │
│ Mayor Demora              │ FUNGI AMAZONICA   │ Despacho programado quincenal.                         │
│ En Liquidación            │ NOA LIFE          │ Vender hasta agotar existencias en almacén.            │
│ En Liquidación            │ INKA PRIME        │ Vender hasta agotar existencias en almacén.            │
│ En Liquidación            │ QORI (Ayacucho)   │ Vender hasta agotar existencias en almacén.            │
└───────────────────────────┴───────────────────┴────────────────────────────────────────────────────────┘
```

---

## 5. CATÁLOGO DE DECISIONES REQUERIDAS DE LA DIRECCIÓN GENERAL

Para proceder con la codificación de la Fase 3, solicitamos al Director General (Cristian Gutiérrez) la ratificación o laudo sobre los siguientes 6 puntos:

| # | Punto de Decisión | Opción Recomendada (Técnica) | Opción Alternativa | Impacto Técnico / Operativo |
| :-: | :--- | :--- | :--- | :--- |
| **D1** | **Bifurcación Linda/Zully en Clientes Híbridos (14 clientes)** | Si el cliente tiene RUC 20 o al menos 1 compra > S/ 400, asignarlo al **Motor B2B (T014)**. | Asignarlo al motor B2C o evaluar cada alerta según el monto de su último pedido. | Evita tratar a pastelerías o ecotiendas como si fueran personas naturales consumiendo un frasco. |
| **D2** | **Atribución de Cartera para Alertas en Clientes Multi-vendedor** | Asignar al **Último Vendedor que facturó venta positiva**, con override (Joel $\to$ Carlos Cuadros; Whitnin $\to$ Cristian). | Asignar al vendedor histórico que acumuló mayor facturación con el cliente. | Refleja quién tiene la relación comercial viva hoy con la cuenta. |
| **D3** | **Visualización de Organa y UNALM en Pestañas 2 y 3** | **Mantener al 100% en Pestañas 2 y 3** (Global Empresa y Proveedores); excluir solo en Pestaña 1 (Fichas Individuales). | Excluir Organa y UNALM de todo el Dashboard. | La opción recomendada preserva la realidad contable de la empresa (S/ 3.29M) y el volumen de compra a laboratorios. |
| **D4** | **Definición Estricta de "Compra" para Regla de 4ta Compra** | Contar únicamente **Días Únicos con Venta Neta Positiva** ($\sum_{\text{día}} > 0$). | Contar cada número de factura individualmente (`Nro_Doc`). | Elimina 434 distorsiones de 0 días y garantiza que la mediana $N$ refleje el ciclo de consumo real. |
| **D5** | **Gestión de Cuentas por Cobrar (T015) ante ausencia de Excel** | Crear contrato JSON/Excel y usar semáforo basado en `Cond_Pago` + `Fecha_Vencimiento < Fecha_Referencia`. | Bloquear T015 hasta que el RPA o administración descargue el archivo oficial del ERP. | Permite avanzar con el motor de alertas sin detener el desarrollo del sprint. |
| **D6** | **Semilla Inicial de Promociones Vigentes (T014b)** | Generar `data/promociones_vigentes.json` con las 7 reglas oficiales del prototipo y spec. | Cargar catálogo vacío y esperar llenado manual. | Habilita inmediatamente las sugerencias automáticas de WhatsApp para los vendedores. |

---

## 6. PRÓXIMOS PASOS TRAS LA APROBACIÓN DIRECTIVA

Una vez que el Director emita su visto bueno o ajustes sobre las decisiones D1 a D6:
1. Crear el script modular `src/motor_reglas_carteras.py` que implementa:
   - Asignación de carteras comerciales (T012).
   - Motor B2C de 25 días (T013).
   - Motor B2B de Frecuencia Dinámica y Onboarding (T014).
   - Motor de Recompra Inteligente cruzando Canasta, Kardex y Promociones (T014b).
   - Módulo de Crédito y Cobranza (T015).
   - Matriz de Lead Times por proveedor (T016).
2. Generar el dataset enriquecido de alertas operativas listo para la Fase 4 (Frontend Binding).

---
*Reporte de Preflight de Fase 3 archivado en disco bajo los lineamientos de AGENTS.md y la Constitución de Antigravity.*
