import streamlit as st

# 1. CONFIGURACIÓN DE PÁGINA (Esto ayuda con el nombre e icono)
st.set_page_config(
    page_title="RGP Pro",
    page_icon="👁️",
    layout="wide"
)

# Función para el cálculo de potencia corneal
def calcular_p_corneal(p_gafa, d_vertice):
    if d_vertice == 0: return p_gafa
    return p_gafa / (1 - (d_vertice / 1000) * p_gafa)

# --- DISEÑO DE LA APLICACIÓN ---
st.title("👁️ RGP Pro")
st.markdown("### Calculadora de Adaptación RGP")
st.write("---")

# 2. BARRA LATERAL: Rx DE GAFAS
with st.sidebar:
    st.header("👓 Rx de Gafas")
    esf_g = st.number_input("Esfera (D)", value=-3.00, step=0.25)
    cil_g = st.number_input("Cilindro (D)", value=-1.00, step=0.25)
    eje_g = st.number_input("Eje (°)", value=0, min_value=0, max_value=180, step=1)
    d_v = st.number_input("Dist. Vértice (mm)", value=12.0, step=1.0)

    # Cálculos de Poder Efectivo
    p1 = calcular_p_corneal(esf_g, d_v)
    p2 = calcular_p_corneal(esf_g + cil_g, d_v)
    
    esf_c = p1
    cil_c = p2 - p1

    st.divider()
    st.subheader("📍 Poder Corneal")
    st.success(f"**{esf_c:+.2f} {cil_c:+.2f} x {eje_g}°**")

# 3. CUERPO PRINCIPAL: QUERATOMETRÍA
st.header("1. Datos Queratométricos")
col1, col2 = st.columns(2)
with col1:
    k1 = st.number_input("K Plana (D)", value=43.00, step=0.25)
with col2:
    k2 = st.number_input("K Curva (D)", value=44.50, step=0.25)

astig_c = abs(k1 - k2)

# Lógica de Diámetro según K1
if k1 <= 43.00:
    filosofia = "ALINEAMIENTO APICAL"
    color_f = "green"
    opciones_diam = [9.2, 9.6]
else:
    filosofia = "LIBRAMIENTO APICAL"
    color_f = "blue"
    opciones_diam = [9.2]

st.markdown(f"**Filosofía Sugerida:** :{color_f}[{filosofia}]")
diam_sel = st.radio("Selecciona Diámetro (mm):", opciones_diam, horizontal=True)

# 4. CÁLCULO DE CURVA BASE (CB)
# Ajustes según astigmatismo (Regla simplificada)
if astig_c <= 3.50:
    if k1 > 43.00: # Libramiento
        ajuste = [-0.75, -0.50, -0.25, 0.00, 0.25][min(int(astig_c/0.75), 4)]
    else: # Alineamiento
        if diam_sel == 9.2:
            ajuste = [-0.50, -0.25, 0.00, 0.25, 0.50][min(int(astig_c/0.75), 4)]
        else: # 9.6
            ajuste = [-0.75, -0.50, -0.25, 0.00, 0.25][min(int(astig_c/0.75), 4)]
    cb_d = k1 + ajuste
else:
    st.warning("⚠️ Astigmatismo elevado. Usando criterio de K-media.")
    cb_d = (k1 + k2) / 2

# 5. RESULTADOS
st.divider()
st.header("2. Lente de Prueba Sugerido")
res1, res2, res3 = st.columns(3)

with res1:
    st.metric("Curva Base", f"{cb_d:.2f} D", f"{337.5/cb_d:.2f} mm")
with res2:
    st.metric("Poder", f"{esf_c:+.2f} D")
with res3:
    st.metric("Diámetro", f"{diam_sel} mm")

st.info(f"**ORDEN:** CB {337.5/cb_d:.2f}mm / PODER {esf_c:+.2f}D / Ø {diam_sel}mm")
