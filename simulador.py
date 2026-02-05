import streamlit as st

# Configuración con ICONO (Emoji de ojo) y Nombre para el Celular
st.set_page_config(
    page_title="RGP Pro", 
    page_icon="👁️", 
    layout="wide"
)

def calcular_vertice_meridiano(potencia, dist_mm):
    if dist_mm == 0: return potencia
    return potencia / (1 - ((dist_mm / 1000) * potencia))

# Título de la App
st.title("👁️ RGP Pro - Adaptación")
st.markdown("---")

# --- BARRA LATERAL: PODER EFECTIVO ---
with st.sidebar:
    st.header("⚙️ Cálculo de Poder Efectivo")
    esf = st.number_input("Esfera Gafa (D)", value=-5.00, step=0.25)
    cil = st.number_input("Cilindro Gafa (D)", value=-3.00, step=0.25)
    eje = st.number_input("Eje (°)", value=0, min_value=0, max_value=180, step=1)
    v_dist = st.number_input("Vértice (mm)", value=12.0, step=1.0)
    
    # Cálculo por meridianos
    p1_ef = calcular_vertice_meridiano(esf, v_dist)
    p2_ef = calcular_vertice_meridiano(esf + cil, v_dist)
    
    esf_corneal = p1_ef
    cil_corneal = p2_ef - p1_ef
    
    st.divider()
    st.subheader("Resultado en Córnea:")
    st.success(f"**{esf_corneal:+.2f} {cil_corneal:+.2f} x {eje}°**")
    st.caption("Potencia real calculada en plano corneal.")

# --- CUERPO PRINCIPAL: QUERATOMETRÍA ---
st.header("1. Datos Queratométricos")
col1, col2 = st.columns(2)
with col1:
    k1 = st.number_input("K Plana (D)", value=43.50, step=0.25)
with col2:
    k2 = st.number_input("K Curva (D)", value=47.25, step=0.25)

astig_corneal = abs(k1 - k2)

# Lógica de Diámetro y Filosofía (Regla de 43.00 D)
if k1 <= 43.00:
    filo, color, diams = "ALINEAMIENTO APICAL", "green", [9.2, 9.6]
else:
    filo, color, diams = "LIBRAMIENTO APICAL", "blue", [9.2]

st.markdown(f"### Filosofía: :{color}[{filo}]")
diam = st.radio("Diámetro Seleccionado (mm)", diams, horizontal=True)

# --- CÁLCULO DE CURVA BASE (CB) ---
if astig_corneal <= 3.50:
    if k1 > 43.00: # Libramiento
        ajuste = [-0.75, -0.50, -0.25, 0.00, 0.25][min(int(astig_corneal/0.75), 4)]
    else: # Alineamiento
        if diam == 9.2:
            ajuste = [-0.50, -0.25, 0.00, 0.25, 0.50][min(int(astig_corneal/0.75), 4)]
        else: # Diámetro 9.6
            ajuste = [-0.75, -0.50, -0.25, 0.00, 0.25][min(int(astig_corneal/0.75), 4)]
    cb_final = k1 + ajuste
else:
    st.warning("⚠️ Astigmatismo Corneal Elevado")
    crit = st.selectbox("Criterio Especial:", ["Regular (25%)", "Irregular (K Media)", "Plana (50%)"])
    if "Regular" in crit: cb_final = k1 + (astig_corneal * 0.75)
    elif "Media" in crit: cb_final = (k1 + k2) / 2
    else: cb_final = k1 + (astig_corneal * 0.50)

# --- RESULTADOS FINALES ---
st.divider()
c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Curva Base", f"{cb_final:.2f} D")
    st.caption(f"Radio: {337.5/cb_final:.2f} mm")

with c2:
    st.metric("Poder Efectivo", f"{esf_corneal:+.2f} D")
    st.caption(f"Cil. Residual: {cil_corneal:+.2f} D")

with c3:
    st.metric("Astig. Corneal", f"{astig_corneal:.2f} D")
    st.caption(f"Ø Final: {diam} mm")

st.info(f"**ORDEN SUGERIDA:** CB {337.5/cb_final:.2f}mm / PODER {esf_corneal:+.2f}D / Ø {diam}mm")
