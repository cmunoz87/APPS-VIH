
import pytest
from utils import generar_iniciales, validar_run, fecha_a_ddmmaa, generar_codigo_vih

def test_iniciales_basico():
    assert generar_iniciales("Camilo", "Muñoz", "Cayun", False) == "CMC"

def test_iniciales_sin_segundo_apellido():
    assert generar_iniciales("Camilo", "Muñoz", "", True) == "CM#"

def test_fecha_ddmmaa():
    from utils import fecha_a_ddmmaa
    assert fecha_a_ddmmaa("08-09-1987") == "080987"

def test_validar_run_valido():
    assert validar_run("16.823.628-K") is True

def test_generar_codigo_con_run():
    out = generar_codigo_vih("Camilo", "Muñoz", "Cayun", False, "08-09-1987", False, "16.823.628-K")
    assert out == "CMC 080987 628-K"

def test_generar_codigo_sin_run():
    out = generar_codigo_vih("Camilo", "Muñoz", "Cayun", False, "08-09-1987", True, None)
    assert out == "CMC 080987 ABC-D"

def test_generar_codigo_sin_seg_ap_y_sin_run():
    out = generar_codigo_vih("Camilo", "Muñoz", "", True, "08-09-1987", True, None)
    assert out == "CM# 080987 ABC-D"
