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
if st.button("GENERAR PARÁMETROS DE PEDIDO", use_container_width=True):
    try:
        esf = float(esfera_input)
        cil = float(cilindro_input)
        dif_k = abs(k2 - k1)
        
        # REGLA PRIORITARIA: Si Astigmatismo > 3.50 -> K MEDIA
        if dif_k > 3.50:
            cb_final = (k1 + k2) / 2
            modo_nombre = "MODO K MEDIA"
            color_titulo = "#E67E22" 
        else:
            cb_final = k1
            color_titulo = "#2E86C1"
            if k1 <= 42.75:
                modo_nombre = "ALINEAMIENTO APICAL"
            else:
                modo_nombre = "LIBRAMIENTO APICAL"

        radio_mm = 337.5 / cb_final
        
        # CÁLCULO DE CPP ESTÁNDAR (0.4 mm)
        cpp_radio = radio_mm + 0.4

        # PODER EFECTIVO (Vértice 12mm para Esfera y Cilindro)
        esf_efectiva = esf / (1 - (0.012 * esf)) if esf != 0 else 0.0
        poder_total = esf + cil
        total_efectivo = poder_total / (1 - (0.012 * poder_total)) if poder_total != 0 else 0.0
        cil_efectivo = total_efectivo - esf_efectiva

        # --- 4. RESULTADOS ---
        st.markdown(f"<h2 style='text-align: center; color: {color_titulo};'>{modo_nombre}</h2>", unsafe_allow_html=True)
        
        # FICHA DE PEDIDO (Resaltada)
        st.success("### 📝 Ficha de Pedido al Laboratorio")
        f1, f2 = st.columns(2)
        with f1:
            st.write(f"**Curva Base (CB):** {radio_mm:.2f} mm ({cb_final:.2f} D)")
            st.write(f"**Poder:** {esf_efectiva:+.2f} D")
            st.write("**Diámetro Total (ØT):** 9.6 mm")
        with f2:
            st.write(f"**CPP (Radio):** {cpp_radio:.2f} mm")
            st.write(f"**Ancho de CPP:** 0.4 mm")
            st.write(f"**Vértice:** 12 mm")

        st.divider()
        st.subheader("Receta Complementaria (Plano Corneal):")
        st.info(f"Rx Efectiva: {esf_efectiva:+.2f} {cil_efectivo:+.2f} x {eje}°")
        
    except ValueError:
        st.error("Error: Revisa los valores de Rx (Esfera/Cilindro).")
