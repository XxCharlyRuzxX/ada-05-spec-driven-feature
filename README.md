# Customer Search Feature (ADA-05)

Microservicio HTTP REST construido bajo la metodología **Spec-Driven Development** (Desarrollo Guiado por Especificaciones) utilizando **FastAPI**, **Python 3.11+** y **pytest**. Permite buscar clientes de manera eficiente por nombre o correo electrónico mediante coincidencias parciales insensibles a mayúsculas y minúsculas.

---

## 🛠️ Stack Tecnológico

- **Lenguaje**: Python 3.11+ (desarrollado y verificado en Python 3.12)
- **Framework Web**: [FastAPI](https://fastapi.tiangolo.com/)
- **Servidor ASGI**: [Uvicorn](https://www.uvicorn.org/)
- **Modelos y Validación**: [Pydantic v2](https://docs.pydantic.dev/) (con validación de correos vía `email-validator`)
- **Testing y Calidad**: [pytest](https://docs.pytest.org/) y [HTTPX](https://www.python-httpx.org/) (FastAPI `TestClient`)
- **Herramienta de Asistencia**: Antigravity CLI (`agy`)

---

## 📁 Estructura del Proyecto

El repositorio está estructurado siguiendo un diseño en capas que aísla el modelo de dominio, la lógica de negocio, el acceso a datos y la entrega HTTP:

```text
ada-05-spec-driven-feature/
├── requirements.txt           # Dependencias principales del proyecto
├── pyproject.toml             # Configuración del entorno de pruebas pytest
├── AI_USAGE_LOG.md            # Registro de uso e interacción con IA (ADA-05 14.1)
├── REQUIREMENTS.md            # Requisitos funcionales y no funcionales
├── SPEC.md                    # Especificación técnica, reglas y criterios de aceptación
├── ARCHITECTURE.md            # Diseño arquitectónico y flujo de datos
├── TASKS.md                   # Desglose secuencial de tareas (T-01 a T-06)
├── AGENTS.md                  # Instrucciones y reglas de gobernanza para agentes
├── results/
│   └── agent-report.md        # Reporte final del agente (ADA-05 17)
├── src/
│   ├── __init__.py
│   ├── main.py                # Punto de entrada de la aplicación FastAPI
│   ├── exceptions.py          # Excepciones de dominio (InvalidQueryException)
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── customers.py   # Controlador y rutas HTTP (GET /api/v1/customers/search)
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── customer.py        # Modelos Pydantic (Customer, CustomerResponse, ErrorResponse)
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── customer_repository.py # Repositorio en memoria con datos semilla
│   └── services/
│       ├── __init__.py
│       └── customer_service.py    # Lógica de búsqueda, saneamiento y validación
└── tests/
    ├── __init__.py
    ├── test_customer_service.py   # Pruebas unitarias de schemas, repositorio y servicio
    └── test_api.py                # Pruebas de integración HTTP y latencia
```

---

## 🚀 Instalación y Preparación

### 1. Clonar el repositorio y navegar a la carpeta
```bash
git clone <url-del-repositorio>
cd ada-05-spec-driven-feature
```

### 2. Crear y activar un entorno virtual
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 💻 Ejecución del Servidor Local

Inicia el servidor ASGI con recarga automática:

```bash
uvicorn src.main:app --reload
```

El servicio estará disponible en `http://127.0.0.1:8000`.

### Documentación Interactiva (Swagger UI)
Accede desde tu navegador a la documentación generada automáticamente por OpenAPI:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🔍 Uso de la API (Ejemplos con cURL)

### 1. Búsqueda exitosa por nombre
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/customers/search?q=doe" -H "Accept: application/json"
```

**Respuesta HTTP 200 OK:**
```json
[
  {
    "id": "c7a6f23b-01d8-4be6-98ec-6e54f73801a1",
    "name": "Jane Doe",
    "email": "jane.doe@example.com",
    "is_active": true
  },
  {
    "id": "d1e2f3a4-b5c6-7d8e-9f0a-1b2c3d4e5f6a",
    "name": "John Doe",
    "email": "john.smith@example.net",
    "is_active": true
  },
  {
    "id": "b2c3d4e5-f6a7-8b9c-0d1e-2f3a4b5c6d7e",
    "name": "Robert Miller",
    "email": "rmiller.doe@example.org",
    "is_active": true
  }
]
```

### 2. Búsqueda insensible a mayúsculas
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/customers/search?q=ALICE"
```

### 3. Búsqueda sin coincidencias (Devuelve lista vacía)
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/customers/search?q=inexistente"
```
**Respuesta HTTP 200 OK:**
```json
[]
```

### 4. Consulta inválida (menos de 2 caracteres o solo espacios)
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/customers/search?q=a"
```
**Respuesta HTTP 400 Bad Request:**
```json
{
  "detail": "Query string must be at least 2 characters long"
}
```

### 5. Parámetro de consulta omitido
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/customers/search"
```
**Respuesta HTTP 422 Unprocessable Entity:**
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["query", "q"],
      "msg": "Field required"
    }
  ]
}
```

---

## 🧪 Ejecución de Pruebas Automatizadas

Ejecuta la suite completa de pruebas unitarias y de integración con salida detallada:

```bash
pytest -v
```

### Resultado esperado:
```text
============================== test session starts ==============================
...
tests/test_api.py::TestCustomerSearchAPI::test_search_success_ac01 PASSED
tests/test_api.py::TestCustomerSearchAPI::test_search_matches_name_and_email_ac02 PASSED
tests/test_api.py::TestCustomerSearchAPI::test_search_case_insensitive_ac03 PASSED
tests/test_api.py::TestCustomerSearchAPI::test_search_item_fields_ac04 PASSED
tests/test_api.py::TestCustomerSearchAPI::test_search_short_or_blank_query_ac05 PASSED
tests/test_api.py::TestCustomerSearchAPI::test_search_non_existent_returns_empty_list_ac06 PASSED
tests/test_api.py::TestCustomerSearchAPI::test_search_missing_q_parameter_ts04 PASSED
tests/test_api.py::TestCustomerSearchAPI::test_search_query_exceeding_max_length PASSED
tests/test_api.py::TestCustomerSearchAPI::test_search_response_latency_nfr01 PASSED
tests/test_customer_service.py::TestCustomerSchema::test_customer_creation_valid PASSED
...
============================== 35 passed in 0.34s ===============================
```

---

## 📋 Trazabilidad y Gobernanza Spec-Driven

Este proyecto sigue una estricta jerarquía de gobernanza para garantizar consistencia entre especificaciones y código:

1. **Requisitos ([REQUIREMENTS.md](REQUIREMENTS.md))**: Define las historias de usuario, requerimientos funcionales (FR-01 a FR-06) y no funcionales (NFR-01 a NFR-03).
2. **Especificación Técnica ([SPEC.md](SPEC.md))**: Establece el contrato de API, modelo de dominio, reglas de búsqueda y criterios de aceptación verificables (AC-01 a AC-07).
3. **Arquitectura ([ARCHITECTURE.md](ARCHITECTURE.md))**: Documenta el diseño en capas, interfaces y justificación técnica de decisiones (repositorio en memoria, desacoplamiento de servicios).
4. **Plan de Trabajo ([TASKS.md](TASKS.md))**: Desglose secuencial de tareas (T-01 a T-06) con condiciones de aceptación y verificación.
5. **Gobernanza de Agente ([AGENTS.md](AGENTS.md))**: Reglas que prohíben modificar especificaciones para acomodar código y exigen validación continua con `pytest -v`.
6. **Bitácora de IA ([AI_USAGE_LOG.md](AI_USAGE_LOG.md))**: Registro detallado de prompts, propuestas, decisiones humanas y artefactos modificados.
7. **Informe Final ([results/agent-report.md](results/agent-report.md))**: Reporte de ejecución, incidentes, verificación final y lecciones aprendidas.
