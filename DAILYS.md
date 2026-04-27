# Dailys

Stand-ups del grupo. Formato libre.
Equipo: Miguel Poudereux (lider), Ivan Alba, Alvaro de Celis, Gonzalo Carrasco.

---

### 2026-04-06 
Leimos el enunciado entero y decidimos el stack:
FastAPI + SQLAlchemy + Streamlit + Docker. Miguel propuso usar SQLite para
el sprint 1 y migrar a Postgres si daba tiempo (al final no dio).
Repartimos las HUs:
- Miguel + Ivan: backend (modelos, repos, services).
- Alvaro: frontend Streamlit.
- Gonzalo: tests + CI.
Creamos el repo en GitHub (C-rner, ya estaba creado vacio de la primera
clase). Subimos el zip del enunciado y leimos la doc de microservicios.
Empezamos a hablar de SOLID y como aplicarlo.

### 2026-04-08 
Discusion larga sobre como organizar las carpetas. Al final:
fastapi/app/{routers,services,repositories,domain,schemas,database,core}.
Hicimos `git init` y primer commit.
Empezamos los modelos SQLAlchemy. Libro, Usuario, Prestamo.

### 2026-04-09
Cerramos sprint 1: tenemos modelos, repositorios y servicios de Libro
y Usuario funcionando. Tests basicos con mocks. Sin Streamlit aun.

---

### 2026-04-14

Empezamos HU-04 (prestamos) y HU-05 (devoluciones). El servicio de
prestamo es el mas dificil porque tiene que comprobar que el libro
existe, el usuario existe y que no este ya prestado. Cuatro paths
distintos, cuatro excepciones.
Bloqueos: nos liamos con la relationship de SQLAlchemy
(Libro <-> Prestamo).

### 2026-04-16 
Empezamos el frontend en Streamlit. Pagina de catalogo.
Escribimos el conftest.py y un par de tests del UsuarioService.
Pulimos el frontend. La pagina de prestamo era un lio porque
necesitaba listar libros disponibles Y usuarios. Hicimos un selectbox
para cada uno.

### 2026-04-19
Cierre sprint 2. Metas cumplidas: HU-01 a HU-05 funcionando,
Streamlit conectado, 24 tests pasando.
Pendiente para sprint 3: HU-06 historial, HU-07 busqueda, HU-08
calendario, mejorar logging y excepciones, CI verde.

---

### 2026-04-20 
HU-06 historial. Discusion sobre como mostrar prestamos activos vs
cerrados. Decidimos colorear las filas. Hicimos la query de SQLAlchemy ordenando por
fecha_prestamo DESC, queda mas natural.
Trabajamos en parejas: Miguel+Ivan en README, Alvaro+Gonzalo en logging y excepciones
personalizadas.
Bloqueos: github actions nos daba un error raro al hacer push porque
el token no tenia el scope `workflow`. Tardamos un buen rato en
saber que era eso. Al final regeneramos el token con `repo` +
`workflow` y solucionado.

### 2026-04-22
Pareja Miguel+Alvaro: refinamos el .gitignore (estaba muy basico).
Pareja Ivan+Gonzalo: HU-07 busqueda. Usamos `ilike` de SQLAlchemy
para que sea case-insensitive y parcial.
Hicismos commit pero nos dimos cuenta que estabamos en una rama
mal. Tuvimos que hacer cherry-pick.

### 2026-04-23
Tests extra. Pareja Miguel+Gonzalo metiendo casos limite (titulo
con whitespace, busquedas con tabs). Ivan+Alvaro empezaron HU-08
calendario.

### 2026-04-24
Pareja Miguel+Ivan: refactor del cliente API en streamlit, subimos
el TTL del cache de 10 a 15s.
Pareja Alvaro+Gonzalo: terminaron HU-08 con FullCalendar embebido
via components.html.

### 2026-04-25
Pareja Miguel+Alvaro: badges en el README (python, tests, coverage).
Pareja Ivan+Gonzalo: tests de integracion con TestClient. Cobertura
subio a 92%.
Pequeños fixes, mensaje al confirmar
devolucion mas claro.
Repasamos docstrings y tipos.
CI verde en GitHub Actions.

### 2026-04-27 
Repaso final, preparamos demo y dailys. Miguel reviso el README
para asegurar que la tabla SOLID esta clara. Manana entregamos
y la semana que viene defendemos.

