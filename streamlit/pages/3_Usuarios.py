"""HU-03: gestion de usuarios."""
import pandas as pd
import streamlit as st

from utils.api_client import ApiError, crear_usuario, listar_usuarios

st.set_page_config(page_title="Usuarios", page_icon="LIB")
st.title("Gestion de Usuarios")

st.subheader("Nuevo usuario")
with st.form("alta_usuario"):
    nombre = st.text_input("Nombre")
    email = st.text_input("Email")
    enviar = st.form_submit_button("Registrar usuario")

if enviar:
    if not (nombre.strip() and email.strip()):
        st.warning("Nombre y email son obligatorios.")
    else:
        try:
            usuario = crear_usuario(nombre, email)
            st.success(f"Usuario {usuario['nombre']} creado con id {usuario['id']}.")
        except ApiError as exc:
            st.error(f"No se ha podido registrar: {exc.detail}")
        except Exception as exc:
            st.error(f"Error inesperado: {exc}")

st.subheader("Usuarios registrados")
try:
    usuarios = listar_usuarios()
    if not usuarios:
        st.info("Aun no hay usuarios registrados.")
    else:
        df = pd.DataFrame(usuarios)
        df.columns = ["ID", "Nombre", "Email"]
        st.dataframe(df, use_container_width=True, hide_index=True)
except ApiError as exc:
    st.error(f"Error al listar usuarios: {exc.detail}")
except Exception as exc:
    st.error(f"Error de conexion: {exc}")
