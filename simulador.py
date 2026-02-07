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

# --- 2. REFRACCIÓN (Rx) ---
st.subheader("Refracción (Rx):")
st.info("Escribe el signo (+ o -) seguido del valor (ej: -4.25)")
c1, c2, c3 = st.columns(3)

with c1:
    # Usamos text_input para que el teclado del celular muestre los signos libremente
    esfera_txt = st.text_input("Esfera:", value="0.00")
with c2:
    cilindro_txt = st.text_input("Cilindro:", value="0.00")
with c3:
    eje = st.number_input("Eje:", min_value=0, max_value=180, value=0, step=1)

st.divider()

# --- 3. LÓGICA DE FILOSOFÍA Y DIÁMETRO ---
if k1 <= 42.75:
    filosofia = "ALINEAMIENTO APICAL"
    st.info(f"Modo: {filosofia}")
    diametro_final = st.radio("Diámetro Sugerido:", [9.2, 9.6], index=1, horizontal=True)
else:
    filosofia = "LIBRAMIENTO APICAL"
    st.warning(f"Modo: {filosofia}")
    st.write("Diámetro fijado automáticamente en **9.6 mm**")
    diametro_final = 9.6

# --- 4. CÁLCULOS ---
if st.button("CALCULAR LENTE", use_container_width=True):
    try:
        # Convertimos los textos de Rx a números flotantes
        esfera = float(esfera_txt)
        cilindro = float(cilindro_txt)
        
        dif_k = abs(k2 - k1)
        
        # REGLA: Si la diferencia > 3.50 D, se usa K Media.
        if dif_k > 3.50:
            cb_dioptrias = (k1 + k2) / 2
            mensaje_ajuste = f"Ajuste: K Media (Astig. {dif_k:.2f} D)."
        else:
            cb_dioptrias = k1
            mensaje_ajuste = "Calculado sobre K plana."
        
        radio_mm = 337.5 / cb_dioptrias

        # PODER EFECTIVO (Equivalente Esférico + Vértice 12mm)
        ee = esfera + (cilindro / 2)
        if ee != 0:
            poder_efectivo = ee / (1 - (0.012 * ee))
        else:
            poder_efectivo = 0.0

        # --- 5. RESULTADOS ---
        st.markdown(f"## {filosofia}")
        res1, res2 = st.columns(2)
        with res1:
            st.metric("Curva Base (CB)", f"{cb_dioptrias:.2f} D")
            st.write(f"**Radio:** {radio_mm:.2f} mm")
        with res2:
            st.metric("Poder Efectivo (EE)", f"{poder_efectivo:+.2f} D")
            st.write(f"**Diámetro:** {diametro_final} mm")

        st.success(f"Rx procesada: {esfera:+.2f} {cilindro:+.2f} x {eje}°")
        st.caption(mensaje_ajuste)
        st.caption("Poder basado en Eq. Esférico compensado a 12mm.")
        
    except ValueError:
        st.error("Por favor, introduce valores numéricos válidos en la Esfera y Cilindro (ej: -3.50)")

