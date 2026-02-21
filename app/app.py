import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

# ============================================================
# CONFIGURACIÓN
# ============================================================
st.set_page_config(
    page_title="Valuador de Cartera NPL — Grupo 4",
    layout="wide"
)

st.title("Valuador de Cartera de Crédito — Grupo 4")
st.markdown("**Sistema de Valuación de Activos (NPL)** — Modelo Híbrido de Dos Etapas")

# ============================================================
# CARGA DE MODELOS
# ============================================================
MODELS_DIR = os.path.join(os.path.dirname(__file__), '..', 'models')


@st.cache_resource
def load_artifacts():
    """Carga los artefactos del modelo entrenado."""
    clf = joblib.load(os.path.join(MODELS_DIR, 'clasificador_pago.pkl'))
    reg = joblib.load(os.path.join(MODELS_DIR, 'regresor_monto.pkl'))
    cols = joblib.load(os.path.join(MODELS_DIR, 'columnas_modelo.pkl'))
    return clf, reg, cols


try:
    clf, reg, model_cols = load_artifacts()
    st.sidebar.success("Modelos cargados correctamente")
except Exception as e:
    st.error(f"Error cargando modelos: {e}")
    st.info("Ejecuta el Notebook 4 primero para generar los artefactos.")
    st.stop()


# ============================================================
# FUNCIONES DE PREPROCESAMIENTO
# ============================================================
def preprocesar_cliente(saldo, dias_mora, antiguedad, recencia, edad, sexo,
                        civil, score_contact=3.0, ratio_cuota=0.02):
    """Preprocesa un cliente individual y retorna DataFrame listo para predicción."""
    log_saldo = np.log1p(saldo)
    mora_clipped = min(dias_mora, 720)

    input_data = pd.DataFrame(columns=model_cols)
    input_data.loc[0] = 0

    input_data['LOG_SALDO'] = log_saldo
    input_data['ANTIGUEDAD_MESES'] = antiguedad
    input_data['EDAD_CLIENTE'] = edad
    input_data['MESES_DESDE_ULTIMO_PAGO'] = recencia
    input_data['DIAS MORA'] = mora_clipped
    input_data['SCORE_CONTACTABILIDAD'] = score_contact
    input_data['RATIO_CUOTA_SALDO'] = ratio_cuota

    if f'SEXO_{sexo}' in input_data.columns:
        input_data[f'SEXO_{sexo}'] = 1
    if f'EST_CIVIL_CLEAN_{civil}' in input_data.columns:
        input_data[f'EST_CIVIL_CLEAN_{civil}'] = 1

    return input_data


def preprocesar_lote(df_saldo, df_detalles):
    """Preprocesa un lote completo de datos para predicción batch."""
    def limpiar_moneda(val):
        if isinstance(val, str):
            val = val.replace('$', '').replace(',', '').replace(' ', '')
            try:
                return float(val)
            except ValueError:
                return 0.0
        return val

    df = df_saldo.copy()

    for col in ['SALDO TOTAL', 'VALOR CUOTA']:
        if col in df.columns:
            df[col] = df[col].apply(limpiar_moneda)

    # Merge con detalles si se proporcionan
    if df_detalles is not None and 'CUENTA' in df.columns and 'CUENTA' in df_detalles.columns:
        df['CUENTA'] = pd.to_numeric(df['CUENTA'], errors='coerce')
        df_detalles = df_detalles.copy()
        df_detalles['CUENTA'] = pd.to_numeric(df_detalles['CUENTA'], errors='coerce')
        df = pd.merge(df, df_detalles, on='CUENTA', how='left', suffixes=('', '_det'))

    # Feature Engineering
    if 'SALDO TOTAL' in df.columns:
        df['LOG_SALDO'] = np.log1p(df['SALDO TOTAL'].fillna(0).astype(float))
    else:
        df['LOG_SALDO'] = 0

    if 'DIAS MORA' in df.columns:
        df['DIAS MORA'] = pd.to_numeric(df['DIAS MORA'], errors='coerce').fillna(360).clip(upper=720)
    else:
        df['DIAS MORA'] = 360

    # Fechas
    for col in ['FECHA_APERTURA', 'FECHA NACIMIENTO', 'FECHA ULTIMO PAGO']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], dayfirst=True, errors='coerce')

    fecha_ref = pd.Timestamp.now()

    if 'FECHA_APERTURA' in df.columns:
        df['ANTIGUEDAD_MESES'] = (fecha_ref - df['FECHA_APERTURA']) / pd.Timedelta(days=30)
        df['ANTIGUEDAD_MESES'] = df['ANTIGUEDAD_MESES'].fillna(df['ANTIGUEDAD_MESES'].median())
    else:
        df['ANTIGUEDAD_MESES'] = 36

    if 'FECHA NACIMIENTO' in df.columns:
        df['EDAD_CLIENTE'] = (fecha_ref - df['FECHA NACIMIENTO']) / pd.Timedelta(days=365.25)
        med = df['EDAD_CLIENTE'].median()
        df.loc[(df['EDAD_CLIENTE'] < 18) | (df['EDAD_CLIENTE'] > 90), 'EDAD_CLIENTE'] = med
        df['EDAD_CLIENTE'] = df['EDAD_CLIENTE'].fillna(med if pd.notna(med) else 40)
    else:
        df['EDAD_CLIENTE'] = 40

    if 'FECHA ULTIMO PAGO' in df.columns:
        df['MESES_DESDE_ULTIMO_PAGO'] = (fecha_ref - df['FECHA ULTIMO PAGO']) / pd.Timedelta(days=30)
        df['MESES_DESDE_ULTIMO_PAGO'] = df['MESES_DESDE_ULTIMO_PAGO'].fillna(999)
    else:
        df['MESES_DESDE_ULTIMO_PAGO'] = 999

    # Score de Contactabilidad
    email = df.get('EMAIL CLIENTE', pd.Series('', index=df.index)).fillna('').astype(str).str.strip().apply(lambda x: 1 if len(x) > 0 and x != '0' and x.lower() != 'nan' else 0)
    direccion = df.get('DIRECCION RESIDENCIAL', pd.Series('', index=df.index)).fillna('').astype(str).str.strip().apply(lambda x: 1 if len(x) > 0 and x != '0' and x.lower() != 'nan' else 0)
    trabajo = df.get('LUGAR_TRABAJO', pd.Series('', index=df.index)).fillna('').astype(str).str.strip().apply(lambda x: 1 if len(x) > 0 and x != '0' and x.lower() != 'nan' else 0)
    telefonos = pd.to_numeric(df.get('TELEFONOS', pd.Series(0, index=df.index)), errors='coerce').fillna(0)
    df['SCORE_CONTACTABILIDAD'] = email * 1 + direccion * 1 + trabajo * 2 + telefonos * 0.5

    # Ratio cuota/saldo
    cuota = df.get('VALOR CUOTA', pd.Series(0, index=df.index)).fillna(0).astype(float)
    saldo_val = df.get('SALDO TOTAL', pd.Series(1, index=df.index)).fillna(1).astype(float)
    df['RATIO_CUOTA_SALDO'] = np.where(saldo_val > 0, cuota / saldo_val, 0)

    # Categóricas
    if 'SEXO' in df.columns:
        df['SEXO'] = df['SEXO'].apply(lambda v: 'M' if str(v).upper().strip() in ['M', 'MASCULINO']
                                      else ('F' if str(v).upper().strip() in ['F', 'FEMENINO'] else 'X'))
    else:
        df['SEXO'] = 'X'

    if 'EST CIVIL' in df.columns:
        def normalizar_civil(val):
            val = str(val).upper().strip()
            if val in ['S', 'SOLTERO', 'SOLTERA']:
                return 'SOLTERO'
            if val in ['C', 'CASADO', 'CASADA']:
                return 'CASADO'
            if val in ['D', 'DIVORCIADO']:
                return 'DIVORCIADO'
            if val in ['U', 'UL', 'UNION LIBRE', 'UNION_LIBRE']:
                return 'UNION_LIBRE'
            return 'OTROS'
        df['EST_CIVIL_CLEAN'] = df['EST CIVIL'].apply(normalizar_civil)
    else:
        df['EST_CIVIL_CLEAN'] = 'OTROS'

    # Encoding
    df_encoded = pd.get_dummies(df, columns=['SEXO', 'EST_CIVIL_CLEAN'], drop_first=True)

    # Alinear columnas con el modelo
    X = pd.DataFrame(0, index=range(len(df_encoded)), columns=model_cols, dtype=float)
    for col in model_cols:
        if col in df_encoded.columns:
            X[col] = df_encoded[col].values

    return X, df


# ============================================================
# INTERFAZ — TABS
# ============================================================
tab1, tab2 = st.tabs(["Evaluación Individual", "Evaluación de Lote (CSV)"])

# ============================================================
# TAB 1: EVALUACIÓN INDIVIDUAL
# ============================================================
with tab1:
    st.header("Evaluación de Cliente Individual")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Datos Financieros")
        saldo_raw = st.number_input("Saldo Total ($)", min_value=1.0, max_value=500000.0,
                                    value=5000.0, step=100.0)
        dias_mora = st.number_input("Días de Mora", min_value=0, max_value=3000, value=180)
        antiguedad = st.slider("Antigüedad (Meses)", 0, 200, 24)

    with col2:
        st.subheader("Datos del Cliente")
        edad = st.slider("Edad", 18, 90, 35)
        sexo = st.selectbox("Sexo", ["M", "F", "X"])
        civil = st.selectbox("Estado Civil",
                             ["SOLTERO", "CASADO", "DIVORCIADO", "UNION_LIBRE", "OTROS"])

    with col3:
        st.subheader("Historial de Contacto")
        recencia = st.slider("Meses sin pago", 0, 100, 6)
        score_contact = st.slider("Score Contactabilidad", 0.0, 6.0, 3.0, 0.5)
        ratio_cuota = st.number_input("Ratio Cuota/Saldo", min_value=0.0, max_value=1.0,
                                      value=0.02, step=0.01, format="%.3f")

    if st.button("CALCULAR VALUACIÓN", type="primary", use_container_width=True):
        input_data = preprocesar_cliente(saldo_raw, dias_mora, antiguedad, recencia,
                                         edad, sexo, civil, score_contact, ratio_cuota)

        prob = clf.predict_proba(input_data)[0, 1]
        monto = max(reg.predict(input_data)[0], 0)
        ev = prob * monto

        st.markdown("---")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Probabilidad de Pago", f"{prob:.1%}")
        c2.metric("Recuperación Estimada", f"${monto:,.2f}")
        c3.metric("Valor Esperado", f"${ev:,.2f}")
        c4.metric("ROI Estimado", f"{(ev / saldo_raw * 100):.1f}%")

        st.markdown("---")
        if ev > saldo_raw * 0.15:
            st.success("**OPORTUNIDAD DE COMPRA** — El valor esperado supera el 15% del saldo.")
        elif ev > saldo_raw * 0.05:
            st.warning("**EVALUAR** — Valor esperado moderado, requiere análisis adicional.")
        else:
            st.error("**RIESGO ALTO** — Valor esperado muy bajo respecto al saldo.")

# ============================================================
# TAB 2: EVALUACIÓN POR LOTE (CSV)
# ============================================================
with tab2:
    st.header("Evaluación Masiva de Cartera")
    st.markdown("""
    Suba los archivos CSV del nuevo lote para obtener la valuación completa.
    - **Saldo CSV:** Archivo con columnas `CUENTA`, `SALDO TOTAL`, `DIAS MORA`, etc.
    - **Detalles CSV (opcional):** Archivo con datos demográficos del deudor.
    """)

    col_up1, col_up2 = st.columns(2)
    with col_up1:
        file_saldo = st.file_uploader("Subir Saldo.csv", type=['csv'], key='saldo')
    with col_up2:
        file_detalles = st.file_uploader("Subir Detalles.csv (opcional)", type=['csv'],
                                          key='detalles')

    margen = st.slider("Margen de seguridad (%)", 10, 40, 20, 5) / 100

    if file_saldo is not None:
        if st.button("PROCESAR LOTE", type="primary", use_container_width=True):
            try:
                df_saldo_up = pd.read_csv(file_saldo, encoding='latin1')
                df_detalles_up = None
                if file_detalles is not None:
                    df_detalles_up = pd.read_csv(file_detalles, encoding='latin1')

                with st.spinner(f"Procesando {len(df_saldo_up):,} cuentas..."):
                    X_lote, df_original = preprocesar_lote(df_saldo_up, df_detalles_up)

                    # Predicciones
                    prob_pago = clf.predict_proba(X_lote)[:, 1]
                    monto_pred = np.maximum(reg.predict(X_lote), 0)
                    valor_esperado = prob_pago * monto_pred

                # Resultados
                st.markdown("---")
                st.subheader("Resultados de Valuación")

                valor_total = valor_esperado.sum()
                precio_compra = valor_total * (1 - margen)

                k1, k2, k3, k4 = st.columns(4)
                k1.metric("Cuentas Evaluadas", f"{len(X_lote):,}")
                k2.metric("Valor Total Estimado", f"${valor_total:,.0f}")
                k3.metric(f"Precio Sugerido ({(1-margen)*100:.0f}%)", f"${precio_compra:,.0f}")
                k4.metric("VE Promedio/Cuenta", f"${valor_total / len(X_lote):,.2f}")

                # Tabla de resultados
                df_resultado = pd.DataFrame({
                    'Probabilidad_Pago': (prob_pago * 100).round(1),
                    'Monto_Estimado': monto_pred.round(2),
                    'Valor_Esperado': valor_esperado.round(2)
                })

                if 'CUENTA' in df_original.columns:
                    df_resultado.insert(0, 'CUENTA', df_original['CUENTA'].values)
                if 'SALDO TOTAL' in df_original.columns:
                    df_resultado['Saldo'] = df_original['SALDO TOTAL'].values

                df_resultado = df_resultado.sort_values('Valor_Esperado', ascending=False)

                st.markdown("### Top 50 Cuentas con Mayor Valor Esperado")
                st.dataframe(df_resultado.head(50), use_container_width=True, hide_index=True)

                # Descargar resultados completos
                csv_result = df_resultado.to_csv(index=False)
                st.download_button(
                    "Descargar resultados completos (CSV)",
                    csv_result,
                    "valuacion_lote.csv",
                    "text/csv",
                    use_container_width=True
                )

            except Exception as e:
                st.error(f"Error procesando el lote: {e}")
                st.info("Verifique que los archivos CSV tengan el formato correcto.")

# ============================================================
# FOOTER
# ============================================================
st.sidebar.markdown("---")
st.sidebar.markdown("### Acerca del Modelo")
st.sidebar.markdown("""
**Arquitectura:** Hurdle Model (Dos Etapas)
- Etapa 1: GradientBoosting Classifier
- Etapa 2: GradientBoosting Regressor

**Predicción:** VE = P(pago) × Monto

**Grupo 4** — ML Supervisado UDB
""")
