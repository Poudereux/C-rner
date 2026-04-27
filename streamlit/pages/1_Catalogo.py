"""HU-01 + HU-07: catalogo de libros con buscador."""
import pandas as pd
import streamlit as st

from utils.api_client import ApiError, listar_libros

st.set_page_config(page_title="Catalogo", page_icon="LIB")
st.title("Catalogo de Libros")

texto = st.text_input(
    "Buscar por titulo o autor",
    placeholder="Ej: orwell, clean, pragmatic...",
)

try:
    libros = listar_libros(texto.strip() or None)
except ApiError as exc:
    st.error(f"Error al consultar el catalogo: {exc.detail}")
    st.stop()
except Exception as exc:
    st.error(
        f"No se ha podido conectar con la API en el puerto 8000.\n\n{exc}"
    )
    st.info("Asegurate de que el backend FastAPI este arrancado.")
    st.stop()

if not libros:
    if texto.strip():
        st.warning(f"No hay libros que coincidan con '{texto}'.")
    else:
        st.info("Aun no hay libros en el catalogo. Da de alta el primero.")
    st.stop()

df = pd.DataFrame(libros)
df["disponibilidad"] = df["disponible"].map(
    {True: "Disponible", False: "Prestado"}
)
df = df[["id", "titulo", "autor", "genero", "disponibilidad"]]
df.columns = ["ID", "Titulo", "Autor", "Genero", "Disponibilidad"]
st.dataframe(df, use_container_width=True, hide_index=True)
st.caption(f"{len(df)} libros mostrados.")
