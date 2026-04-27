"""HU-08: historial en formato calendario."""
import streamlit as st
import streamlit.components.v1 as components

from utils.api_client import ApiError, historial_usuario, listar_usuarios

st.set_page_config(page_title="Calendario", page_icon="LIB", layout="wide")
st.title("Calendario de prestamos")

try:
    usuarios = listar_usuarios()
except Exception as exc:
    st.error(f"Error al cargar usuarios: {exc}")
    st.stop()

if not usuarios:
    st.info("Aun no hay usuarios.")
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
    st.info(f"{usuario['nombre']} aun no tiene prestamos.")
    st.stop()


# Construimos eventos para FullCalendar.io
def evento(p: dict) -> dict:
    fin = p.get("fecha_devolucion") or p["fecha_prestamo"]
    return {
        "title": p["libro_titulo"],
        "start": p["fecha_prestamo"][:10],
        "end": fin[:10],
        "color": "#e0a800" if p["activo"] else "#28a745",
    }


eventos = [evento(p) for p in historial]
eventos_js = str(eventos).replace("'", '"').replace("True", "true").replace(
    "False", "false"
)

html = f"""
<link href='https://cdn.jsdelivr.net/npm/fullcalendar@6.1.11/index.global.min.css' rel='stylesheet' />
<script src='https://cdn.jsdelivr.net/npm/fullcalendar@6.1.11/index.global.min.js'></script>
<div id='calendario' style='max-width:900px;margin:0 auto;'></div>
<script>
document.addEventListener('DOMContentLoaded', function() {{
  var calendarEl = document.getElementById('calendario');
  var calendar = new FullCalendar.Calendar(calendarEl, {{
    initialView: 'dayGridMonth',
    locale: 'es',
    headerToolbar: {{
      left: 'prev,next today',
      center: 'title',
      right: 'dayGridMonth,timeGridWeek'
    }},
    events: {eventos_js}
  }});
  calendar.render();
}});
</script>
"""
components.html(html, height=700, scrolling=True)
st.caption("Naranja: prestamo activo. Verde: devuelto.")
