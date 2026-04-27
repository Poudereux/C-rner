"""Pagina principal de la aplicacion Streamlit."""
import streamlit as st

st.set_page_config(
    page_title="Gestor de Bibliotecas",
    layout="wide",
    page_icon="LIB",
)

st.title("Gestor de Bibliotecas")

st.markdown(
    """
Bienvenido al sistema de gestion de la biblioteca.

Selecciona una pagina en el menu lateral:

* Catalogo: ver y buscar libros (HU-01, HU-07).
* Alta de libro: registrar un libro nuevo (HU-02).
* Usuarios: registrar y consultar usuarios (HU-03).
* Prestamo: prestar un libro a un usuario (HU-04).
* Devolucion: devolver un prestamo activo (HU-05).
* Historial: ver el historial de prestamos de un usuario (HU-06).
* Calendario: ver el historial en formato calendario (HU-08).
"""
)

st.sidebar.success("Selecciona una pagina arriba.")
