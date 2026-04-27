"""HU-02: registrar un nuevo libro."""
import streamlit as st

from utils.api_client import ApiError, crear_libro

st.set_page_config(page_title="Alta de libro", page_icon="LIB")
st.title("Registrar nuevo libro")

with st.form("alta_libro"):
    titulo = st.text_input("Titulo")
    autor = st.text_input("Autor")
    genero = st.text_input("Genero")
    enviar = st.form_submit_button("Registrar libro")

if enviar:
    if not (titulo.strip() and autor.strip() and genero.strip()):
        st.warning("Todos los campos son obligatorios.")
    else:
        try:
            libro = crear_libro(titulo, autor, genero)
            st.success(f"Libro '{libro['titulo']}' registrado con id {libro['id']}.")
        except ApiError as exc:
            st.error(f"No se ha podido registrar: {exc.detail}")
        except Exception as exc:
            st.error(f"Error inesperado: {exc}")
