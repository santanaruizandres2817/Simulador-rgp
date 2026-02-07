import streamlit as st

# Configuración de la interfaz
st.set_page_config(page_title="RGP-PRO", page_icon="👁️", layout="centered")

# Título
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
# Se usa min_value=None para permitir el signo menos (-) en el celular
st.subheader("Refracción (Rx):")
c1, c2, c3 = st.columns(3)
with c1:
    esfera = st.number_input("Esfera", value=0.0, step=0.25, format="%.2f", min_value=None)
with c2:
    cilindro = st.number_input("Cilindro", value=0.0, step=0.25, format="%.2f", min_value=None)
with c3:
    eje = st.number_input("Eje", min_value=0, max_value=180, value=0, step=1)

st.divider()

# --- 3. LÓGICA DE FILOSOFÍA Y DIÁMETRO ---
# REGLA: Hasta 42.75 es Alineamiento. A partir de 43.00 es Libramiento.
if k1 <= 42.75:
    filosofia = "ALINEAMIENTO APICAL"
    st.info(f"Modo: {filosofia}")
    # En Alineamiento se puede elegir entre 9.2 y 9.6
    diametro_final = st.radio("Diámetro Sugerido:", [9.2, 9.6], index=1, horizontal=True)
else:
    filosofia = "LIBRAMIENTO APICAL"
    st.warning(f"Modo: {filosofia}")
    # En Libramiento es fijo 9.6
    st.write("Diámetro fijado automáticamente en **9.6 mm**")
    diametro_final = 9.6

# --- 4. CÁLCULOS ---
if st.button("CALCULAR LENTE", use_container_width=True):
    # Astigmatismo corneal
    astig_corneal = abs(k2 - k1)
    ajuste = 0.0
    
    # REGLA: Solo se ajusta si la diferencia es mayor a 3.50 D
    if astig_corneal > 3.50:
        if "Irregular" in tipo_cornea:
            ajuste = astig_corneal * 0.50  # 50% para irregulares
        else:
            ajuste = astig_corneal * 0.25  # 25% para regulares
    
    cb_dioptrias = k1 + ajuste
    radio_mm = 337.5 / cb_dioptrias

    # Poder del Lente: Se toma la esfera directamente
    poder_lente = esfera

    # --- 5. RESULTADOS ---
    st.markdown(f"## {filosofia}")
    
    res1, res2 = st.columns(2)
    with res1:
        st.metric("Curva Base (CB)", f"{cb_dioptrias:.2f} D")
        st.write(f"**Radio:** {radio_mm:.2f} mm")
    with res2:
        st.metric("Poder del Lente", f"{poder_lente:+.2f} D")
        st.write(f"**Diámetro:** {diametro_final} mm")

    st.success(f"Adaptación lista para Rx: {esfera:+.2f} {cilindro:+.2f} x {eje}°")
