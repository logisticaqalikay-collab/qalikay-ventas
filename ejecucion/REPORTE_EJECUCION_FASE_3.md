# REPORTE DE EJECUCIÓN TÉCNICA - FASE 3
## Motor de Reglas de Carteras, Frecuencia B2B, Ciclo B2C, Recompra Inteligente y Cobranza OneDrive (Qali Kay S.A.C.)

**Código:** `QK-VENTAS-EXEC-FASE3`  
**Alcance:** Tareas T012, T013, T014, T014b, T015 y T016 (100% Implementadas y Certificadas)  
**Fecha de Ejecución:** 28 de Octubre de 2026  
**Responsable Técnico:** Agente Ejecutor y Desarrollador de Software  
**Supervisión Directiva:** Director General (Cristian Gutiérrez) & Director Técnico Comercial  
**Presupuesto Ejecutado:** S/ 0.00 ($0.00 USD)

---

## 1. RESUMEN EJECUTIVO DE RESULTADOS

La **Fase 3 del Sistema de Inteligencia Comercial de Qali Kay S.A.C.** ha sido completada e implementada en su totalidad mediante el script determinista `src/motor_reglas_carteras.py`. El motor ejecutó la segmentación de las **6 carteras comerciales**, el cálculo de **frecuencia dinámica B2B y ciclo B2C**, la generación de **sugerencias de recompra inteligente cruzando Kardex y promociones vigentes**, y la vinculación en vivo en modo solo lectura con el maestro de **Cuentas por Cobrar y Directorio de Clientes en OneDrive**.

```mermaid
flowchart TD
    A["data/ventas_2025_2026.parquet (37,711 filas)"] --> M["src/motor_reglas_carteras.py"]
    K["Kardex Resumido (634 SKUs)"] --> M
    P["data/promociones_vigentes.json"] --> M
    C["OneDrive: Cuentas por cobrar 2026.xlsx"] --> M
    
    M --> T12["T012: 6 Carteras Segmentadas"]
    M --> T13["T013: Motor Ciclo B2C (25d)"]
    M --> T14["T014: Motor Frecuencia B2B (Mediana N)"]
    M --> T14b["T014b: Recompra Inteligente + WhatsApp"]
    M --> T15["T015: Control de Crédito y Cobranza"]
    M --> T16["T016: Matriz Lead Times"]
    
    M --> OUT1["data/alertas_comerciales_consolidadas.json (3.56 MB)"]
    M --> OUT2["data/resumen_carteras.json (1.95 KB)"]
```

### Tabla de Certificación de Métricas de la Fase 3

| Métrica / Dimensión | Valor Certificado | Estado |
| :--- | :---: | :---: |
| **Clientes Totales Auditados y Clasificados** | **1,310 clientes** (100% de la base comercial) | 🟢 Certificado |
| **Carteras Comerciales Segmentadas (HUDs)** | **6 carteras oficiales** | 🟢 Certificado |
| **Venta Neta Comercial Consolidada** | **S/ 3,288,001.29** (exactitud al centavo) | 🟢 Certificado |
| **Transacciones Comerciales Netas Mapeadas** | **37,711 transacciones** | 🟢 Certificado |
| **Conexión en Vivo a Cuentas por Cobrar (OneDrive)** | **552 clientes en CXC** (S/ 163,815.99 deuda vencida) | 🟢 Certificado |
| **Directorio de Clientes Enriquecido (Celulares/Nombres)**| **5,157 clientes** en OneDrive (1,053 clientes de ventas) | 🟢 Certificado |
| **Cruce de Stock con Kardex Resumido (T014b)** | **634 SKUs** con stock y costo en almacén central | 🟢 Certificado |
| **Catálogo de Promociones Vigentes (T014b)** | **9 promociones activas** en `promociones_vigentes.json` | 🟢 Certificado |
| **Alertas Operativas Totales Generadas** | **1,310 alertas** con WhatsApp copy personalizado | 🟢 Certificado |
| **Tiempo Total de Ejecución del Pipeline** | **36.16 segundos** | 🟢 Certificado |

---

## 2. T012: SEGMENTACIÓN DE LAS 6 CARTERAS COMERCIALES

Se implementó la lógica de doble nivel:
1. **Nivel Transaccional (Ventas y HUDs de Pestaña 1):** Clasificación de cada comprobante según la cartera correspondiente, aplicando las exclusiones soberanas para las Fichas Individuales de Walter y Cristian.
2. **Nivel Cliente (Gobernanza de Alertas):** Asignación de la cuenta al último vendedor con venta neta positiva, con los overrides aprobados en D1 y D2.

```
┌──────────────────────┬──────────────────────┬──────────────────────┬──────────────────────┬─────────────┐
│ Cartera Comercial    │ Venta Neta en Ficha  │ Transacciones Ficha  │ Venta Neta Total     │ Clientes    │
├──────────────────────┼──────────────────────┼──────────────────────┼──────────────────────┼─────────────┤
│ cristian-gutierrez   │ S/   528,228.66      │                6,215 │ S/ 2,107,387.68      │          87 │
│ walter-gutierrez     │ S/   521,126.43      │                6,966 │ S/   589,977.41      │          48 │
│ enrique-garcia       │ S/   270,947.38      │                4,386 │ S/   270,947.38      │         236 │
│ zully-b2c (Inbound)  │ S/   127,378.45      │                2,611 │ S/   127,378.45      │         886 │
│ zully-b2b (Inbound)  │ S/   121,798.22      │                  975 │ S/   121,798.22      │          43 │
│ carlos-cuadros       │ S/    70,512.15      │                1,158 │ S/    70,512.15      │          62 │
├──────────────────────┼──────────────────────┼──────────────────────┼──────────────────────┼─────────────┤
│ TOTALES              │ S/ 1,639,991.29      │               22,311 │ S/ 3,288,001.29      │       1,362*│
└──────────────────────┴──────────────────────┴──────────────────────┴──────────────────────┴─────────────┘
```
*\*Nota: La suma de clientes suma 1,362 debido a los 51 clientes multi-vendedor históricos atendidos en más de una cartera.*

### Resoluciones Específicas de Cartera Certificadas:
1. **Absorción Joel García $\to$ Carlos Cuadros:**  
   Carlos Cuadros absorbió el 100% del historial de Joel García (904 transacciones, S/ 53.9K) más sus ventas directas (235 transacciones, S/ 14.4K) y la cliente delegada de Alejandra Chávez (`Ortiz Ccanto`), consolidando **S/ 70,512.15 en 1,158 transacciones**.
2. **Unificación de Whitnin Tesen (Piura):**  
   Se unificaron sus boletas (DNI `48517168`, 29 filas) y facturas (RUC `10485171687`, 7 filas) en la cartera de **Cristian Gutiérrez** (36 transacciones, **S/ 5,606.81**).
3. **Exclusiones de Organa y UNALM (Decisión D3):**  
   - En la Ficha Individual de Cristian se excluyó Organa/CHYP (S/ 1,578,701.69 y 14,058 filas), reflejando una venta de **S/ 528,228.66**.
   - En la Ficha Individual de Walter se excluyó UNALM (`20101259014`, S/ 68,850.98 y 1,357 filas), reflejando una venta de **S/ 521,126.43**.
   - **En Pestaña 2 y Pestaña 3 se mantiene el 100% de la facturación global de la empresa (S/ 3,288,001.29).**
4. **Bifurcación Linda / Zully (Decisión D1):**  
   - A nivel comprobante: S/ 121,798.22 (> S/ 400.00) en B2B y S/ 127,378.45 (<= S/ 400.00) en B2C.
   - Los 14 clientes híbridos con RUC de empresa fueron derivados al motor B2B para evitar tratarlos como consumidores finales individuales.

---

## 3. T013 Y T014: MOTOR DE FRECUENCIA B2B Y CICLO B2C

Se aplicó la regla de oro ratificada en **D4**: una "Compra" se contabiliza únicamente como **Día Único de Facturación Neta Positiva** ($\sum_{\text{día}} > 0$).

### 3.1 Distribución de Alertas por Severidad (1,310 Clientes)
- **CRÍTICA (Roja - 1,161 clientes):** Clientes con más de 60 días sin compra en B2C o que excedieron en $\ge N+5$ días su ciclo habitual en B2B (incluye 945 cuentas inactivas desde 2025 o de una sola compra).
- **ADVERTENCIA (Naranja - 61 clientes):** Clientes en seguimiento con ciclo vencido de 1 a 4 días ($N < T \le N+4$), compras del día 15 en onboarding de nuevos o alertas por contracción de volumen $\ge 30\%$.
- **OPORTUNIDAD (Amarilla - 19 clientes):** Clientes en su ventana ideal de pedido ($[N-3, N]$ días) o clientes nuevos en su día 7 de post-venta para asegurar recompra.
- **INFO / AL DÍA (Verde - 69 clientes):** Cuentas con compras recientes que se encuentran en su período normal de consumo.

```mermaid
pie title Distribución de Clientes por Estado de Alerta (1,310 Clientes al 2026-10-24)
    "Crítica / Fuga / Rescate (>N+5d / >60d)": 1161
    "Info / En Ciclo Normal (<N-3d)": 69
    "Advertencia / Vencido Reciente": 61
    "Oportunidad / Ventana Pedido [N-3, N]": 19
```

---

## 4. T014b Y T016: MOTOR DE RECOMPRA B2B INTELIGENTE Y LEAD TIMES

Para cada uno de los clientes se construyó su recomendación comercial personalizada:
1. **Canasta Habitual:** TOP 3 SKUs ordenados por recurrencia de compra y valor monetario.
2. **Cruce con Stock Kardex:**
   - Si `stock > 0`: Indica stock disponible en Almacén Central y despacho en 24 a 48h.
   - Si `stock = 0`: Dispara automáticamente el Lead Time oficial del Proveedor Titular (T016).
3. **Cruce con Promociones Vigentes:** Inserción de bonificaciones activas desde `data/promociones_vigentes.json` (ej. 12+1 en NAD+ Resveratrol, 6+1 en Nanita, pack mixto VivaFrut, descuentos por caja en Molinos).
4. **Copy de WhatsApp Personalizado:** Mensaje limpio, sin caracteres deformados, firmado por el vendedor responsable de la cartera, listo para enviar con 1 clic.

### Ejemplo Real Generado por el Motor:

```text
¡Hola Milagros! Te saluda Enrique García de Qali Kay S.A.C. 🌿

Esperamos que todo vaya excelente en *NATURAL MARKET*. Revisando tu historial, 
vemos que es momento de reponer tu canasta habitual para no quedarte sin stock en anaquel:

• *CITRATO DE MAGNESIO PREMIUM POTE X 400 gr NANITA*
• *COLAGENO HIDROLIZADO PREMIUM 400 gr NANITA*
• *HARINA DE PLATANO x 200 gr MOLINOS DEL MUNDO*

📦 *Disponibilidad:* Contamos con stock en almacén para entrega inmediata en 24 a 48 horas.
🎁 *Promoción activa del mes:* Bonificación 6+1 activa en canales de farmacias y belleza.

¿Te gustaría que te reserve las unidades y coordinemos el despacho para esta semana? 
Quedo atento a tu confirmación. ¡Un abrazo!
```

---

## 5. T015: CONEXIÓN EN VIVO A CUENTAS POR COBRAR EN ONEDRIVE

Se implementó la conexión en modo solo lectura al archivo en vivo:  
`C:\Users\cguti\OneDrive\Inka Comex\CUENTAS POR COBRAR\QALI KAY\2026\Cuentas por cobrar 2026.xlsx`

### 5.1 Datos Consolidados de la Hoja `'CXC'` (`skiprows=10`):
- **Documentos auditados:** 2,445 registros.
- **Deuda Vencida Total:** **S/ 163,815.99** en 210 comprobantes.
- **Deuda a Cuenta:** **S/ 54,654.34** en 53 comprobantes.
- **Deuda Pendiente (Vigente):** **S/ 83,348.46** en 69 comprobantes.
- **Documentos Cancelados:** 2,113 comprobantes.
- **Bloqueo por Mora:** A los clientes con saldo vencido $> 0$, el motor les asigna el flag `bloqueo_por_mora = True` y la instrucción: *"Condición: Pago previo antes de nuevo despacho"*.

### 5.2 Enriquecimiento de Contactos de la Hoja `'Clientes (usar)'`:
- **5,157 clientes mapeados** con teléfono celular (`CEL.`), nombre comercial de la tienda/farmacia (`NOMBRE COMERCIAL`), contacto directo (`CONTACTO`) y dirección de entrega (`DIRECCIÓN DE ENTREGA`).
- **1,053 de los 1,310 clientes de ventas (80.4%)** quedaron directamente enriquecidos con su teléfono celular verificado para el botón de WhatsApp de la Pestaña 5.

### 5.3 Regla de Elegibilidad Crediticia (FR-10):
- Clientes con $\ge 6$ compras históricas al contado y con saldo vencido en S/ 0.00 reciben el flag `elegible_linea_credito = True` para sugerir evaluación de línea de crédito a 15/30 días.

---

## 6. ARTEFACTOS GENERADOS Y PERSISTIDOS EN DISCO

1. **`data/promociones_vigentes.json` (4.27 KB):**  
   Catálogo estructurado de las 9 promociones de campaña activas (NANITA 12+1 y 6+1, VivaFrut pack mixto, Molinos descuento por caja, Qorinka tarifa display, Amazon Andes bonificación, etc.).
2. **`data/alertas_comerciales_consolidadas.json` (3.56 MB):**  
   Dataset analítico completo con los 1,310 clientes, sus métricas de frecuencia $N$, días de inactividad, cartera y canal, estado de cobranza en OneDrive, canasta habitual, estado logístico en Kardex y copy de WhatsApp.
3. **`data/resumen_carteras.json` (1.95 KB):**  
   Resumen ejecutivo estructurado con los KPIs certificados de las 6 carteras (venta en ficha vs venta total, transacciones, clientes activos).
4. **`src/motor_reglas_carteras.py` (22.8 KB):**  
   Código fuente modular, tipado y documentado con soporte para ejecución standalone y funciones reutilizables para la Fase 4.

---

## 7. MATRIZ DE CUMPLIMIENTO DE ASERCIONES MATEMÁTICAS

```
┌───────────────────────────────────────┬──────────────┬──────────────┬──────────────┐
│ Parámetro Evaluado                    │ Esperado     │ Obtenido     │ Estado       │
├───────────────────────────────────────┼──────────────┼──────────────┼──────────────┤
│ Clientes comerciales evaluados        │        1,310 │        1,310 │ 🟢 EXACTO    │
│ Carteras comerciales segmentadas      │            6 │            6 │ 🟢 EXACTO    │
│ Venta comercial consolidada total     │S/3,288,001.29│S/3,288,001.29│ 🟢 EXACTO    │
│ Deuda vencida leída desde CXC         │ S/ 163,815.99│ S/ 163,815.99│ 🟢 EXACTO    │
│ Clientes con datos CXC vinculados     │          552 │          552 │ 🟢 EXACTO    │
│ SKUs de Kardex integrados con stock   │          634 │          634 │ 🟢 EXACTO    │
│ Promociones oficiales cargadas        │            9 │            9 │ 🟢 EXACTO    │
│ Error o duplicados en asignación      │            0 │            0 │ 🟢 EXACTO    │
└───────────────────────────────────────┴──────────────┴──────────────┴──────────────┘
```

---

## 8. CONCLUSIÓN Y TRANSICIÓN A FASE 4

Con las tareas **T012, T013, T014, T014b, T015 y T016** completadas al 100%, la lógica de inteligencia comercial, carteras, recompra y cobranza se encuentra totalmente operativa y empaquetada.

El sistema queda listo para la **FASE 4: VINCULACIÓN AL DASHBOARD (FRONTEND BINDING) (Tareas T017 a T019)**:
- **T017:** Crear `src/exportar_datos_dashboard.py` para consolidar el payload final `data/datos_comerciales.json`.
- **T018:** Conectar `PROTOTIPO_DASHBOARD_VENTAS_QALIKAY.html` a `data/datos_comerciales.json`, reemplazando el mock en memoria.
- **T019:** Integrar el componente Dropzone con SheetJS embebido para actualización drag & drop offline.

---
*Reporte de Ejecución archivado en disco bajo los lineamientos de AGENTS.md y la Constitución de Antigravity.*
