
import re
from datetime import datetime

# -------------------- Helpers --------------------

def _first_alpha_char(s: str) -> str:
    """Return first alphabetic character in the string (A-Z plus accented letters and Ñ)."""
    if s is None:
        return ""
    s = s.strip().upper()
    # Keep diacritics; accept unicode letters
    for ch in s:
        if ch.isalpha():
            return ch
    return ""

def generar_iniciales(primer_nombre: str, primer_apellido: str, segundo_apellido: str, sin_segundo_apellido: bool) -> str:
    """Genera las 3 iniciales ABC para el código.
    - Si no tiene segundo apellido (checkbox), usa '#'
    - Para apellidos/nombres compuestos, toma solo la primera letra alfabética
    - Mantiene tildes/Ñ (solo pasa a MAYÚSCULAS)
    """
    a = _first_alpha_char(primer_nombre)
    b = _first_alpha_char(primer_apellido)
    if sin_segundo_apellido:
        c = "#"
    else:
        c = _first_alpha_char(segundo_apellido)
        if c == "":  # si está vacío pero no marcaron el checkbox, aplicamos seguridad
            c = "#"
    return f"{a}{b}{c}"

def validar_fecha_dd_mm_aaaa(fecha: str) -> bool:
    """Valida formato DD-MM-AAAA y existencia de la fecha."""
    if not re.fullmatch(r"\d{2}-\d{2}-\d{4}", fecha or ""):
        return False
    d, m, y = fecha.split("-")
    try:
        datetime(int(y), int(m), int(d))
        return True
    except ValueError:
        return False

def fecha_a_ddmmaa(fecha: str) -> str:
    """Convierte 'DD-MM-AAAA' a 'DDMMAA'."""
    if not validar_fecha_dd_mm_aaaa(fecha):
        raise ValueError("Formato de fecha inválido. Use DD-MM-AAAA.")
    d, m, y = fecha.split("-")
    return f"{d}{m}{y[-2:]}"

def limpiar_rut(rut: str) -> str:
    """Elimina puntos y espacios, normaliza guion. Devuelve 'XXXXXXXX-DV' en mayúsculas."""
    rut = (rut or "").strip().upper().replace(".", "").replace(" ", "")
    rut = rut.replace("—", "-").replace("–", "-").replace("_", "-")
    return rut

def validar_run(rut: str) -> bool:
    """Valida RUT/RUN usando módulo 11. Acepta formatos con o sin puntos y con guion."""
    rut = limpiar_rut(rut)
    # Debe tener guion separando DV
    if not re.fullmatch(r"\d{1,8}-[0-9K]", rut):
        return False
    num, dv_ing = rut.split("-")
    # Cálculo DV
    factores = [2, 3, 4, 5, 6, 7]
    suma = 0
    for i, ch in enumerate(reversed(num)):
        suma += int(ch) * factores[i % len(factores)]
    resto = suma % 11
    dv_calc = 11 - resto
    if dv_calc == 11:
        dv_calc_char = "0"
    elif dv_calc == 10:
        dv_calc_char = "K"
    else:
        dv_calc_char = str(dv_calc)
    return dv_calc_char == dv_ing

def extraer_ultimos3(num_str: str) -> str:
    """Devuelve los últimos 3 dígitos del número, con padding a la izquierda si tiene menos de 3."""
    num_str = re.sub(r"\D", "", num_str or "")
    if not num_str:
        return ""
    return num_str[-3:].rjust(3, "0")

def formatear_run_para_codigo(rut: str) -> str:
    """De un RUT válido 'XXXXXXXX-DV' retorna 'NNN-DV' con NNN = últimos 3 dígitos del número."""
    rut = limpiar_rut(rut)
    if not validar_run(rut):
        raise ValueError("Error de RUN. Vuelva a ingresarlo.")
    num, dv = rut.split("-")
    return f"{extraer_ultimos3(num)}-{dv}"

# -------------------- Generador de código VIH --------------------

def generar_codigo_vih(
    primer_nombre: str,
    primer_apellido: str,
    segundo_apellido: str,
    sin_segundo_apellido: bool,
    fecha_nacimiento_dd_mm_aaaa: str,
    usuario_sin_run: bool,
    rut: str = None,
) -> str:
    """Genera el código VIH según las reglas acordadas.
    - Siempre usa: 'ABC DDMMAA ...'
    - Con RUN válido → 'ABC DDMMAA NNN-DV'
    - Sin RUN → 'ABC DDMMAA ABC-D' (ABC-D ES LITERAL FIJO)
    """
    iniciales = generar_iniciales(primer_nombre, primer_apellido, segundo_apellido, sin_segundo_apellido)
    # Fecha a DDMMAA
    ddmmaa = fecha_a_ddmmaa(fecha_nacimiento_dd_mm_aaaa)

    if usuario_sin_run:
        return f"{iniciales} {ddmmaa} ABC-D"

    # Con RUN → validar
    if not validar_run(rut or ""):
        raise ValueError("Error de RUN. Vuelva a ingresarlo.")
    sufijo_run = formatear_run_para_codigo(rut)
    return f"{iniciales} {ddmmaa} {sufijo_run}"
