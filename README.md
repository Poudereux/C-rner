# Practica Final: Gestor de Bibliotecas

![Python](https://img.shields.io/badge/python-3.11-blue) ![Tests](https://img.shields.io/badge/tests-32_passing-brightgreen) ![Coverage](https://img.shields.io/badge/coverage-92%25-brightgreen)

Sistema de gestion de catalogo y prestamos de una biblioteca.
Asignatura: Programacion II.

## Stack

| Capa | Tecnologia |
|------|-----------|
| Backend | FastAPI 0.111 + SQLAlchemy 2.x |
| Persistencia | SQLite (Postgres-ready via DATABASE_URL) |
| Frontend | Streamlit 1.38 |
| Tests | Pytest + pytest-cov (cobertura > 80%) |
| Contenedores | Docker + docker-compose |
| CI | GitHub Actions |

## Arquitectura (vista de alto nivel)

```
streamlit/  -- Frontend (paginas + cliente HTTP)
    |  HTTP REST
    v
fastapi/app/
    routers/     -- APIRouter (libros, usuarios, prestamos)
    services/    -- Logica de negocio (HUs)
    repositories/-- Acceso a datos (SQLAlchemy)
    domain/      -- Modelos + excepciones de dominio
    schemas/     -- DTOs Pydantic
    database/    -- Engine, sesion, context manager
    core/        -- Config, logging, decoradores
```

## Como aplicamos SOLID

| Principio | Donde |
|-----------|------|
| **SRP** (Single Responsibility) | Cada modulo tiene una responsabilidad: `routers/` solo serializa HTTP; `services/` solo aplica reglas de negocio; `repositories/` solo accede a la BD. |
| **OCP** (Open/Closed) | Para cambiar de SQLite a Postgres basta cambiar `DATABASE_URL`; los servicios no se tocan. Para anadir un repositorio en memoria solo hay que crear una clase nueva que cumpla el `Protocol`. |
| **LSP** (Liskov) | Cualquier implementacion concreta de los `*RepositoryProtocol` se puede sustituir sin romper nada. Los tests unitarios de servicios usan mocks que cumplen ese mismo contrato. |
| **ISP** (Interface Segregation) | Cada protocolo de repositorio expone solo los metodos que su consumidor necesita; `LibroRepositoryProtocol` no incluye operaciones de prestamo y viceversa. |
| **DIP** (Dependency Inversion) | Los servicios reciben sus repositorios por constructor (inyeccion). Los routers reciben los servicios via `Depends(...)` de FastAPI. Nadie hace `import` directo de SQLAlchemy fuera de `repositories/` y `database/`. |

## Buenas practicas Python aplicadas

- **Excepciones personalizadas tipadas** (`app/domain/exceptions.py`) que se mapean a codigos HTTP coherentes.
- **Logging** con tres niveles (INFO, WARNING, ERROR) configurado en `app/core/logging_config.py`.
- **Decoradores propios** (`@log_call` en `app/core/decorators.py`) usados en cada metodo de servicio.
- **Properties** (`@property`) en los modelos: `Libro.disponible`, `Prestamo.activo`, `Usuario.prestamos_activos`.
- **Context manager** (`session_scope()`) para abrir/cerrar/transaccionar sesiones de BD.
- **Generadores** (`LibroRepository.stream()`) con `yield` y `yield_per()` para procesar grandes catalogos sin cargarlos en memoria.
- **Cache** en Streamlit con `@st.cache_data(ttl=10)` en `utils/api_client.py`.

## Historias de usuario implementadas

| HU | Descripcion | Endpoint principal | Pagina Streamlit |
|----|------------|--------------------|-----------------|
| 01 | Consultar catalogo | `GET /libros/` | Catalogo |
| 02 | Registrar libro | `POST /libros/` | Alta de libro |
| 03 | Gestion de usuarios | `GET/POST /usuarios/` | Usuarios |
| 04 | Realizar prestamo | `POST /prestamos/` | Prestamo |
| 05 | Devolver libro | `POST /prestamos/{id}/devolver` | Devolucion |
| 06 | Historial de prestamos | `GET /prestamos/usuario/{id}/historial` | Historial |
| 07 | Buscar por titulo/autor | `GET /libros/?q=texto` | Catalogo (input de busqueda) |
| 08 | Calendario de prestamos | (reutiliza HU-06) | Calendario (FullCalendar.io) |

## Como ejecutar

### Opcion A: en local sin Docker (rapido)

```bash
# 1. Backend
cd fastapi
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload          # http://localhost:8000/docs

# 2. Frontend (en otro terminal)
cd ../streamlit
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run Library_App.py           # http://localhost:8501
```

### Opcion B: con docker-compose

```bash
docker compose up --build
# FastAPI: http://localhost:8000/docs
# Streamlit: http://localhost:8501
```

## Como ejecutar los tests

```bash
cd fastapi
pytest
```

El propio `pytest.ini` exige cobertura minima del 80%.

## Estado actual de tests

- 32 tests
- 92% de cobertura
- Tests unitarios con mocks (servicios), tests de repositorio (BD en memoria) y tests de integracion con `TestClient` de FastAPI.

## Metodologia XP

- **TDD**: ver carpeta `fastapi/tests/`. Los tests de servicio se escribieron antes que la implementacion (commits `test:` previos a `feat:`).
- **Pair programming**: registrado en commits con `Co-authored-by:`.
- **Integracion continua**: GitHub Actions corre los tests en cada push (`.github/workflows/ci.yml`).
- **Stand-ups diarios**: ver `DAILYS.md`.


## Autores

| Nombre | GitHub | Email |
|--------|--------|-------|
| Miguel Poudereux | @Poudereux | 9401312@alumnos.ufv.es |
| Ivan Alba | @ivaneguinoa | 9403674@alumnos.ufv.es |
| Alvaro de Celis | @alvarro1 | 9406189@alumnos.ufv.es |
| Gonzalo Carrasco | @GonzaloCarrascoBarros | 9405444@alumnos.ufv.es |
