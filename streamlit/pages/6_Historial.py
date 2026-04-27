"""HU-06: historial de prestamos de un usuario."""
import pandas as pd
import streamlit as st

from utils.api_client import ApiError, historial_usuario, listar_usuarios

st.set_page_config(page_title="Historial", page_icon="LIB")
st.title("Historial de prestamos")

try:
    usuarios = listar_usuarios()
except Exception as exc:
    st.error(f"Error al cargar usuarios: {exc}")
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
except ApiError as exc:
    st.error(f"Error: {exc.detail}")
    st.stop()
except Exception as exc:
    st.error(f"Error inesperado: {exc}")
    st.stop()

if not historial:
    st.info(f"{usuario['nombre']} aun no tiene historial de prestamos.")
    st.stop()

df = pd.DataFrame(historial)
df["estado"] = df["activo"].map({True: "Activo", False: "Devuelto"})
df["fecha_prestamo"] = pd.to_datetime(df["fecha_prestamo"]).dt.strftime("%Y-%m-%d")
df["fecha_devolucion"] = pd.to_datetime(df["fecha_devolucion"]).dt.strftime(
    "%Y-%m-%d"
)
df = df[
    ["id", "libro_titulo", "fecha_prestamo", "fecha_devolucion", "estado"]
]
df.columns = ["ID", "Libro", "Fecha prestamo", "Fecha devolucion", "Estado"]


def colorear_estado(valor: str) -> str:
    if valor == "Activo":
        return "background-color: #fff3cd"
    return "background-color: #d4edda"


styled = df.style.map(colorear_estado, subset=["Estado"])
st.dataframe(styled, use_container_width=True, hide_index=True)
st.caption(f"{len(df)} prestamos en total.")
