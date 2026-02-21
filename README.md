# Dashboard de Valuación de Cartera NPL

Aplicación en Streamlit para valorar cartera de crédito en mora (NPL) usando un modelo híbrido de dos etapas:

1. **Clasificador:** estima probabilidad de pago por cuenta.
2. **Regresor:** estima monto recuperable.
3. **Valor esperado:** `Probabilidad de Pago × Monto Estimado`.

---

## Funcionalidades principales

- **Evaluación individual:** analiza una sola cuenta con variables financieras y demográficas.
- **Evaluación por lote (CSV):** procesa cartera completa (`Saldo.csv` + `Detalles.csv`).
- **Dashboard ejecutivo:** muestra KPIs, ROI, VAN, TIR, segmentación y sensibilidad.
- **Detalle de cuentas:** filtros y exportación a CSV de cuentas priorizadas.

---

## Requisitos

- Python 3.10+
- Dependencias en `requirements.txt`

Instalación:

```bash
pip install -r requirements.txt
```

---

## Ejecutar localmente

```bash
streamlit run streamlit_app.py
```

La app principal se carga desde `app/dashboard.py` a través de `streamlit_app.py`.

---

## Uso de la app

### 1) Evaluación individual

Sin subir archivos, puedes simular una cuenta con:

- Saldo total
- Días de mora
- Antigüedad
- Edad
- Sexo
- Estado civil
- Meses sin pago
- Score de contactabilidad
- Ratio cuota/saldo

La app devuelve:

- Probabilidad de pago
- Recuperación estimada
- Valor esperado
- ROI estimado

### 2) Evaluación por lote

En la barra lateral:

- Cargar `Saldo.csv`
- Cargar `Detalles.csv`

Luego ajustar parámetros de compra:

- Precio por $1 de saldo
- Perfil de cobranza
- Costo operativo

El dashboard genera métricas y visualizaciones para apoyar la decisión de compra.

---

## Estructura del proyecto

```text
.
├── streamlit_app.py
├── requirements.txt
├── README.md
├── app/
│   ├── __init__.py
│   └── dashboard.py
└── models/
	├── clasificador_pago.pkl
	├── regresor_monto.pkl
	├── columnas_modelo.pkl
	└── config_mejores_params.json
```

---

## Despliegue en Streamlit Community Cloud

1. Publica este repositorio en GitHub.
2. Crea una app en Streamlit Community Cloud.
3. Selecciona como archivo principal: `streamlit_app.py`.
4. Streamlit instalará dependencias automáticamente desde `requirements.txt`.

---

## Notas

- La app requiere los artefactos del modelo en la carpeta `models/`.
- Si falta algún `.pkl` o el archivo de configuración, la app mostrará error de carga.
