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

# --- 3. LÓGICA DE CÁLCULO ---
if st.button("CALCULAR LENTE", use_container_width=True):
    try:
        esf = float(esfera_input)
        cil = float(cilindro_input)
        dif_k = abs(k2 - k1)
        
        # REGLA PRIORITARIA: Si Astigmatismo > 3.50 -> SIEMPRE K MEDIA
        if dif_k > 3.50:
            cb_final = (k1 + k2) / 2
            modo_nombre = "K MEDIA"
            color_alerta = "orange"
            diametro_final = 9.6 # Diámetro fijo para córneas con alto astigmatismo
        else:
            # Si es menor a 3.50, usamos la filosofía por valor de K1
            if k1 <= 42.75:
                modo_nombre = "ALINEAMIENTO APICAL"
                color_alerta = "blue"
                diametro_final = 9.6 # Por defecto 9.6
            else:
                modo_nombre = "LIBRAMIENTO APICAL"
                color_alerta = "green"
                diametro_final = 9.6

        radio_mm = 337.5 / cb_final

        # PODER EFECTIVO (Vértice 12mm aplicado a Esfera y Cilindro por separado)
        esf_efectiva = esf / (1 - (0.012 * esf)) if esf != 0 else 0.0
        poder_total_anteojo = esf + cil
        poder_total_efectivo = poder_total_anteojo / (1 - (0.012 * poder_total_anteojo)) if poder_total_anteojo != 0 else 0.0
        cil_efectivo = poder_total_efectivo - esf_efectiva

        # --- 4. RESULTADOS ---
        st.markdown(f"<h2 style='text-align: center; color: {color_alerta};'>{modo_nombre}</h2>", unsafe_allow_html=True)
        
        res1, res2 = st.columns(2)
        with res1:
            st.metric("Curva Base (CB)", f"{cb_final:.2f} D")
            st.write(f"**Radio:** {radio_mm:.2f} mm")
        with res2:
            st.metric("Poder Efectivo (Esf)", f"{esf_efectiva:+.2f} D")
            st.write(f"**Cilindro Efectivo:** {cil_efectivo:+.2f} D")
            st.write(f"**Diámetro:** {diametro_final} mm")

        st.success(f"Cálculo para Rx: {esf:+.2f} {cil:+.2f} x {eje}°")
        st.caption(f"Diferencia queratométrica: {dif_k:.2f} D. Distancia al vértice: 12mm.")
        
    except ValueError:
        st.error("Revisa el formato de los números y signos.")
