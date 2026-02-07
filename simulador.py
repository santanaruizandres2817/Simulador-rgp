import streamlit as st

st.set_page_config(page_title="RGP-PRO", page_icon="👁️", layout="centered")

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
st.info("Ingresa los valores con su signo (+ o -)")
c1, c2, c3 = st.columns(3)
with c1:
    esfera_input = st.text_input("Esfera:", value="-4.00")
with c2:
    cilindro_input = st.text_input("Cilindro:", value="0.00")
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
        esf = float(esfera_input)
        cil = float(cilindro_input)
        dif_k = abs(k2 - k1)
        
        # REGLA CB: Si Astigmatismo > 3.50 -> K Media. Si no -> K Plana.
        if dif_k > 3.50:
            cb_final = (k1 + k2) / 2
            tipo_cb = "K MEDIA"
        else:
            cb_final = k1
            tipo_cb = "K PLANA"
        
        radio_mm = 337.5 / cb_final

        # PODER EFECTIVO (Vértice 12mm aplicado a Esfera y Cilindro)
        # Se calcula la potencia efectiva de cada componente para obtener la Rx en plano corneal
        esf_efectiva = esf / (1 - (0.012 * esf)) if esf != 0 else 0.0
        
        # El cilindro efectivo se saca calculando el vértice del poder total y restando la esfera efectiva
        poder_total_anteojo = esf + cil
        poder_total_efectivo = poder_total_anteojo / (1 - (0.012 * poder_total_anteojo)) if poder_total_anteojo != 0 else 0.0
        cil_efectivo = poder_total_efectivo - esf_efectiva

        # --- 5. RESULTADOS ---
        st.markdown(f"### {filosofia}")
        res1, res2 = st.columns(2)
        with res1:
            st.metric("Curva Base (CB)", f"{cb_final:.2f} D")
            st.write(f"**Radio:** {radio_mm:.2f} mm")
            st.caption(f"Basado en: {tipo_cb}")
        with res2:
            st.metric("Poder Efectivo (Esf)", f"{esf_efectiva:+.2f} D")
            st.write(f"**Cilindro Efectivo:** {cil_efectivo:+.2f} D")
            st.write(f"**Diámetro:** {diametro_final} mm")
            st.caption("Compensación de Vértice a 12mm")

        st.success(f"Cálculo para Rx: {esf:+.2f} {cil:+.2f} x {eje}°")
        
    except ValueError:
        st.error("Revisa el formato de los números y signos.")
