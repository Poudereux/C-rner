# Daily stand-ups

Formato: fecha | asistentes | que hice | que hare | bloqueos.

## 2026-04-20 (Sprint 1, dia 1)
- Asistentes: Miguel, [companer@]
- Hicimos: kick-off, lectura del enunciado, seleccion de stack, creacion del repo, board de HUs en GitHub Projects.
- Hare: scaffolding del backend (FastAPI + SQLAlchemy), modelo Libro, primer test.
- Bloqueos: ninguno.

## 2026-04-21 (Sprint 1, dia 2)
- Asistentes: Miguel, [companer@]
- Hicimos: TDD HU-02 (registrar libro). Tests + servicio + repositorio + endpoint.
- Hare: HU-01 catalogo (incluyendo property `Libro.disponible`).
- Bloqueos: ninguno.

## 2026-04-22 (Sprint 1, dia 3)
- Asistentes: Miguel, [companer@]
- Hicimos: HU-01 + HU-03 (usuarios) con TDD. Excepcion personalizada `EmailDuplicadoError`.
- Hare: HU-04 prestamos. Anadir GitHub Actions.
- Bloqueos: dudas con dependency injection en FastAPI; resueltas en pair-programming.

## 2026-04-23 (Sprint 2, dia 1)
- Asistentes: Miguel, [companer@]
- Hicimos: HU-04 prestar + HU-05 devolver. CI verde.
- Hare: HU-06 historial + refactor a APIRouter por entidad.
- Bloqueos: ninguno.

## 2026-04-24 (Sprint 2, dia 2)
- Asistentes: Miguel, [companer@]
- Hicimos: HU-07 busqueda case-insensitive (`ilike`). Decorador `@log_call`.
- Hare: pulir frontend Streamlit + cache.
- Bloqueos: ninguno.

## 2026-04-25 (Sprint 3, dia 1)
- Asistentes: Miguel, [companer@]
- Hicimos: paginas Streamlit (catalogo, alta, usuarios, prestamo, devolucion, historial).
- Hare: HU-08 calendario y context manager para sesiones.
- Bloqueos: ninguno.

## 2026-04-26 (Sprint 3, dia 2)
- Asistentes: Miguel, [companer@]
- Hicimos: HU-08 con FullCalendar embebido. Generador `LibroRepository.stream()`.
- Hare: tests de integracion con TestClient + cobertura > 80%.
- Bloqueos: ninguno.

## 2026-04-27 (Sprint 3, dia 3 - cierre)
- Asistentes: Miguel, [companer@]
- Hicimos: tests de integracion (5 escenarios end-to-end), README final con SOLID documentado, DAILYS.md.
- Hare: entregar.
- Bloqueos: ninguno.
