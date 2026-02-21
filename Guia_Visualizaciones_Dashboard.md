# Guía de Lectura de Visualizaciones — Dashboard NPL

## Índice

1. [Métricas KPI (Resumen Ejecutivo)](#1-métricas-kpi-resumen-ejecutivo)
2. [Indicadores Clave (Semáforo de Decisión)](#2-indicadores-clave-semáforo-de-decisión)
3. [Gauge de ROI](#3-gauge-de-roi)
4. [Cascada de Valor](#4-cascada-de-valor)
5. [Flujos de Recuperación Mensual Proyectados](#5-flujos-de-recuperación-mensual-proyectados)
6. [Distribución de Probabilidad de Pago](#6-distribución-de-probabilidad-de-pago)
7. [Distribución de Valor Esperado](#7-distribución-de-valor-esperado)
8. [Mapa de Riesgo: Mora vs Valor Esperado](#8-mapa-de-riesgo-mora-vs-valor-esperado)
9. [Saldo vs Valor Esperado por Segmento](#9-saldo-vs-valor-esperado-por-segmento)
10. [Box Plots por Segmento](#10-box-plots-por-segmento)    
11. [Segmentación de Cartera (Donas)](#11-segmentación-de-cartera-donas)
12. [Análisis por Características](#12-análisis-por-características)
13. [TIR y VAN por Escenario de Cumplimiento](#13-tir-y-van-por-escenario-de-cumplimiento)
14. [Mapa de Calor: TIR por Precio y Cumplimiento](#14-mapa-de-calor-tir-por-precio-y-cumplimiento)
15. [Precio Máximo según TIR Objetivo](#15-precio-máximo-según-tir-objetivo)
16. [Tabla de Detalle de Cuentas](#16-tabla-de-detalle-de-cuentas)

---

## 1. Métricas KPI (Resumen Ejecutivo)

**Ubicación:** Panel superior, inmediatamente después de cargar los datos.

Se muestran **10 tarjetas métricas** organizadas en dos filas:

| Métrica | Qué significa | Cómo leerla |
|---------|---------------|-------------|
| **Cuentas** | Número total de cuentas en el lote cargado. | Referencia de tamaño del lote. |
| **Saldo Facial** | Suma de los saldos totales adeudados por todos los deudores. | Es el valor nominal de la cartera, no lo que se espera recuperar. |
| **Valor Esperado** | Suma de `P(pago) × Monto estimado` para cada cuenta. | Cuánto predice el modelo que se puede recuperar en términos brutos. |
| **Precio Compra** | = Saldo Facial × Precio por $1 (configurado en barra lateral). | Lo que se pagaría por el lote al precio establecido. |
| **Utilidad Neta** | = Recuperación Neta − Precio de Compra. El indicador `delta` muestra el ROI. | Positivo = ganancia; negativo = pérdida. El delta porcentual facilita la comparación rápida. |
| **TIR Anual** | Tasa Interna de Retorno anualizada, calculada sobre flujos mensuales. | Compararla contra la tasa de referencia del inversionista (ej. 10-25%). |
| **VAN (tasa 10%)** | Valor Actual Neto descontando al 10% anual. | VAN > 0 indica que el lote genera valor por encima de la tasa de descuento. |
| **Múltiplo (x)** | = Recuperación Neta / Precio de Compra. | >1x significa que se recupera más de lo invertido; >1.5x es favorable. |
| **Pagadores Est. (>50%)** | Cuentas con probabilidad de pago > 50%. | Proporción esperada de deudores que harán al menos un pago. |
| **Costo Operativo** | = Valor Esperado × % de costo de gestión. | Refleja gastos de cobranza (call center, legal, etc.). |

---

## 2. Indicadores Clave (Semáforo de Decisión)

**Ubicación:** Pestaña "Decisión de Compra", columna izquierda.

Sistema de evaluación con cuatro criterios:

| Criterio | Favorable `[+]` | Precaución `[~]` | Desfavorable `[-]` |
|----------|-----------------|-------------------|--------------------|
| ROI | > 30% | 10–30% | < 10% |
| TIR | > 25% | 10–25% | < 10% |
| VAN (10%) | Positivo | — | Negativo |
| Múltiplo | > 1.5x | 1.0–1.5x | < 1.0x |

**Resultado final:**
- **3-4 favorables** → "COMPRAR": los indicadores respaldan la inversión.
- **2 favorables** → "EVALUAR CON CUIDADO": considerar ajustar precio o margen.
- **0-1 favorables** → "NO COMPRAR / RENEGOCIAR": riesgo alto, buscar mejor precio.

---

## 3. Gauge de ROI

**Ubicación:** Pestaña "Decisión de Compra", columna derecha.

Indicador de velocímetro (gauge) que representa el ROI esperado en porcentaje.

- **Zonas de color del fondo:**
  - Roja (< 0%): inversión con pérdida esperada.
  - Amarilla (0%–20%): retorno positivo pero por debajo de la referencia.
  - Verde (> 20%): retorno atractivo.
- **Barra central:** color dinámico (verde/naranja/rojo) según el valor del ROI.
- **Línea de referencia:** marca el 20% como umbral de comparación.
- **Delta:** diferencia respecto al 20% de referencia.

**Lectura rápida:** Si la aguja queda en zona verde y el delta es positivo, el lote tiene un retorno atractivo.

---

## 4. Cascada de Valor

**Ubicación:** Pestaña "Decisión de Compra", ancho completo.

Gráfico de cascada (*waterfall*) que descompone cómo se llega de la recuperación bruta a la utilidad neta:

```
Recuperación Bruta  →  (−) Costo Operativo  →  (−) Precio de Compra  →  Utilidad Neta
```

- **Barra verde:** flujo positivo (recuperación bruta).
- **Barras rojas:** deducciones (costos, precio).
- **Barra total azul/roja:** utilidad neta. Azul si es positiva, rojo si es negativa.
- **Etiquetas numéricas:** cada barra muestra su valor en dólares.

**Lectura rápida:** Si la barra final (Utilidad Neta) es azul y su valor es positivo, el lote es rentable después de costos.

---

## 5. Flujos de Recuperación Mensual Proyectados

**Ubicación:** Pestaña "Decisión de Compra", parte inferior.

Gráfico de barras + línea con doble eje Y:

- **Barras azules (eje izquierdo):** flujo neto mensual esperado (después de costos operativos). Cada barra representa cuánto se espera cobrar en ese mes.
- **Línea verde (eje derecho):** acumulado progresivo de lo cobrado.
- **Línea roja discontinua (etiqueta "Inversión"):** monto de la inversión inicial, referencia para el punto de equilibrio.
- **Línea naranja punteada:** marca el mes de *break-even* (payback), donde el acumulado supera al precio de compra.

**Lectura rápida:**
- Cuando la línea verde cruza la línea roja, se alcanza el punto de equilibrio.
- Si el perfil es "decreciente", las barras son más altas al inicio y bajan — típico de cobranza agresiva en los primeros meses.
- Si el payback es > 12 meses, la inversión no se recupera en el horizonte modelado.

---

## 6. Distribución de Probabilidad de Pago

**Ubicación:** Pestaña "Distribución", esquina superior izquierda.

Histograma de las probabilidades predichas por el clasificador para cada cuenta.

- **Eje X:** probabilidad de pago (0 a 1).
- **Eje Y:** número de cuentas.
- **Línea roja discontinua vertical:** umbral del 50%.
- **Cuentas a la derecha del 50%:** el modelo predice que probablemente pagarán.
- **Cuentas a la izquierda del 50%:** el modelo predice que probablemente NO pagarán.

**Lectura rápida:** Si la mayor parte de las cuentas se concentra a la izquierda (< 0.5), el lote es de riesgo alto. Si hay una proporción significativa a la derecha, el lote tiene potencial de recuperación.

---

## 7. Distribución de Valor Esperado

**Ubicación:** Pestaña "Distribución", esquina superior derecha.

Histograma del valor esperado (VE = P(pago) × Monto estimado) para cuentas con VE > 0.

- **Eje X:** valor esperado en dólares.
- **Eje Y:** número de cuentas.
- **Cola derecha larga:** indica que pocas cuentas concentran mucho valor.

**Lectura rápida:** Una distribución sesgada a la derecha es normal en cartera NPL — pocas cuentas "estrella" aportan la mayor parte del valor. Evaluar si la concentración es excesiva (riesgo de depender de pocas cuentas).

---

## 8. Mapa de Riesgo: Mora vs Valor Esperado

**Ubicación:** Pestaña "Distribución", esquina inferior izquierda.

Scatter plot (diagrama de dispersión) bidimensional:

- **Eje X:** días de mora de cada cuenta.
- **Eje Y:** valor esperado en dólares.
- **Color:** probabilidad de pago (escala Rojo → Amarillo → Verde).
- **Tamaño de burbuja:** monto estimado de recuperación.

**Lectura rápida:**
- Puntos **verdes abajo-izquierda** (poca mora, alta probabilidad): cuentas fáciles de cobrar.
- Puntos **rojos arriba-derecha** (mucha mora, baja probabilidad pero alto saldo): cuentas difíciles pero de alto valor teórico.
- Las cuentas más rentables son las verdes con burbujas grandes.

---

## 9. Saldo vs Valor Esperado por Segmento

**Ubicación:** Pestaña "Distribución", esquina inferior derecha.

Scatter plot que contrasta el saldo facial de cada cuenta con su valor esperado:

- **Eje X:** saldo total ($).
- **Eje Y:** valor esperado ($).
- **Color por segmento:** Verde (Alto Potencial), Naranja (Moderado), Rojo (Bajo Potencial).
- **Diagonal ideal:** si VE = Saldo, se recupera el 100%.

**Lectura rápida:** Las cuentas por debajo de la diagonal (VE << Saldo) tienen baja recuperabilidad. Cuentas cerca de la diagonal en verde son las más atractivas.

---

## 10. Box Plots por Segmento

**Ubicación:** Pestaña "Distribución", sección "Distribución por Segmento".

Dos gráficos de caja (*box plots*) lado a lado:

**Gráfico izquierdo — Probabilidad de Pago por Segmento:**
- Muestra la mediana, cuartiles y outliers de P(pago) para cada segmento.
- Alto Potencial debería tener mediana > 0.4 y distribución alta.
- Bajo Potencial debería concentrarse cerca de 0.

**Gráfico derecho — Valor Esperado por Segmento:**
- Misma estructura pero para el VE en dólares.
- Permite ver la dispersión del valor dentro de cada grupo.
- Outliers (puntos individuales) representan cuentas con valor excepcionalmente alto.

**Lectura rápida:** Cajas más altas y más a la derecha = mejor. Los bigotes largos hacia arriba en "Alto Potencial" indican oportunidades de valor concentrado.

---

## 11. Segmentación de Cartera (Donas)

**Ubicación:** Pestaña "Segmentación", fila superior.

Dos gráficos de dona (*donut charts*):

**Dona izquierda — Distribución del Valor Esperado:**
- Qué proporción del VE total aporta cada segmento.
- Si "Alto Potencial" concentra >60% del VE, la cartera es más predecible.

**Dona derecha — Distribución de Cuentas:**
- Cuántas cuentas hay en cada segmento.
- Normalmente la mayoría de cuentas NPL serán "Bajo Potencial" pero aportarán poco VE.

**Tabla resumen debajo:** detalla métricas exactas por segmento (VE total, promedio, mediana, tasa de pago, % de cartera).

---

## 12. Análisis por Características

**Ubicación:** Pestaña "Segmentación", sección inferior.

Gráfico de barras que agrupa las cuentas por una variable categórica seleccionable (Sexo, Estado Civil, Producto, Lote, Rango Mora).

- **Eje X:** categoría seleccionada.
- **Eje Y (barras):** valor esperado total por grupo.
- **Color de barra:** probabilidad de pago promedio del grupo (escala Rojo → Verde).
- **Etiquetas:** valor en dólares sobre cada barra.

**Lectura rápida:** Barras altas y verdes = segmentos con alto valor Y alta probabilidad. Permite identificar nichos de mayor recuperabilidad (ej. "Casados" o "Producto X" podrían tener mejor tasa).

---

## 13. TIR y VAN por Escenario de Cumplimiento

**Ubicación:** Pestaña "Sensibilidad & TIR", gráfico principal.

Gráfico combinado de línea + barras con doble eje Y:

- **Línea azul (eje izquierdo):** TIR anual (%) para cada escenario de cumplimiento.
- **Barras verde/roja (eje derecho):** VAN ($) — verde si positivo, rojo si negativo.
- **Línea gris discontinua horizontal:** TIR = 0% (línea de pérdida).
- **Línea roja punteada:** tasa de referencia configurada en la simulación.

**Eje X:** escenarios de cumplimiento del Valor Esperado (ej. 50%, 60%, ..., 120%).
- 100% = se cobra exactamente lo que predice el modelo.
- 80% = se cobra solo el 80% de lo predicho (escenario pesimista).
- 120% = se cobra un 20% más de lo predicho (escenario optimista).

**Lectura rápida:**
- Si la TIR se mantiene por encima de la línea roja incluso al 60-70% de cumplimiento, la inversión es robusta.
- Si la TIR cruza el 0% antes del 80%, el modelo debe cumplir casi perfectamente para no perder dinero — riesgo alto.

**Tabla de escenarios debajo:** valores exactos de TIR, VAN, ROI y Múltiplo para cada escenario. Celdas verdes = VAN positivo; celdas rojas = VAN negativo.

---

## 14. Mapa de Calor: TIR por Precio y Cumplimiento

**Ubicación:** Pestaña "Sensibilidad & TIR", sección inferior.

Heatmap (mapa de calor) bidimensional que muestra la TIR para combinaciones de:

- **Eje X:** porcentaje de cumplimiento de la recuperación (40% a 120%).
- **Eje Y:** precio de compra por $1 de saldo ($0.01 a $0.15).
- **Color de celda:** TIR anual — rojo (pérdida), amarillo (bajo retorno), verde (retorno atractivo).
- **Texto en celda:** valor numérico de la TIR (%).
- **Marcador "Actual":** indica la combinación de precio y cumplimiento actualmente configurada.

**Lectura rápida:**
- La esquina inferior-derecha (precio bajo + cumplimiento alto) es siempre verde — el mejor escenario.
- La esquina superior-izquierda (precio alto + cumplimiento bajo) es roja — el peor escenario.
- El gradiente entre ambas esquinas indica qué tan sensible es el retorno a cambios en precio o cumplimiento.
- Si el marcador "Actual" está en zona verde, la configuración es favorable. Si está en zona amarilla/roja, revisar el precio.

---

## 15. Precio Máximo según TIR Objetivo

**Ubicación:** Pestaña "Sensibilidad & TIR", parte final.

Cálculo de búsqueda binaria que responde la pregunta: *"¿Cuánto es lo máximo que puedo pagar para obtener una TIR del X%?"*

- **Precio Máximo ($):** monto total máximo a pagar por el lote completo.
- **Precio por $1 de saldo:** cuántos centavos pagar por cada dólar de saldo facial.
- **TIR al precio máximo:** confirma que al pagar ese monto se logra exactamente la TIR objetivo.

**Lectura rápida:** Si el precio calculado es mayor al precio actual de oferta del lote, hay margen de negociación favorable. Si es menor, el precio ofrecido es demasiado alto para lograr la TIR deseada.

---

## 16. Tabla de Detalle de Cuentas

**Ubicación:** Pestaña "Detalle de Cuentas".

Tabla interactiva con datos a nivel de cuenta individual:

| Columna | Descripción |
|---------|-------------|
| CUENTA | Identificador único del deudor. |
| SALDO TOTAL | Saldo facial adeudado. |
| DIAS MORA | Días transcurridos desde el último pago. |
| Prob_Pago | Probabilidad estimada de que el deudor realice al menos un pago (0 a 1). |
| Monto_Estimado | Si paga, cuánto se estima que pagará ($). |
| Valor_Esperado | = Prob_Pago × Monto_Estimado. Valor ajustado por riesgo. |
| ROI_Cuenta | = Valor_Esperado / Saldo Total. Tasa de recuperación individual. |
| Segmento | Clasificación: Alto Potencial (≥ 0.4), Moderado (0.2–0.4), Bajo Potencial (< 0.2). |

**Filtros disponibles:**
- Segmento: incluir/excluir grupos.
- Rango de Probabilidad: acotar cuentas por umbral.
- Top N: limitar a las N cuentas de mayor valor esperado.

**Gradiente de color:** la columna Valor_Esperado tiene fondo verde más intenso para valores más altos (facilita identificar las cuentas más valiosas visualmente).

**Métricas resumen de selección:** Cuentas mostradas, VE de selección, % del VE total, Probabilidad promedio.

**Botón de descarga:** exporta la selección filtrada a CSV para análisis offline o integración con sistemas de cobranza.

---

## Glosario de Términos Financieros

| Término | Definición |
|---------|------------|
| **NPL** | *Non-Performing Loan*. Crédito vencido con incumplimiento de pago. |
| **VE** | Valor Esperado = Probabilidad × Monto. Estimación ajustada por riesgo. |
| **ROI** | *Return on Investment*. Ganancia neta dividida entre inversión inicial. |
| **VAN** | *Valor Actual Neto*. Suma de flujos futuros descontados menos la inversión. VAN > 0 crea valor. |
| **TIR** | *Tasa Interna de Retorno*. Tasa que hace VAN = 0. Comparable con el costo de oportunidad. |
| **Múltiplo** | Recuperación total / Inversión. 2.0x significa que se recuperó el doble de lo invertido. |
| **Payback** | Mes en que el acumulado de flujos supera la inversión inicial. |
| **Saldo Facial** | Valor nominal total adeudado, sin ajustar por probabilidad de cobro. |
| **Hurdle Model** | Modelo de dos etapas: (1) Clasificador predice si paga, (2) Regresor predice cuánto paga. |

---

