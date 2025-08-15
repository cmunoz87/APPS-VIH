
# Verificador de Código VIH (estructura plana)

App de Streamlit en **una sola carpeta** (sin subdirectorios).

## Archivos
```
app.py
utils.py
test_utils.py
logo_gidil.png
logo_ssas.png
requirements.txt
.gitignore
README.md
```

## Reglas implementadas
- Iniciales (ABC): 1ª letra de primer nombre, primer apellido y segundo apellido (o `#` si no tiene).
- Fecha: input `DD-MM-AAAA` (solo dígitos y `-`), se usa `DDMMAA` en el código.
- Con RUN: valida DV (mód. 11). Código: `ABC DDMMAA NNN-DV` (NNN: últimos 3 dígitos).
- Sin RUN: `ABC DDMMAA ABC-D` (literal fijo).
- Error en RUN: mensaje **"Error de RUN. Vuelva a ingresarlo."**

## Ejecutar
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy (Streamlit Cloud)
- Suba esta carpeta tal cual a un repo en GitHub y deploye `app.py` como entrypoint.
