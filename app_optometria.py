import streamlit as st

# Configuración de la pestaña
st.set_page_config(page_title="OptoApp Elite - FES Iztacala", layout="wide")

# --- ESTILOS CSS PROFESIONALES ---
st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    [data-testid="stSidebar"] { background-color: #003b5c; }
    [data-testid="stSidebar"] * { color: white !important; }
    .stButton>button {
        width: 100%; border-radius: 12px; height: 3.5em;
        background: linear-gradient(135deg, #003b5c 0%, #005689 100%);
        color: white; font-weight: bold; border: none; transition: 0.3s;
    }
    .stButton>button:hover {
        background: #d4af37; color: #003b5c; transform: translateY(-2px);
    }
    .card {
        background-color: white; padding: 25px; border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1); border-top: 6px solid #d4af37;
        margin-bottom: 20px; text-align: center;
    }
    .data-val { color: #003b5c; font-size: 2.5em; font-weight: bold; margin: 10px 0; }
    .instruction-card {
        background-color: #eef2f6; padding: 15px; border-radius: 10px;
        border-left: 5px solid #003b5c; margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE NAVEGACIÓN A PRUEBA DE FALLOS ---
if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = "Inicio"

def navegar(pagina):
    st.session_state.pagina_actual = pagina
    st.rerun()

# --- BARRA LATERAL (AHORA CON BOTONES) ---
with st.sidebar:
    st.title("🩺 OptoApp Pro")
    st.write("Menú de Navegación:")
    
    if st.button("🏠 Inicio"): navegar("Inicio")
    if st.button("🧪 1. Rígido Esférico"): navegar("1. Rígido Esférico")
    if st.button("🌀 2. Tórico Interno"): navegar("2. Tórico Interno")
    if st.button("👓 3. Blando Lumitoric"): navegar("3. Blando Lumitoric")
    if st.button("⚡ 4. Poder Efectivo"): navegar("4. Poder Efectivo")
    
    st.markdown("---")
    st.caption("Andrés | FES Iztacala UNAM")

# --- LÓGICA DE CONTENIDO ---

# 0. INICIO
if st.session_state.pagina_actual == "Inicio":
    st.title("💎 Panel de Control")
    st.write("Selecciona una calculadora para comenzar:")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Ir a Rígido Esférico 🧪"): navegar("1. Rígido Esférico")
        if st.button("Ir a Blando Lumitoric 👓"): navegar("3. Blando Lumitoric")
    with c2:
        if st.button("Ir a Tórico Interno 🌀"): navegar("2. Tórico Interno")
        if st.button("Ir a Poder Efectivo ⚡"): navegar("4. Poder Efectivo")

# 1. RÍGIDO ESFÉRICO
elif st.session_state.pagina_actual == "1. Rígido Esférico":
    st.title("🧪 Diseño Rígido Esférico")
    if st.button("⬅️ Volver al Panel"): navegar("Inicio")
    
    col1, col2 = st.columns(2)
    with col1:
        tipo = st.selectbox("Tipo de Córnea:", ["Regulares", "Irregulares"])
        kp = st.number_input("K Plana (D):", value=42.0, step=0.25)
    with col2:
        kc = st.number_input("K Curva (D):", value=43.0, step=0.25)
    
    dk = abs(kc - kp)
    cb_d = 0.0
    filo = ""
    
    if tipo == "Regulares":
        if dk > 3.5:
            filo = "Filosofía del 25%"
            cb_d = kp + (dk / 4)
        elif kp < 43:
            filo = "Filosofía de Alineamiento"
            if 0 <= dk <= 0.50: cb_d = kp - 0.50
            elif 0.75 <= dk <= 1.25: cb_d = kp - 0.25
            elif 1.50 <= dk <= 2.00: cb_d = kp
            elif 2.25 <= dk <= 2.75: cb_d = kp + 0.25
            elif 3.00 <= dk <= 3.50: cb_d = kp + 0.50
        else:
            filo = "Filosofía de Libramiento"
            if 0 <= dk <= 0.50: cb_d = kp
            elif 0.75 <= dk <= 1.25: cb_d = kp + 0.25
            elif 1.50 <= dk <= 2.00: cb_d = kp + 0.50
            elif 2.25 <= dk <= 2.75: cb_d = kp + 0.75
            elif 3.00 <= dk <= 3.50: cb_d = kp + 1.00
    else:
        if dk > 3.5:
            if kp < 41:
                filo = "Filosofía del 50%"
                cb_d = kp + (dk * 0.5)
            elif kp > 45:
                filo = "Filosofía del 30%"
                cb_d = kp + (dk * 0.3)
            else:
                st.error("K plana fuera de rango (41-45).")
        else:
            st.error("DK debe ser > 3.50 para Irregulares.")

    if cb_d != 0:
        mm = 337.5 / cb_d
        dia = 8.8 if mm < 7.5 else (9.2 if mm <= 8.2 else 9.6)
        html_rgp = "<div class='card'><h3>" + filo + "</h3><p class='data-val'>" + f"{mm:.2f}" + " mm</p><p>Diámetro: " + str(dia) + " mm</p></div>"
        st.markdown(html_rgp, unsafe_allow_html=True)

# 2. TÓRICO INTERNO
elif st.session_state.pagina_actual == "2. Tórico Interno":
    st.title("🌀 Diseño Tórico Interno")
    if st.button("⬅️ Volver al Panel"): navegar("Inicio")
    
    kp = st.number_input("K más plana (D):", value=42.0, step=0.25)
    kc = st.number_input("K más curva (D):", value=47.0, step=0.25)
    diam = st.slider("Diámetro del lente (mm):", 7.0, 12.0, 9.0, 0.5)
    
    dk = abs(kc - kp)
    if dk > 3.5:
        mm1_base = 337.5 / (kp + 0.62)
        mm2_base = 337.5 / (kc + ((2/3) * dk))
        ajuste = ((diam - 9.0) / 0.5) * 0.20
        
        t_curvas = f"{mm1_base + ajuste:.2f} / {mm2_base + ajuste:.2f} mm"
        t_ajuste = f"{ajuste:+.2f} mm"
        html_torico = "<div class='card'><h3>Curvas Base (Ø " + str(diam) + " mm)</h3><p class='data-val'>" + t_curvas + "</p><p>Ajuste aplicado: " + t_ajuste + "</p></div>"
        st.markdown(html_torico, unsafe_allow_html=True)
    else:
        st.error("Diferencia insuficiente (>3.50 D)")

# 3. BLANDO LUMITORIC
elif st.session_state.pagina_actual == "3. Blando Lumitoric":
    st.title("👓 Blando Lumitoric")
    if st.button("⬅️ Volver al Panel"): navegar("Inicio")
    
    st.markdown("<div class='instruction-card'>Cálculo de CB basado en promedio queratométrico. Diámetro estándar base: 15.00 mm.</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        k1 = st.number_input("K1 (D):", value=44.0, step=0.25)
    with col2:
        k2 = st.number_input("K2 (D):", value=45.0, step=0.25)
    
    diam = st.slider("Seleccionar Diámetro (mm):", 12.0, 16.0, 15.0, 0.5)
    prom = (k1 + k2) / 2
    
    if prom > 45.00:
        cb_base = 8.60
        rango_txt = "> 45.00 D"
    elif 43.12 <= prom <= 45.00:
        cb_base = 8.90
        rango_txt = "43.12 - 45.00 D"
    else:
        cb_base = 9.20
        rango_txt = "< 43.12 D"
    
    pasos = (diam - 15.0) / 0.5
    ajuste = pasos * 0.20
    cb_final = cb_base + ajuste
    
    val_final = f"{cb_final:.2f} mm"
    txt_ajuste = f"{ajuste:+.2f} mm"
    txt_cb = f"{cb_base:.2f}"
    txt_prom = f"{prom:.2f}"
    
    html_lumi = "<div class='card'><h3>Resultado Lumitoric</h3><p style='color: #666;'>Rango Promedio: <b>" + rango_txt + "</b> (Dió: " + txt_prom + " D)</p><p class='data-val'>" + val_final + "</p><p>CB Base obtenida: " + txt_cb + " | Ajuste por Ø " + str(diam) + " mm: " + txt_ajuste + "</p></div>"
    st.markdown(html_lumi, unsafe_allow_html=True)

# 4. PODER EFECTIVO
elif st.session_state.pagina_actual == "4. Poder Efectivo":
    st.title("⚡ Poder Efectivo")
    if st.button("⬅️ Volver al Panel"): navegar("Inicio")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        esf = st.number_input("Esfera:", value=-5.00, step=0.25)
    with col2:
        cil = st.number_input("Cilindro:", value=-1.00, step=0.25)
    with col3:
        eje = st.number_input("Eje:", value=180, step=1)
    
    m1, m2 = esf, esf + cil
    if abs(m1) < 4.0 and abs(m2) < 4.0:
        res = f"{esf:+.2f} {cil:+.2f} x {eje}°"
        st.warning("Poder menor a 4.00 D: No requiere compensación.")
    else:
        def f_eff(p):
            return 1/((1/p) - 0.012) if p != 0 else 0
        r1, r2 = f_eff(m1), f_eff(m2)
        n_esf = max(r1, r2)
        n_cil = min(r1, r2) - n_esf
        res = f"{round(n_esf*4)/4:+.2f} {round(n_cil*4)/4:+.2f} x {eje}°"
    
    html_poder = "<div class='card'><h3>Resultado</h3><p class='data-val'>" + res + "</p><p>Compensación a 12mm</p></div>"
    st.markdown(html_poder, unsafe_allow_html=True)