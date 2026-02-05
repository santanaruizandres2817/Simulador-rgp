import streamlit as st

# ESTO ES LO QUE EL CELULAR LEE PARA EL NOMBRE
st.set_page_config(
    page_title="RGP Pro", 
    page_icon="👁️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# El resto del código sigue igual...
def calcular_vertice_meridiano(potencia, dist_mm):
    if dist_mm == 0: return potencia
    return potencia / (1 - ((dist_mm / 1000) * potencia))

st.title("👁️ RGP Pro - Adaptación")
st.markdown("---")

with st.sidebar:
    st.header("⚙️ Cálculo de Poder Efectivo")
    esf = st.number_input("Esfera Gafa (D)", value=-5.00, step=0.25)
    cil = st.number_input("Cilindro Gafa (D)", value=-3.00, step=0.25)
    eje = st.number_input("Eje (°)", value=0, min_value=0, max_value=180, step=1)
    v_dist = st.number_input("Vértice (mm)", value=12.0, step=1.0)
    
    p1_ef = calcular_vertice_meridiano(esf, v_dist)
    p2_ef = calcular_vertice_meridiano(esf + cil, v_dist)
    
    esf_corneal = p1_ef
    cil_corneal = p2_ef - p1_ef
    
    st.divider()
    st.subheader("Resultado en Córnea:")
    st.success(f"**{esf_corneal:+.2f} {cil_corneal:+.2f} x {eje}°**")

st.header("1. Datos Queratométricos")
col1, col2 = st.columns(2)
with col1:
    k1 = st.number_input("K Plana (D)", value=43.50, step=0.25)
with col2:
    k2 = st.number_input("K Curva (D)", value=47.25, step=0.25)

astig_corneal = abs(k1 - k2)

if k1 <= 43.00:
    filo, color, diams = "ALINEAMIENTO APICAL", "green", [9.2, 9.6]
else:
    filo, color, diams = "LIBRAMIENTO APICAL", "blue", [9.2]

st.markdown(f"### Filosofía: :{color}[{filo}]")
diam = st.radio("Diámetro Seleccionado (mm)", diams, horizontal=True)

if astig_corneal <= 3.50:
    if k1 > 43.00:
        ajuste = [-0.75, -0.50, -0.25, 0.00, 0.25][min(int(astig_corneal/0.75), 4)]
    else:
        if diam == 9.2:
            ajuste = [-0.50, -0.25, 0.00, 0.25, 0.50][min(int(astig_corneal/0.75), 4)]
        else:
            ajuste = [-0.75, -0.50, -0.25, 0.00, 0.25][min(int(astig_corneal/0.75), 4)]
    cb_final = k1 + ajuste
else:
    st.warning("⚠️ Astigmatismo Elevado")
    crit = st.selectbox("Criterio:", ["Regular (25%)", "K Media", "Plana (50%)"])
    cb_final = k1 + (astig_corneal * 0.75) if "Reg" in crit else (k1+k2)/2 if "Med" in crit else k1 + (astig_corneal * 0.50)

st.divider()
c1, c2, c3 = st.columns(3)
c1.metric("Curva Base", f"{cb_final:.2f} D", f"{337.5/cb_final:.2f} mm")
c2.metric("Esfera Efectiva", f"{esf_corneal:+.2f} D")
c3.metric("Diámetro", f"{diam} mm")

st.info(f"**ORDEN:** CB {337.5/cb_final:.2f}mm / ESF {esf_corneal:+.2f}D / Ø {diam}mm")
