import streamlit as st

# Configuración de la interfaz para celulares
st.set_page_config(page_title="RGP-PRO", page_icon="👁️", layout="centered")

# Título de la App
st.markdown("<h1 style='text-align: center; color: #2E86C1;'>👁️ RGP-PRO</h1>", unsafe_allow_html=True)
st.divider()

# --- 1. DATOS QUERATOMÉTRICOS ---
st.subheader("Queratometría")
col_k1, col_k2 = st.columns(2)

with col_k1:
    k1 = st.number_input("K1 (Plana) en D:", value=42.75, step=0.25, format="%.2f")
with col_k2:
    k2 = st.number_input("K2 (Curva) en D:", value=44.00, step=0.25, format="%.2f")

tipo_cornea = st.selectbox("Tipo de Córnea:", ["Regular", "Irregular (Plana/Curva)"])

# --- 2. REFRACCIÓN (Rx) ---
# Se usa min_value=None para que el celular permita borrar el 0 y poner el signo (-)
st.subheader("Refracción (Rx):")
c1, c2, c3 = st.columns(3)
with c1:
    esfera = st.number_input("Esfera", value=0.0, step=0.25, format="%.2f", min
