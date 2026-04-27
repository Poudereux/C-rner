"""HU-04: realizar un prestamo."""
import streamlit as st

from utils.api_client import (
    ApiError,
    crear_prestamo,
    listar_libros,
    listar_usuarios,
)

st.set_page_config(page_title="Prestamo", page_icon="LIB")
st.title("Realizar prestamo")

try:
    libros = listar_libros()
    usuarios = listar_usuarios()
except Exception as exc:
    st.error(f"No se ha podido cargar el formulario: {exc}")
    st.stop()

disponibles = [l for l in libros if l["disponible"]]

if not disponibles:
    st.warning("Ahora mismo no hay libros disponibles para prestar.")
    st.stop()
if not usuarios:
    st.warning("Primero registra al menos un usuario.")
    st.stop()

with st.form("prestar"):
    libro = st.selectbox(
        "Libro",
        options=disponibles,
        format_func=lambda l: f"#{l['id']} - {l['titulo']} ({l['autor']})",
    )
    usuario = st.selectbox(
        "Usuario",
        options=usuarios,
        format_func=lambda u: f"#{u['id']} - {u['nombre']} <{u['email']}>",
    )
    enviar = st.form_submit_button("Prestar")

if enviar:
    try:
        prestamo = crear_prestamo(libro["id"], usuario["id"])
        st.success(
            f"Prestamo #{prestamo['id']} registrado: "
            f"'{libro['titulo']}' a {usuario['nombre']}."
        )
        st.rerun()
    except ApiError as exc:
        st.error(f"No se ha podido prestar: {exc.detail}")
    except Exception as exc:
        st.error(f"Error inesperado: {exc}")
