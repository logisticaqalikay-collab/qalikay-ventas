# Blueprint Maestro: Sistema de Inteligencia Comercial, KPIs y Alertas — Qali Kay (V4.1 Final)

> [!IMPORTANT]
> **Reglas Inquebrantables del Proyecto (`Constitution`):**
> 1. **Aislamiento Total (Cero Modificación a Otros Proyectos):** Queda **terminantemente prohibido** modificar códigos, scripts o automatizaciones de `qalikay-abastecimiento` (ni de ningún otro repositorio). `qalikay-ventas` es 100% autónomo.
> 2. **Base Histórica 2025 + 2026 con Ventana Incremental de 2 Meses (60 días):** El sistema analiza **todo el 2025 y todo el 2026**. La actualización diaria incremental procesa una **ventana rodante de los últimos 60 días (2 meses)** para capturar automáticamente Notas de Crédito, anulaciones o modificaciones de documentos pasados sin tener que reprocesar los 24 meses.
> 3. **Gestión Activa de Clientes B2C Vencidos:** Los consumidores finales B2C que superan su ciclo estimado (**> 25 días** para recompra preventiva o **> 60 días** inactivos) tienen filtro visible directo en el dashboard y botones de WhatsApp listos para campañas de reactivación/reposición de frasco.
> 4. **Estándar UX con Skill `impeccable`:** El diseño, jerarquía visual, experiencia mobile y accesibilidad del Dashboard se auditan y pulen utilizando la skill **`impeccable`** (modo `Operate` para dashboards de alta densidad de datos).
> 5. **Privacidad Estricta:** Ningún archivo de Google Drive ni de OneDrive se expone como enlace público.

---

## 1. Arquitectura de Datos 2025–2026 (Sin tocar `qalikay-abastecimiento`)

1. **Almacén Histórico Propio en `qalikay-ventas` (`data/ventas_2025_2026.parquet`):**
   * **Carga Inicial (1 sola vez):** Se incorpora el histórico completo `01/01/2025 – 31/12/2025` y los meses cerrados anteriores a la ventana rodante.
   * **Actualización Incremental Diaria (07:30 AM y 03:30 PM):**
     * Descarga de Defontana los **últimos 60 días (2 meses)**.
     * Aplica `upsert` por clave única (`Nombre Doc + Número del Documento + Cod. Producto`) sobre la base consolidada `2025–2026`.
     * Cualquier anulación o Nota de Crédito aplicada dentro de los últimos 2 meses sobreescribe y actualiza el estado real de la venta de inmediato.
2. **Privacidad en los 2 Archivos de Prospectos en Google Drive (`1JgTmPRm...` y `1Wycm8UH...`):**
   * Ambos archivos se mantienen en modo **Restringido (Privado)**.
   * Se leen de forma privada guardándolos como *Hojas de cálculo de Google* nativas en la misma carpeta privada o mediante credencial con permisos específicos, sin enlaces públicos.

---

## 2. Cuadro de Indicadores MENSUAL por Vendedor + Comparativa en el Tiempo (2025–2026)

### A. Cuadro Mensual por Vendedor (Selector de Mes: Sep 2026, Ago 2026, Jul 2026...)
Muestra el desempeño **del mes seleccionado** para las **6 carteras** (`Enrique`, `Walter`, `Cristian`, `Linda/Zully B2B >S/400`, `Carlos C +ex Joel`, `Linda/Zully B2C <=S/400`):

| Ejecutivo / Canal | Venta Neta del Mes | Clientes del Mes / Cartera | Pedidos del Mes | Ticket Prom. Mes | 🟢 Nuevos del Mes | 🟠 1 Sola Compra (>2M) | 🔴 Sin Comprar (>2M) |
| :--- | ---: | :---: | :---: | ---: | :---: | :---: | :---: |
| **1. Enrique García** | S/ 22,489.51 | 38 / 67 | 47 | S/ 478.50 | 13 | 7 | 7 |
| **2. Walter Gutiérrez** *(s/UNALM)* | S/ 15,757.28 | 14 / 23 | 28 | S/ 562.76 | 2 | 2 | 2 |
| **3. ⭐ Cristian Gutiérrez** *(Mi Cartera)* | S/ 12,821.43 | 6 / 7 | 10 | **S/ 1,282.14** | 1 | 0 | 0 |
| **4. Carlos Cuadros** *(+ex Joel)* | S/ 4,794.81 | 9 / 18 | 11 | S/ 435.89 | 5 | 2 | 3 |
| **5. 🏢 Linda / Zully — B2B (`> S/400`)** | S/ 4,273.86 | 4 / 10 | 4 | **S/ 1,068.47** | 1 | 3 | 3 |
| **6. 👤 Linda / Zully — B2C (`<= S/400`)** | S/ 4,165.63 | 35 / 87 | 39 | S/ 106.81 | 30 | 20 | 21 |
| **TOTAL EMPRESA** | **S/ 64,302.52** | **106** | **139** | **S/ 462.61** | **52** | **34** | **36** |

### B. Módulo de Gestión y Reactivación B2C
* **B2C en Ciclo de Reposición (25 a 35 días):** Alerta preventiva de fin de frasco. Mensaje de reposición habitual para no cortar consumo.
* **B2C Vencidos (> 35 a 60 días):** Alerta de seguimiento. Pregunta de satisfacción y recordatorio de continuidad.
* **B2C Inactivos / Rescate (> 60 días o 1 sola compra):** Oferta especial (pack dúo o descuento en 2da unidad) para reactivar al cliente.

---

## 3. Adopción de la Skill `impeccable` para UX/UI

La skill **`impeccable`** se usará para auditar y pulir el frontend del Dashboard (`qalikay-ventas`):
1. **Modo `Operate`:** Jerarquía de escaneo rápido para directores y vendedores (semáforos contrastados, datos numéricos alineados a la derecha, badges informativos legibles).
2. **Mobile UX:** Optimización táctil para smartphones (botones de WhatsApp grandes, filas expandibles en tabla, tipografía no menor a 12px).
3. **Control de Errores y Estados Vacíos:** Pantallas claras cuando no haya alertas pendientes o cuando Defontana tarde en actualizar.

---

## 4. Matriz de Proveedores y Flujo `Spec-Kit` en `qalikay-ventas`

* **Proveedores Rápidos (1–2 días $\rightarrow$ si `Stock = 0`, entrega en 4–5 días hábiles + aviso a Compras):** `NUTRIVAS`, `AMAZON ANDES`, `TAURI`, `OLIVO DE ORO`, `DEPURATÉ`, `INKA COMEX`, `ANDES CRISP`.
* **Entrega Fija Semanal (Miércoles):** `MOLINOS DEL MUNDO` (`SANTIVERI`).
* **Demoras Mayores:** `QORINKA` (4 días), `PECADITOS INTEGRALES` (1 semana), `FIBRA FRUT` / `VIVAFRUT` (1 semana), `FUNGI AMAZÓNICA` (propio).
* **Liquidación:** `QORI`, `NOA LIFE`, `INKA PRIME`.
* **Flujo `Spec-Kit`:** 1. `constitution` $\rightarrow$ 2. `specify` $\rightarrow$ 3. **`clarify`** $\rightarrow$ 4. `plan` $\rightarrow$ 5. `tasks` + `analyze` $\rightarrow$ 6. `implement` $\rightarrow$ 7. `impeccable polish`.
