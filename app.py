import re
import streamlit as st
from utils import generar_codigo_vih, validar_fecha_dd_mm_aaaa

st.set_page_config(page_title="Herramientas VIH", page_icon="🧪", layout="centered")

# ----------------------------- Utilidades UI -----------------------------
def header(titulo: str):
    col1, col2 = st.columns([1, 1])
    with col1:
        st.image("logo_gidil.png", use_column_width=True)
    with col2:
        st.image("logo_ssas.png", use_column_width=True)
    st.markdown(
        f"<h2 style='text-align:center; margin-top:0;'>{titulo}</h2>",
        unsafe_allow_html=True
    )

def auto_guiones_fecha(raw: str) -> str:
    """Inserta guiones automáticamente si vienen sin ellos."""
    digits = re.sub(r"\D", "", raw or "")
    if len(digits) >= 8:
        return f"{digits[:2]}-{digits[2:4]}-{digits[4:8]}"
    elif len(digits) >= 4:
        return f"{digits[:2]}-{digits[2:4]}"
    else:
        return digits

# ----------------------------- Sidebar: selector de página -----------------------------
pagina = st.sidebar.radio(
    "Páginas",
    ["Verificador Código VIH", "Flujo de Interpretación VIH"],
    index=0
)

# =============================================================================
# Página 1: Verificador Código VIH
# =============================================================================
if pagina == "Verificador Código VIH":
    header("VERIFICADOR DE CODIGO VIH")
    st.markdown(
        """
        <div style="text-align:center; color:#555; font-size:0.95rem;">
          Ingrese los datos exactamente como se solicita.
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---- Estado inicial de esta página ----
    defaults = {
        "primer_nombre": "",
        "primer_apellido": "",
        "segundo_apellido": "",
        "sin_segundo_apellido": False,
        "fecha_nac": "",
        "usuario_sin_run": False,
        "rut": "",
    }
    for k, v in defaults.items():
        st.session_state.setdefault(k, v)

    # ---- Formulario ----
    with st.form("form_vih"):
        # Fila: Primer nombre
        st.session_state["primer_nombre"] = st.text_input(
            "Primer nombre",
            value=st.session_state["primer_nombre"]
        ).strip()

        # Fila: Primer apellido
        st.session_state["primer_apellido"] = st.text_input(
            "Primer apellido",
            value=st.session_state["primer_apellido"]
        ).strip()

        # Fila: Segundo apellido + checkbox a la derecha
        c_left, c_right = st.columns([3, 1])
        with c_right:
            st.session_state["sin_segundo_apellido"] = st.checkbox(
                "No tiene segundo apellido",
                value=st.session_state["sin_segundo_apellido"]
            )
        with c_left:
            st.session_state["segundo_apellido"] = st.text_input(
                "Segundo apellido",
                value=st.session_state["segundo_apellido"],
                disabled=st.session_state["sin_segundo_apellido"]
            ).strip()

        # Fecha (autoguiones al enviar)
        st.session_state["fecha_nac"] = st.text_input(
            "Fecha de nacimiento (DD-MM-AAAA)",
            value=st.session_state["fecha_nac"],
            placeholder="28-03-2025",
        ).strip()

        st.markdown("---")

        # RUN a la izquierda y casilla "Usuario sin RUN" a la derecha
        cr_left, cr_right = st.columns([2, 1])
        with cr_right:
            st.session_state["usuario_sin_run"] = st.checkbox(
                "Usuario sin RUN",
                value=st.session_state["usuario_sin_run"],
                help="Si se marca, el código terminará en 'ABC-D' (literal fijo).",
            )
        with cr_left:
            st.session_state["rut"] = st.text_input(
                "RUN (con o sin puntos, con guion)",
                value=st.session_state["rut"],
                placeholder="12345678-9",
                disabled=st.session_state["usuario_sin_run"]
            ).strip()

        # Botones
        b1, b2 = st.columns([1, 1])
        submitted = b1.form_submit_button("Generar código")
        reset_clicked = b2.form_submit_button("Restablecer")

    # ---- Acciones ----
    if reset_clicked:
        for k, v in defaults.items():
            st.session_state[k] = v
        st.rerun()

    if submitted:
        # Reglas post-envío
        if st.session_state["sin_segundo_apellido"]:
            st.session_state["segundo_apellido"] = ""

        st.session_state["fecha_nac"] = auto_guiones_fecha(st.session_state["fecha_nac"])

        # Validaciones
        if not st.session_state["primer_nombre"] or not st.session_state["primer_apellido"] or (
            not st.session_state["sin_segundo_apellido"] and not st.session_state["segundo_apellido"]
        ):
            st.error("Complete nombre y apellidos.")
        elif not validar_fecha_dd_mm_aaaa(st.session_state["fecha_nac"]):
            st.error("Formato de fecha inválido. Use DD-MM-AAAA (solo números y guiones).")
        elif (not st.session_state["usuario_sin_run"]) and (not st.session_state["rut"]):
            st.error("Ingrese RUN o marque 'Usuario sin RUN'.")
        else:
            try:
                codigo = generar_codigo_vih(
                    primer_nombre=st.session_state["primer_nombre"],
                    primer_apellido=st.session_state["primer_apellido"],
                    segundo_apellido=st.session_state["segundo_apellido"],
                    sin_segundo_apellido=st.session_state["sin_segundo_apellido"],
                    fecha_nacimiento_dd_mm_aaaa=st.session_state["fecha_nac"],
                    usuario_sin_run=st.session_state["usuario_sin_run"],
                    rut=st.session_state["rut"],
                )
                st.markdown(
                    f"""
                    <div style="
                        font-size:2rem;
                        font-weight:800;
                        text-align:center;
                        letter-spacing:1px;
                        padding:14px 18px;
                        border:1px solid #e5e7eb;
                        border-radius:12px;
                        background:#f8fafc;
                        margin-top:6px;
                    ">{codigo}</div>
                    """,
                    unsafe_allow_html=True
                )
            except ValueError as e:
                st.error(str(e))

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:0.8rem; color:#666; text-align:center;'>"
        "Creada por Camilo Muñoz Cayún, Tecnólogo Médico, Hospital Villarrica, Agosto 2025"
        "</p>",
        unsafe_allow_html=True
    )

# =============================================================================
# Página 2: Flujo de Interpretación VIH (sin valores precargados)
# =============================================================================
else:
    header("🧬 Flujo de Interpretación de Resultados VIH")

    # Botón de reinicio solo para esta página
    if st.button("🔄 Reiniciar flujo"):
        for key in [
            "resultado_inicial_str", "repeticion1_str", "repeticion2_str",
            "confirmacion_isp", "prueba_identidad_str"
        ]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

    st.write("Ingrese el resultado cuantitativo inicial,  para iniciar el flujo de interpretación.")

    # Utilidad: parsear números desde un text_input (permite punto o coma)
    def get_float_from_text(label: str, key: str):
        s = st.text_input(label, value=st.session_state.get(key, ""), key=key, placeholder="").strip()
        if s == "":
            return None
        s2 = s.replace(",", ".")
        try:
            return float(s2)
        except ValueError:
            st.error(f"“{label}” debe ser numérico. Use punto o coma para decimales.")
            return None

    # Paso 1: Resultado cuantitativo inicial (en blanco por defecto)
    resultado_inicial = get_float_from_text("Resultado cuantitativo inicial", "resultado_inicial_str")

    if resultado_inicial is None:
        st.info("Ingrese el resultado inicial para continuar.")
    elif resultado_inicial < 1:
        st.success("Resultado cuantitativo: NO REACTIVO ✅. SE EMITE INFORME.")
    else:
        st.warning("Resultado inicial REACTIVO ⚠️. Ingrese las repeticiones:")

        # Paso 2: Repeticiones (también en blanco por defecto)
        repeticion1 = get_float_from_text("Repetición 1", "repeticion1_str")
        repeticion2 = get_float_from_text("Repetición 2", "repeticion2_str")

        # Avanzar solo cuando hay datos numéricos en ambas repeticiones
        if (repeticion1 is None) or (repeticion2 is None):
            st.info("Ingrese ambas repeticiones para evaluar el resultado cualitativo.")
        else:
            if repeticion1 < 1 and repeticion2 < 1:
                st.success("Resultado cualitativo: NO REACTIVO ✅. SE EMITE INFORME.")
            else:
                st.error("Resultado cualitativo: REACTIVO ⚠️")
                st.info("Se requiere confirmación ISP")

                # Paso 3: Confirmación ISP
                confirmacion_isp = st.selectbox(
                    "Resultado confirmación ISP",
                    ["Seleccionar", "Negativo", "Positivo"],
                    key="confirmacion_isp"
                )

                if confirmacion_isp == "Negativo":
                    st.success("Confirmación ISP: NEGATIVO ✅. SE EMITE INFORME.")
                elif confirmacion_isp == "Positivo":
                    st.warning("Confirmación ISP: POSITIVO ⚠️. Requiere prueba de identidad.")

                    # Paso 4: Prueba de identidad (en blanco por defecto)
                    prueba_identidad = get_float_from_text("Resultado prueba de identidad", "prueba_identidad_str")

                    if prueba_identidad is None:
                        st.info("Ingrese el valor de la prueba de identidad para continuar.")
                    else:
                        if prueba_identidad < 1:
                            st.warning("Resultado prueba de identidad: NO REACTIVO ⚠️. Revisar proceso, no emitir informe.")
                        else:
                            st.error("Resultado prueba de identidad: REACTIVO 🔴. Emitir informe.")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:0.8rem; color:#666; text-align:center;'>"
        "Creada por Camilo Muñoz Cayún, Tecnólogo Médico, Hospital Villarrica, Agosto 2025"
        "</p>",
        unsafe_allow_html=True
    )
