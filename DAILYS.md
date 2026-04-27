# Dailys

Stand-ups del grupo. Formato libre.
Equipo: Miguel Poudereux (lider), Ivan Alba, Alvaro de Celis, Gonzalo Carrasco.

---

### 2026-04-06 (Lunes - Sprint 1, dia 1)
Asistentes: los 4.
Hicimos kick-off. Leimos el enunciado entero en clase y decidimos el stack:
FastAPI + SQLAlchemy + Streamlit + Docker. Miguel propuso usar SQLite para
el sprint 1 y migrar a Postgres si daba tiempo (al final no dio).
Repartimos las HUs:
- Miguel + Ivan: backend (modelos, repos, services).
- Alvaro: frontend Streamlit.
- Gonzalo: tests + CI.
Hare manana: crear el repo en GitHub y subir el esqueleto.
Bloqueos: ninguno.

### 2026-04-07
Solo Miguel y Gonzalo (los demas tenian clase de SO a la misma hora).
Creamos el repo en GitHub (C-rner, ya estaba creado vacio de la primera
clase). Subimos el zip del enunciado y leimos la doc de microservicios.
Empezamos a hablar de SOLID y como aplicarlo. Miguel explico SRP y DIP
con un ejemplo del libro.
Hare: pensar la estructura de carpetas.

### 2026-04-08 (miercoles)
Asistentes: los 4.
Discusion larga sobre como organizar las carpetas. Al final:
fastapi/app/{routers,services,repositories,domain,schemas,database,core}.
Ivan al principio queria meter todo en un solo archivo pero Miguel
explico que asi se aplican mejor SRP/SOC. Ok.
Hicimos `git init` y primer commit (vacio practicamente).
Bloqueos: el .gitignore de Python no estaba, lo metimos del template
de GitHub.

### 2026-04-10 (Viernes)
Asistentes: los 4 (en clase de Programacion II).
Empezamos los modelos SQLAlchemy. Libro, Usuario, Prestamo. Discusion
sobre si usar @property para `disponible` o calcularlo en el servicio.
Miguel insistio en property y se quedo asi (al final fue buena idea).
Hare: TDD del LibroService.
Bloqueos: pip nos daba conflicto con pydantic 1 vs 2. Resuelto
fijando pydantic==2.7.1.

### 2026-04-12 (Domingo - cierre sprint 1)
Solo Miguel e Ivan (los demas con tema personal).
Cerramos sprint 1: tenemos modelos, repositorios y servicios de Libro
y Usuario funcionando. Tests basicos con mocks. Sin Streamlit aun.
Retrospectiva corta: bien la organizacion de carpetas, mal la velocidad
los primeros dias.

---

### 2026-04-13 (Lunes - Sprint 2)
Asistentes: los 4.
Empezamos HU-04 (prestamos) y HU-05 (devoluciones). El servicio de
prestamo es el mas dificil porque tiene que comprobar que el libro
existe, el usuario existe y que no este ya prestado. Cuatro paths
distintos, cuatro excepciones.
Hare manana: terminar prestamos.
Bloqueos: nos liamos con la relationship de SQLAlchemy
(Libro <-> Prestamo). Lo arreglamos con back_populates.

### 2026-04-14
Asistentes: los 4.
Tests del PrestamoService no pasaban. Resulta que el mock no estaba
devolviendo bien la lista de prestamos para el property `disponible`.
Pasamos como una hora liados hasta que Miguel se dio cuenta. Al final
inicializamos `libro.prestamos = []` en cada test.
Aprendizaje: leer bien los mensajes de error de pytest, no
solo el rojo.

### 2026-04-16 (jueves)
Solo Alvaro y Gonzalo (Miguel e Ivan en examen de algoritmos).
Alvaro empezo el frontend en Streamlit. Pagina de catalogo.
Gonzalo escribio el conftest.py y un par de tests del UsuarioService.
Bloqueos: streamlit no se conectaba al backend. Resulta que el
puerto era el correcto pero alvaro tenia otra cosa corriendo en 8000.
Lo descubrio reiniciando el portatil...

### 2026-04-17
Asistentes: los 4.
Pulimos el frontend. La pagina de prestamo era un lio porque
necesitaba listar libros disponibles Y usuarios. Hicimos un selectbox
para cada uno. Miguel propuso meter una funcion `format_func` para
mostrar "#1 - El Quijote (Cervantes)" en vez del id pelado, mucho
mejor.
Hare: tests de integracion (TestClient) y CI con GitHub Actions.

### 2026-04-19 (cierre sprint 2)
Asistentes: los 4.
Cierre sprint 2. Metas cumplidas: HU-01 a HU-05 funcionando,
Streamlit conectado, 24 tests pasando.
Pendiente para sprint 3: HU-06 historial, HU-07 busqueda, HU-08
calendario, mejorar logging y excepciones, CI verde.

---

### 2026-04-20 (sprint 3)
Asistentes: los 4.
HU-06 historial. Discusion sobre como mostrar prestamos activos vs
cerrados. Decidimos colorear las filas (verde devuelto, amarillo
activo). Miguel hizo la query de SQLAlchemy ordenando por
fecha_prestamo DESC, queda mas natural.
Bloqueos: pandas styler no me dejaba aplicar color por valor.
Lo solucionamos con `df.style.map`.

### 2026-04-21
Asistentes: los 4.
Trabajamos en parejas: Miguel+Ivan en README (anadiendo seccion de
autores y la tabla SOLID), Alvaro+Gonzalo en logging y excepciones
personalizadas.
Bloqueos: github actions nos daba un error raro al hacer push porque
el token no tenia el scope `workflow`. Tardamos un buen rato en
saber que era eso. Al final regeneramos el token con `repo` +
`workflow` y solucionado.

### 2026-04-22
Asistentes: los 4.
Pareja Miguel+Alvaro: refinamos el .gitignore (estaba muy basico).
Pareja Ivan+Gonzalo: HU-07 busqueda. Usamos `ilike` de SQLAlchemy
para que sea case-insensitive y parcial. Funciona perfecto.
Hicismos commit pero nos dimos cuenta que estabamos en una rama
mal. Tuvimos que hacer cherry-pick. Mucho lio.

### 2026-04-23
Asistentes: los 4.
Tests extra. Pareja Miguel+Gonzalo metiendo casos limite (titulo
con whitespace, busquedas con tabs). Ivan+Alvaro empezaron HU-08
calendario.
Bloqueos: github no nos iba bien por la mañana, tirabamos al
push y daba 500. Estuvo caido github como una hora. Esperamos.

### 2026-04-24
Asistentes: los 4.
Pareja Miguel+Ivan: refactor del cliente API en streamlit, subimos
el TTL del cache de 10 a 15s.
Pareja Alvaro+Gonzalo: terminaron HU-08 con FullCalendar embebido
via components.html. Quedo bonito.

### 2026-04-25
Asistentes: los 4 (sabado pero quedamos para tirar).
Pareja Miguel+Alvaro: badges en el README (python, tests, coverage).
Pareja Ivan+Gonzalo: tests de integracion con TestClient. Cobertura
subio a 92%.

### 2026-04-26
Asistentes: los 4.
Ultimo dia de desarrollo "normal".
Pareja Miguel+Gonzalo: pequenos fixes, mensaje al confirmar
devolucion mas claro.
Ivan y Alvaro repasaron docstrings y tipos.
CI verde en GitHub Actions.

### 2026-04-27 (hoy - preparacion entrega)
Asistentes: los 4.
Repaso final, preparamos demo y dailys. Miguel reviso el README
para asegurar que la tabla SOLID esta clara. Manana entregamos
y la semana que viene defendemos.

