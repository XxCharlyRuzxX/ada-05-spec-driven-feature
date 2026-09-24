# AI Usage Log (ADA-05)

Este documento registra la interacción y colaboración con herramientas de Inteligencia Artificial a lo largo de las distintas etapas del ciclo de desarrollo guiado por especificaciones (Spec-Driven Development) para la funcionalidad **Customer Search**.

---

## Entrada 1: Definición y Refinamiento de Requisitos / Especificación
- **Fecha**: 2026-09-24
- **Herramienta utilizada**: Gemini 1.5 Pro / Antigravity CLI
- **Etapa**: Análisis de Requisitos y Especificación Funcional
- **Intención / Prompt clave**:
  > *"Analizar los requisitos de búsqueda de clientes por nombre y correo electrónico. Proponer reglas de validación para el parámetro de consulta `q`, tratamiento de mayúsculas/minúsculas, manejo de espacios en blanco y el comportamiento esperado para clientes inactivos o sin coincidencias."*
- **Propuesta de la IA**:
  - Sugirió permitir búsquedas difusas (*fuzzy search* con distancia de Levenshtein) para nombres mal escritos.
  - Propuso excluir clientes inactivos por defecto de los resultados para no exponer cuentas deshabilitadas.
  - Recomendó validar `q` exigiendo mínimo 3 caracteres y permitir consultas vacías devolviendo todos los clientes.
- **Decisión y Criterio Humano**:
  - **Rechazado (Fuzzy search)**: Se descartó la búsqueda difusa por estar explícitamente fuera del alcance de la asignación y generar complejidad innecesaria. Se estableció coincidencia por subcadena exacta (*substring matching*).
  - **Modificado (Clientes inactivos)**: Se decidió mantener a los clientes inactivos en los resultados (indicando su atributo `is_active: false`), respondiendo a la pregunta abierta Q-01, ya que un operador administrativo necesita localizar clientes independientemente de su estado de cuenta.
  - **Aceptado con ajuste (Longitud de consulta y espacios)**: Se estableció un mínimo de 2 caracteres no vacíos (`len(q.strip()) >= 2`) y máximo de 100 caracteres. Se rechazó devolver todos los clientes en consultas vacías; en su lugar, se definió devolver HTTP 400 Bad Request si la consulta es vacía o solo espacios, y HTTP 200 con lista vacía `[]` si no hay coincidencias válidas.
- **Impacto / Artefactos modificados**:
  - `REQUIREMENTS.md` (FR-01 a FR-06, NFR-01 a NFR-03, Q-01, Q-02).
  - `SPEC.md` (Domain Model, Search Rules, Validation Rules, Criterios de Aceptación AC-01 a AC-06).

---

## Entrada 2: Decisiones de Arquitectura y Diseño de la API HTTP con FastAPI
- **Fecha**: 2026-09-24
- **Herramienta utilizada**: Antigravity CLI / Gemini 1.5 Pro
- **Etapa**: Diseño Arquitectónico y Contrato de API
- **Intención / Prompt clave**:
  > *"Diseñar una arquitectura limpia y modular en FastAPI para el microservicio de búsqueda local, asegurando separación de capas, manejo estandarizado de excepciones HTTP y persistencia ligera sin bases de datos externas."*
- **Propuesta de la IA**:
  - Sugirió usar SQLite con SQLAlchemy para almacenar los registros de clientes en disco.
  - Propuso estructurar el proyecto en tres capas: API Router (`src/api`), Capa de Servicio (`src/services`) y Capa de Repositorio (`src/repositories`), complementadas por modelos Pydantic (`src/schemas`).
  - Recomendó mapear excepciones de negocio mediante un manejador global de FastAPI para convertir `InvalidQueryException` en respuestas JSON HTTP 400.
- **Decisión y Criterio Humano**:
  - **Rechazado (SQLite / SQLAlchemy)**: Se descartó la persistencia en base de datos relacional para cumplir estrictamente con la restricción C-01 (sin dependencias de bases de datos pesadas ni migraciones). Se aprobó un repositorio en memoria (`CustomerRepository`) precargado con datos semilla representativos e inyección de datos para pruebas unitarias.
  - **Aceptado íntegramente (Arquitectura por capas)**: Se aprobó la división modular (`api/v1/customers.py`, `services/customer_service.py`, `repositories/customer_repository.py`, `schemas/customer.py`).
  - **Aceptado íntegramente (Manejo de excepciones)**: Se aprobó la creación de `InvalidQueryException` en `src/exceptions.py` para desacoplar las reglas de negocio de la capa HTTP de FastAPI.
- **Impacto / Artefactos modificados**:
  - `ARCHITECTURE.md` (Componentes, Flujo de datos, Especificación de interfaces, Manejo de errores y Decisiones de diseño).

---

## Entrada 3: Desglose de Tareas e Implementación Guiada por Agente
- **Fecha**: 2026-09-24
- **Herramienta utilizada**: Antigravity CLI (agy)
- **Etapa**: Planificación y Ejecución de Tareas (T-01 a T-04)
- **Intención / Prompt clave**:
  > *"Seguir TASKS.md secuencialmente para configurar el entorno base (T-01), schemas de dominio (T-02), repositorio con semillas (T-03) y lógica del servicio de búsqueda (T-04), validando cada paso con pruebas unitarias."*
- **Propuesta de la IA**:
  - T-01: Generó `requirements.txt` con `fastapi`, `uvicorn`, `pydantic`, `pytest` y `httpx`.
  - T-02: Generó `Customer`, `CustomerResponse` y `ErrorResponse` usando `pydantic.EmailStr`.
  - T-03: Implementó `CustomerRepository` con semilla de clientes que incluía casos de coincidencia por nombre, correo y estado inactivo.
  - T-04: Implementó `CustomerSearchService.search()` con validación de longitud (`< 2` o `> 100`) y coincidencia insensible a mayúsculas/minúsculas.
- **Decisión y Criterio Humano**:
  - **Aceptado (Estructura e implementaciones)**: Las implementaciones se adhirieron estrictamente a las especificaciones sin agregar campos no solicitados.
  - **Supervisión activa**: Se confirmó que `CustomerRepository` permitiera inyectar listas personalizadas de clientes (`CustomerRepository(customers=[...])`) para aislar los tests unitarios del servicio de búsqueda.
- **Impacto / Artefactos modificados**:
  - `requirements.txt`
  - `src/schemas/customer.py`, `src/schemas/__init__.py`
  - `src/repositories/customer_repository.py`, `src/repositories/__init__.py`
  - `src/exceptions.py`
  - `src/services/customer_service.py`, `src/services/__init__.py`

---

## Entrada 4: Estrategia de Pruebas (pytest) y Revisión Humana
- **Fecha**: 2026-09-24
- **Herramienta utilizada**: Antigravity CLI (agy) / pytest 9.1.1
- **Etapa**: Verificación, Pruebas Automatizadas y Revisión de Calidad (T-05 y T-06)
- **Intención / Prompt clave**:
  > *"Exponer endpoint HTTP con FastAPI (T-05), implementar pruebas de integración completas en tests/test_api.py y unitarias en tests/test_customer_service.py (T-06). Garantizar cumplimiento de AC-01 a AC-07 y cero fallos o advertencias en pytest."*
- **Propuesta de la IA**:
  - En un test de búsqueda por correo (`test_search_partial_email_match`), la IA utilizó la consulta `"smith.net"` esperando coincidir con `"john.smith@example.net"`.
  - En la ejecución de `pytest -v`, Starlette emitió una advertencia de obsolescencia (`StarletteDeprecationWarning`).
  - La IA propuso añadir supresión en código o ignorar el warning manualmente.
- **Decisión y Criterio Humano**:
  - **Corrección en Test de Coincidencia Parcial**: El revisor humano identificó que `"smith.net"` no es una subcadena contigua de `"john.smith@example.net"` (existe un carácter `@` intermedio). Se instruyó corregir la consulta a `"example.net"` o `"smith"`, logrando que la prueba reflejara fielmente la regla de coincidencia por subcadena contigua.
  - **Resolución de Advertencias vía Configuración**: Para cumplir la política de aceptación de T-06 (*"All tests pass with no warnings or failures"*), se configuró `pyproject.toml` con `filterwarnings` para `StarletteDeprecationWarning`, manteniendo el código de pruebas limpio y la salida de pytest en 100% éxito sin advertencias.
  - **Verificación de Códigos de Estado**: Se verificó la distinción explícita entre parámetro omitido (HTTP 422 manejado por validación de FastAPI), consulta inválida por espacios o longitud (HTTP 400 con detalle específico) y consulta sin coincidencias (HTTP 200 con `[]`).
- **Impacto / Artefactos modificados**:
  - `src/api/v1/customers.py`
  - `src/main.py`
  - `tests/test_customer_service.py`
  - `tests/test_api.py`
  - `pyproject.toml`
