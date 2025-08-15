
import streamlit as st
from utils import (
    generar_iniciales,
    generar_codigo_vih,
    validar_run,
    validar_fecha_dd_mm_aaaa,
)

st.set_page_config(page_title="Verificador de Código VIH", page_icon="🧪", layout="centered")

# Encabezado con logos (en la misma carpeta)
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
      Ingrese los datos exactamente como se solicita. La fecha debe ser <b>DD-MM-AAAA</b> (solo dígitos y guiones).
    </div>
    """,
    unsafe_allow_html=True
)

with st.form("form_vih"):
    col_a, col_b = st.columns(2)
    with col_a:
        primer_nombre = st.text_input("Primer nombre", value="").strip()
        primer_apellido = st.text_input("Primer apellido", value="").strip()
    with col_b:
        sin_segundo_apellido = st.checkbox("No tiene segundo apellido", value=False)
        segundo_apellido = st.text_input("Segundo apellido", value="" if not sin_segundo_apellido else "", disabled=sin_segundo_apellido).strip()

    fecha_nac = st.text_input("Fecha de nacimiento (DD-MM-AAAA)", placeholder="28-03-2025").strip()

    st.markdown("---")
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        usuario_sin_run = st.checkbox("Usuario sin RUN", value=False, help="Si se marca, el código terminará en 'ABC-D' (literal fijo).")
    with col_r2:
        rut = st.text_input("RUN (con o sin puntos, con guion)", placeholder="16.823.628-K", disabled=usuario_sin_run).strip()

    submitted = st.form_submit_button("Generar código")

if submitted:
    # Validaciones mínimas
    if not primer_nombre or not primer_apellido or (not sin_segundo_apellido and not segundo_apellido):
        st.error("Complete nombre y apellidos.")
    elif not validar_fecha_dd_mm_aaaa(fecha_nac):
        st.error("Formato de fecha inválido. Use DD-MM-AAAA (solo números y guiones).")
    elif (not usuario_sin_run) and (not rut):
        st.error("Ingrese RUN o marque 'Usuario sin RUN'.")
    else:
        try:
            codigo = generar_codigo_vih(
                primer_nombre=primer_nombre,
                primer_apellido=primer_apellido,
                segundo_apellido=segundo_apellido,
                sin_segundo_apellido=sin_segundo_apellido,
                fecha_nacimiento_dd_mm_aaaa=fecha_nac,
                usuario_sin_run=usuario_sin_run,
                rut=rut,
            )
            st.success("Código generado correctamente:")
            st.code(codigo, language="text")
        except ValueError as e:
            st.error(str(e))

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "<p style='font-size:0.8rem; color:#666; text-align:center;'>"
    "Creada por Camilo Muñoz Cayún, Tecnólogo Médico, Hospital Villarrica, Agosto 2025"
    "</p>",
    unsafe_allow_html=True
)
