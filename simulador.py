import streamlit as st
import math

def calcular_vertice_meridiano(potencia, dist_mm):
    if dist_mm == 0: return potencia
    return potencia / (1 - ((dist_mm / 1000) * potencia))

st.set_page_config(page_title="Calculador RGP Pro", page_icon="👁️", layout="wide")

st.title("👁️ Calculador de Adaptación RGP")
st.markdown("---")

# --- BARRA LATERAL: PODER EFECTIVO COMPLETO ---
with st.sidebar:
    st.header("Cálculo de Poder Efectivo (Rx)")
    esf = st.number_input("Esfera (D)", value=-3.00, step=0.25)
    cil = st.number_input("Cilindro (D)", value=-1.00, step=0.25)
    eje = st.number_input("Eje (°)", value=0, min_value=0, max_value=180, step=1)
    v_dist = st.number_input("Distancia Vértice (mm)", value=12.0, step=1.0)
    
    # Cálculo por meridiano
    # Meridiano 1 (Esfera)
    p1_gafa = esf
    p1_efectivo = calcular_vertice_meridiano(p1_gafa, v_dist)
    
    # Meridiano 2 (Esfera + Cilindro)
    p2_gafa = esf + cil
    p2_efectivo = calcular_vertice_meridiano(p2_gafa, v_dist)
    
    # Nueva Rx en plano corneal
    esf_final = p1_efectivo
    cil_final = p2_efectivo - p1_efectivo
    
    st.divider()
    st.subheader("Rx en Plano Corneal:")
    st.write(f"**{esf_final:+.2f} {cil_final:+.2f} x {eje}°**")
    st.caption("Este es el poder real que el ojo recibe en la superficie corneal.")

# --- CUERPO PRINCIPAL: QUERATOMETRÍA ---
col_k1, col_k2 = st.columns(2)
with col_k1:
    k1 = st.number_input("K Plana (D)", value=43.00, step=0.25)
with col_k2:
    k2 = st.number_input("K Curva (D)", value=44.00, step=0.25)

astig_corneal = abs(k1 - k2)

# --- FILOSOFÍA Y DIÁMETRO ---
if k1 <= 43.00:
    filosofia = "ALINEAMIENTO APICAL"
    color = "green"
    diams_disponibles = [9.2, 9.6]
else:
    filosofia = "LIBRAMIENTO APICAL"
    color = "blue"
    diams_disponibles = [9.2]

st.markdown(f"### Filosofía: :{color}[{filosofia}]")
diam = st.radio("Diámetro del Lente (mm)", diams_disponibles, horizontal=True)

# --- LÓGICA DE CÁLCULO DE CURVA BASE (CB) ---
if astig_corneal <= 3.50:
    if k1 > 43.00: # Libramiento
        if astig_corneal < 0.75: ajuste = -0.75
        elif astig_corneal < 1.50: ajuste = -0.50
        elif astig_corneal < 2.25: ajuste = -0.25
        elif astig_corneal < 3.00: ajuste = 0.00
        else: ajuste = 0.25
    else: # Alineamiento
        if diam == 9.2:
            if astig_corneal < 0.75: ajuste = -0.50
            elif astig_corneal < 1.50: ajuste = -0.25
            elif astig_corneal < 2.25: ajuste = 0.00
            elif astig_corneal < 3.00: ajuste = 0.25
            else: ajuste = 0.50
        else: # 9.6
            if astig_corneal < 0.75: ajuste = -0.75
            elif astig_corneal < 1.50: ajuste = -0.50
            elif astig_corneal < 2.25: ajuste = -0.25
            elif astig_corneal < 3.00: ajuste = 0.00
            else: ajuste = 0.25
    cb_final = k1 + ajuste
else:
    st.warning(f"⚠️ Astigmatismo Corneal Elevado ({astig_corneal:.2f} D)")
    criterio = st.selectbox("Criterio:", ["Regular (25%)", "Irregular (K Media)", "Plana (50%)"])
    if "Regular" in criterio: cb_final = k1 + (astig_corneal * 0.75)
    elif "Irregular" in criterio: cb_final = (k1 + k2) / 2
    else: cb_final = k1 + (astig_corneal * 0.50)

# --- RESULTADOS ---
st.divider()
res1, res2, res3 = st.columns(3)

with res1:
    st.metric("Curva Base", f"{cb_final:.2f} D")
    st.caption(f"Radio: {337.5/cb_final:.2f} mm")

with res2:
    st.metric("Esfera Efectiva", f"{esf_final:.2f} D")
    st.caption(f"Cil. Efectivo: {cil_final:.2f} D")

with res3:
    st.metric("Astig. Corneal", f"{astig_corneal:.2f} D")
    st.caption(f"Diámetro: {diam} mm")

st.success(f"**ORDEN SUGERIDA:** CB {337.5/cb_final:.2f}mm / PODER EFECTIVO {esf_final:.2f} {cil_final:.2f} x {eje}° / Ø {diam}mm")