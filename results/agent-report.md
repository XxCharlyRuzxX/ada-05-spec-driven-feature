# Agent Report

## Agent / Version
- **Agent**: Antigravity CLI (agy)
- **Model**: Gemini 3.8 Flash (High)
- **Environment**: macOS, Python 3.12.3, pytest 9.1.1, FastAPI 0.139.2, Pydantic 2.13.4, HTTPX 0.28.1

## Initial Context
El proyecto inició con un repositorio local recién inicializado (commit `6bde0a4`) que contenía exclusivamente los artefactos de especificación y gobernanza: `REQUIREMENTS.md`, `SPEC.md`, `ARCHITECTURE.md`, `TASKS.md` y `AGENTS.md`. No existían archivos de código fuente (`src/`), de pruebas (`tests/`) ni configuración de dependencias (`requirements.txt` o `pyproject.toml`).

La meta consistió en implementar la funcionalidad de **Customer Search** (búsqueda de clientes por coincidencia de subcadena insensible a mayúsculas/minúsculas en nombre y correo electrónico) respetando estrictamente el flujo Spec-Driven Development, sin añadir dependencias no justificadas ni alterar las reglas de negocio descritas en la especificación.

## Task Sequence

### T-01: Project setup
- **Acción del Agente**:
  - Creó `requirements.txt` declarando las dependencias esenciales: `fastapi`, `uvicorn`, `pydantic`, `pytest`, `httpx`.
  - Inicializó los paquetes base mediante `src/__init__.py` y `tests/__init__.py`.
- **Revisión Humana**:
  - Se constató que las versiones instaladas en el entorno satisfacían los requisitos sin conflictos.
- **Estado de Tests**:
  - `pytest -v` ejecutado: 0 tests recolectados sin errores de importación (código de salida esperado según criterio de verificación).

### T-02: Domain model and schemas
- **Acción del Agente**:
  - Creó `src/schemas/customer.py` y `src/schemas/__init__.py`.
  - Definió el modelo `Customer` con validaciones de tipo Pydantic (`id`, `name`, `email: EmailStr`, `is_active: bool = True`), `CustomerResponse` y `ErrorResponse`.
  - Añadió pruebas unitarias de validación en `tests/test_customer_service.py`.
- **Revisión Humana**:
  - Se verificó que los atributos y tipos coincidieran con el modelo de dominio en `SPEC.md`.
- **Estado de Tests**:
  - `pytest -v`: 7 tests pasaron exitosamente.

### T-03: Repository and seed data
- **Acción del Agente**:
  - Creó `src/repositories/customer_repository.py` y `src/repositories/__init__.py`.
  - Inicializó `CustomerRepository` con datos semilla representativos (`SEED_CUSTOMERS`), soportando inyección de datos para aislamiento de pruebas unitarias.
  - Añadió pruebas unitarias en `tests/test_customer_service.py` comprobando la recuperación de registros y la inyección de datos mock.
- **Revisión Humana**:
  - Se verificó que la semilla incluyera registros con coincidencias en nombre ("John Doe", "Jane Doe"), correo electrónico ("jane.doe@example.com", "john.smith@example.net", "rmiller.doe@example.org") y al menos un cliente inactivo ("Ana Garcia").
- **Estado de Tests**:
  - `pytest -v`: 9 tests pasaron exitosamente.

### T-04: Search logic and business validations
- **Acción del Agente**:
  - Creó `src/exceptions.py` definiendo `InvalidQueryException(detail: str)`.
  - Creó `src/services/customer_service.py` y `src/services/__init__.py` con la clase `CustomerSearchService`.
  - Implementó saneamiento de consulta (`strip()`), validación de longitud (mínimo 2 caracteres no vacíos, máximo 100) y búsqueda de subcadena insensible a mayúsculas/minúsculas sobre `name` y `email`.
  - Añadió pruebas unitarias en `tests/test_customer_service.py`.
- **Revisión Humana**:
  - Detección y corrección de un caso de prueba donde una subcadena no contigua provocó fallo en el test inicial de correo. Tras el ajuste, se ratificó la coincidencia estricta de subcadena.
- **Estado de Tests**:
  - `pytest -v`: 23 tests pasaron exitosamente.

### T-05: FastAPI HTTP API and endpoints
- **Acción del Agente**:
  - Creó `src/api/__init__.py`, `src/api/v1/__init__.py` y `src/api/v1/customers.py` exponiendo el endpoint `GET /api/v1/customers/search` con parámetro `q: str = Query(...)`.
  - Creó `src/main.py` registrando el enrutador y configurando el manejador global de `InvalidQueryException` hacia respuestas HTTP 400 con cuerpo JSON `{"detail": "..."}`.
  - Creó `tests/test_api.py` con pruebas de integración utilizando `TestClient(app)`.
- **Revisión Humana**:
  - Se comprobó la concordancia de códigos de estado: HTTP 200 para éxito y consultas sin coincidencias (`[]`), HTTP 400 para violaciones de longitud o espacios, y HTTP 422 para omisión del parámetro `q`.
- **Estado de Tests**:
  - `pytest -v`: 35 tests pasaron exitosamente.

### T-06: Automated testing and traceability verification
- **Acción del Agente**:
  - Consolidó la suite de pruebas unitarias (`tests/test_customer_service.py`) y de integración (`tests/test_api.py`).
  - Añadió verificación de latencia (< 150ms según NFR-01).
  - Creó `pyproject.toml` para filtrar la advertencia de obsolescencia de Starlette (`StarletteDeprecationWarning`), asegurando una ejecución limpia sin advertencias.
- **Revisión Humana**:
  - Se confirmó el cumplimiento al 100% de los criterios de aceptación AC-01 a AC-07 y de los escenarios de prueba TS-01 a TS-06.
- **Estado de Tests**:
  - `pytest -v`: 35 de 35 tests pasaron con 0 fallos y 0 advertencias en 0.34s.

## Problems Encountered
1. **Subcadena no contigua en prueba de correo**:
   - *Problema*: Al redactar una prueba unitaria para validar búsqueda por correo, se usó la consulta `"smith.net"` esperando coincidir con `"john.smith@example.net"`. La aserción falló porque `@example` separa a `smith` de `.net`.
   - *Solución*: Se ajustó el query de prueba a `"example.net"`, validando correctamente la regla de coincidencia por subcadena contigua.
2. **Advertencia de obsolescencia de Starlette TestClient**:
   - *Problema*: FastAPI 0.139 emite `StarletteDeprecationWarning` al importar `TestClient` sobre `httpx` estándar sin la librería experimental `httpx2`.
   - *Solución*: Para cumplir el criterio de aceptación de T-06 ("no warnings or failures"), se añadió `pyproject.toml` con configuración de filtro de advertencias específico (`ignore::starlette.exceptions.StarletteDeprecationWarning`).
3. **Manejo de consultas compuestas únicamente por espacios**:
   - *Problema*: Si no se aplicaba `strip()` antes de validar la longitud mínima de 2 caracteres, consultas como `"   "` pasaban inadvertidas y devolvían coincidencias parciales con espacios en los nombres.
   - *Solución*: Se aplicó saneamiento inicial `sanitized_query = query.strip()` previo a las evaluaciones de longitud.

## Human Interventions
- **Alineación con la Regla de Clientes Inactivos**: Se confirmó que los clientes inactivos (ej. "Ana Garcia" con `is_active=False`) deben devolverse en los resultados con su estatus intacto, respondiendo a la pregunta abierta Q-01.
- **Revisión y Corrección de Casos de Prueba**: Corrección de aserciones en `tests/test_customer_service.py` para asegurar que las pruebas reflejen fielmente la lógica de búsqueda por subcadena.
- **Aprobación de pyproject.toml**: Autorización de la inclusión de `pyproject.toml` para centralizar la configuración de pruebas de `pytest`.

## Requirement / Specification Changes
**N/A**. No se modificaron `REQUIREMENTS.md` ni `SPEC.md`. Todas las implementaciones se adaptaron estrictamente a las especificaciones preexistentes y a los supuestos documentados en la etapa de diseño.

## Final Verification
- **Herramienta de prueba**: `pytest -v` (v9.1.1)
- **Total de pruebas ejecutadas**: 35 pruebas
- **Pruebas aprobadas**: 35 (100%)
- **Pruebas fallidas**: 0
- **Advertencias**: 0
- **Tiempo de ejecución**: 0.34s
- **Cobertura de Criterios de Aceptación**:
  - AC-01 (GET /api/v1/customers/search?q=ana -> 200 + lista JSON): Verificado.
  - AC-02 (q=doe coincide con nombre y correo): Verificado.
  - AC-03 (Búsqueda insensible a mayúsculas/minúsculas): Verificado.
  - AC-04 (Estructura de respuesta completa con id, name, email, is_active): Verificado.
  - AC-05 (Consultas vacías, espacios o longitud < 2 -> HTTP 400): Verificado.
  - AC-06 (Sin coincidencias -> HTTP 200 + `[]`): Verificado.
  - AC-07 (Ejecución 100% exitosa de pytest): Verificado.
  - NFR-01 (Latencia inferior a 150ms): Verificado (~5ms en entorno local).

