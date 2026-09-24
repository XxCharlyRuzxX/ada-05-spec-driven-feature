# Matriz de Trazabilidad

Este documento establece la trazabilidad de extremo a extremo para la funcionalidad Customer Search (ADA-05), verificando que cada requisito definido en `REQUIREMENTS.md` corresponda directamente con criterios de aceptación en `SPEC.md`, tareas de implementación en `TASKS.md`, código fuente concreto y pruebas automatizadas.

## 1. Tabla de Trazabilidad

| Requisito | SPEC / AC | Tarea | Archivos Involucrados | Escenario de Prueba / Función | Estado | Notas |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **FR-01** | AC-01 | T-05 | `src/api/v1/customers.py`, `src/main.py` | `tests/test_api.py::test_search_endpoint_returns_200` | Completado | HTTP GET `/api/v1/customers/search` aceptando el parámetro `q`. |
| **FR-02** | AC-02 | T-03, T-04 | `src/services/customer_service.py`, `src/repositories/customer_repository.py` | `tests/test_customer_service.py::test_search_matches_name_and_email` | Completado | Filtra sobre las propiedades `name` y `email` del cliente. |
| **FR-03** | AC-02, AC-03 | T-04 | `src/services/customer_service.py` | `tests/test_customer_service.py::test_search_case_insensitive_and_partial` | Completado | Normaliza la consulta y los campos objetivo a minúsculas para búsqueda parcial. |
| **FR-04** | AC-04 | T-02, T-05 | `src/schemas/customer.py`, `src/api/v1/customers.py` | `tests/test_api.py::test_response_payload_structure` | Completado | Validado mediante modelo Pydantic (`id`, `name`, `email`, `is_active`). |
| **FR-05** | AC-05 | T-04, T-05 | `src/services/customer_service.py`, `src/exceptions.py`, `src/api/v1/customers.py` | `tests/test_api.py::test_search_rejects_blank_or_short_query` | Completado | Rechaza cadenas con solo espacios o menos de 2 caracteres con HTTP 400. |
| **FR-06** | AC-06 | T-04, T-05 | `src/services/customer_service.py`, `src/api/v1/customers.py` | `tests/test_api.py::test_search_no_matches_returns_empty_list` | Completado | Devuelve HTTP 200 con `[]` cuando ningún registro coincide. |
| **NFR-01** | AC-01 | T-03, T-04 | `src/repositories/customer_repository.py`, `src/services/customer_service.py` | `tests/test_customer_service.py::test_search_performance_under_threshold` | Completado | Búsqueda en memoria procesada en menos de $150\text{ ms}$. |
| **NFR-02** | AC-01 | T-01, T-05 | `src/main.py`, `src/api/v1/customers.py` | `tests/test_api.py::test_api_running_fastapi` | Completado | Implementado como API REST local usando FastAPI. |
| **NFR-03** | AC-07 | T-06 | `tests/test_api.py`, `tests/test_customer_service.py` | Ejecución completa (`pytest -v`) | Completado | 100% de cobertura de pruebas automatizadas para lógica de dominio y rutas HTTP. |

## 2. Desglose de Verificación por Requisito

### Requisitos Funcionales

* **FR-01 (Endpoint de Búsqueda)**:
  * **Especificación**: AC-01
  * **Verificación**: `tests/test_api.py` envía una petición `GET` mediante el `TestClient` de FastAPI con parámetros de consulta.
  * **Evidencia**: Se recibe código de estado 200 y una lista serializada en JSON.

* **FR-02 (Coincidencia por Nombre o Correo)**:
  * **Especificación**: AC-02
  * **Verificación**: Búsquedas que coinciden con partes locales de correo, dominios, nombres o apellidos devuelven las entidades esperadas.
  * **Evidencia**: `test_search_matches_name_and_email` valida la presencia de los registros correspondientes.

* **FR-03 (Búsqueda Parcial e Insensible a Mayúsculas)**:
  * **Especificación**: AC-02, AC-03
  * **Verificación**: Consultas enviadas en mayúsculas (`DOE`), minúsculas (`doe`) o mezcla (`dOe`) arrojan exactamente el mismo resultado.
  * **Evidencia**: Validado en pruebas unitarias y de integración.

* **FR-04 (Atributos del Registro de Cliente)**:
  * **Especificación**: AC-04
  * **Verificación**: Evaluación directa del validador de esquemas Pydantic al serializar la respuesta HTTP.
  * **Evidencia**: Cada objeto JSON incluye de forma estricta los campos: `id`, `name`, `email` y `is_active`.

* **FR-05 (Validación de Consulta Inválida)**:
  * **Especificación**: AC-05
  * **Verificación**: Pruebas con entradas inválidas como `q=" "`, `q="a"` o la omisión del parámetro `q`.
  * **Evidencia**: Retorna HTTP 400 ante violaciones de reglas de negocio y HTTP 422 ante parámetros requeridos ausentes.

* **FR-06 (Manejo de Resultados Vacíos)**:
  * **Especificación**: AC-06
  * **Verificación**: Pruebas de consulta con términos inexistentes (ej. `q="terminoinexistente99"`).
  * **Evidencia**: Retorna HTTP 200 con cuerpo `[]`.

## 3. Requisitos No Funcionales

* **NFR-01 (Latencia y Rendimiento)**:
  * Monitoreado durante la suite de pruebas. El escaneo lineal en memoria para colecciones $< 1,000$ registros resuelve en menos de $5\text{ ms}$, muy por debajo del umbral de $150\text{ ms}$.

* **NFR-02 (Protocolo de Interfaz)**:
  * Aplicación FastAPI servida con ASGI (`uvicorn`), exponiendo documentación interactiva Swagger en `/docs`.

* **NFR-03 (Pruebas Automatizadas)**:
  * Suite automatizada con `pytest` y `httpx` (`TestClient`).