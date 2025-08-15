import re
import streamlit as st
from utils import (
    generar_codigo_vih,
    validar_fecha_dd_mm_aaaa,
)

st.set_page_config(page_title="Verificador de Código VIH", page_icon="🧪", layout="centered")

# ---- Estado inicial ----
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

# ---- Utilidad: autoguiones de fecha al enviar ----
def auto_guiones_fecha(raw: str) -> str:
    digits = re.sub(r"\D", "", raw or "")
    if len(digits) >= 8:
        return f"{digits[:2]}-{digits[2:4]}-{digits[4:8]}"
    elif len(digits) >= 4:
        return f"{digits[:2]}-{digits[2:4]}"
    else:
        return digits

# ---- Encabezado con logos ----
col1, col2 = st.columns([1, 1])
with col1:
    st.image("logo_gidil.png", use_column_width=True)
with col2:
    st.image("logo_ssas.png", use_column_width=True)

st.markdown(
    "<h2 style='text-align:center; margin-top:0;'>VERIFICADOR DE CODIGO VIH</h2>",
    unsafe_allow_html=True
)
st.markdown(
    """
    <div style="text-align:center; color:#555; font-size:0.95rem;">
      Ingrese los datos exactamente como se solicita.
    </div>
    """,
    unsafe_allow_html=True
)

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

    # Fecha (los guiones se agregan automáticamente al enviar)
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
            placeholder="16.823.628-K",
            disabled=st.session_state["usuario_sin_run"]
        ).strip()

    # Botones: Generar y Restablecer
    b1, b2 = st.columns([1, 1])
    submitted = b1.form_submit_button("Generar código")
    reset_clicked = b2.form_submit_button("Restablecer")

# ---- Acciones de los botones ----
if reset_clicked:
    for k, v in defaults.items():
        st.session_state[k] = v
    st.rerun()

if submitted:
    # Forzar reglas post-envío dentro de la forma:
    if st.session_state["sin_segundo_apellido"]:
        st.session_state["segundo_apellido"] = ""

    # Auto-insertar guiones en fecha si vienen sin guiones
    st.session_state["fecha_nac"] = auto_guiones_fecha(st.session_state["fecha_nac"])

    # Validaciones mínimas
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
            # Mostrar código grande y en negrita
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

