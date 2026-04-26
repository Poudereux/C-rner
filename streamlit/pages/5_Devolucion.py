"""HU-05: devolver un prestamo activo."""
import streamlit as st

from utils.api_client import (
    ApiError,
    devolver_prestamo,
    historial_usuario,
    listar_usuarios,
)

st.set_page_config(page_title="Devolucion", page_icon="LIB")
st.title("Registrar devolucion")

try:
    usuarios = listar_usuarios()
except Exception as exc:
    st.error(f"No se ha podido cargar la lista de usuarios: {exc}")
    st.stop()

if not usuarios:
    st.info("Aun no hay usuarios registrados.")
    st.stop()

usuario = st.selectbox(
    "Usuario",
    options=usuarios,
    format_func=lambda u: f"#{u['id']} - {u['nombre']}",
)

try:
    historial = historial_usuario(usuario["id"])
except Exception as exc:
    st.error(f"Error al consultar el historial: {exc}")
    st.stop()

activos = [p for p in historial if p["activo"]]

if not activos:
    st.info(f"{usuario['nombre']} no tiene prestamos activos.")
    st.stop()

with st.form("devolver"):
    prestamo = st.selectbox(
        "Prestamo activo",
        options=activos,
        format_func=lambda p: f"#{p['id']} - {p['libro_titulo']}",
    )
    enviar = st.form_submit_button("Registrar devolucion")

if enviar:
    try:
        devolver_prestamo(prestamo["id"])
        st.success(
            f"Devolucion registrada: '{prestamo['libro_titulo']}' (prestamo #{prestamo['id']})."
        )
        st.rerun()
    except ApiError as exc:
        st.error(f"No se ha podido devolver: {exc.detail}")
    except Exception as exc:
        st.error(f"Error inesperado: {exc}")
