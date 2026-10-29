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


---

# AI Usage Log - ADA-08 (Agent-Ready Repository)

Este bloque documenta la auditoría, diseño de guardrails, adaptadores y experimentos comparativos BEFORE/AFTER correspondientes a la práctica ADA-08.

---

## Entrada 5: Auditoría Inicial BEFORE y Detección de Fricción
- **Fecha**: 2026-10-29
- **Herramienta utilizada**: Antigravity Assistant / Gemini 3.8 Flash
- **Etapa**: Repository Readiness Audit - BEFORE
- **Intención / Prompt clave**:
  > *"Evaluar el repositorio baseline contra las 8 dimensiones de readiness de ADA-08, calculando puntaje y detectando puntos críticos de fricción."*
- **Propuesta de la IA**:
  - Sugirió calificar la dimensión de Instrucciones del Agente con 3/5 argumentando que ya existía un archivo `agents.md` con reglas básicas.
  - Detectó que no había CI ni scripts de verificación (`0/5` en Automation & Guardrails).
  - Identificó que las 35 pruebas unitarias pasaban pero que no había linter configurado ni protección contra archivos temporales.
- **Decisión y Criterio Humano**:
  - **Ajuste de calificación (Instrucciones de Agente)**: Se redujo a 2/5 (6.0/15) porque `agents.md` carecía de tabla de comandos estándar, carecía de comandos de verificación ejecutable y no tenía stop conditions explícitas, lo que genera fricción severa para cualquier agente autónomo.
  - **Aceptado íntegramente**: Calificación global baseline de 41 / 100 y priorización de los 3 puntos de fricción principales (falta de verificación automatizada, ausencia de .gitignore con .pyc en git, y falta de mapa de navegación).
- **Impacto / Artefactos modificados**:
  - `REPOSITORY_READINESS_AUDIT.md` (Sección BEFORE y Top 3 friction points).

---

## Entrada 6: Diseño de AGENTS.md y Adaptadores de Herramientas
- **Fecha**: 2026-10-29
- **Herramienta utilizada**: Antigravity Assistant / Gemini 3.8 Flash
- **Etapa**: Diseño de Contratos Operativos y Adaptadores
- **Intención / Prompt clave**:
  > *"Diseñar AGENTS.md como contrato operativo mínimo y estructurado, junto con adaptadores para GEMINI.md y CLAUDE.md sin duplicar fuentes de verdad."*
- **Propuesta de la IA**:
  - Propuso incluir en `AGENTS.md` un resumen de las historias de usuario y de las fórmulas de coincidencia de búsqueda tomadas de `SPEC.md`.
  - Sugirió crear archivos independientes `GEMINI.md` y `CLAUDE.md` con instrucciones detalladas de razonamiento paso a paso.
- **Decisión y Criterio Humano**:
  - **Rechazado (Duplicación de requisitos)**: Se eliminó cualquier copia o resumen de requisitos funcionales dentro de `AGENTS.md` para evitar el riesgo de divergencia de especificaciones (*Spec Drift*). `AGENTS.md` solo debe declarar que `REQUIREMENTS.md` y `SPEC.md` son las fuentes de verdad.
  - **Rechazado (Instrucciones redundantes en adaptadores)**: Se descartó duplicar reglas en `GEMINI.md` y `CLAUDE.md`. Se diseñaron como adaptadores delgados de solo 3 pasos que delegan formalmente en `AGENTS.md`.
  - **Aceptado**: Se definieron tablas claras de Comandos Estándar, Reglas de Cambio, Condiciones de Parada y Definición de Terminado (DoD) verificable.
- **Impacto / Artefactos modificados**:
  - `AGENTS.md`
  - `GEMINI.md`
  - `CLAUDE.md`

---

## Entrada 7: Descubribilidad y Conocimiento Implícito a Explícito
- **Fecha**: 2026-10-29
- **Herramienta utilizada**: Antigravity Assistant / Gemini 3.8 Flash
- **Etapa**: Análisis de Descubribilidad y Deuda de Contexto
- **Intención / Prompt clave**:
  > *"Identificar todo conocimiento implícito o tribal revelado durante la ejecución BEFORE que un desarrollador o agente tuvo que inferir o buscar indirectamente, y transformarlo en artefactos explícitos."*
- **Propuesta de la IA**:
  - Documentó IK-01 a IK-04 en `results/implicit-knowledge.md`:
    - IK-01: El comando completo de verificación (tests + lint + contrato).
    - IK-02: Qué archivos están protegidos contra edición directa (`README.md`, `architecture.md`, `SEED_CUSTOMERS`).
    - IK-03: Ubicación de puntos de entrada y guía de modificación por capas.
    - IK-04: Estándares de limpieza de repositorio (ignorar `.pyc`, `__pycache__`, `.DS_Store`).
- **Decisión y Criterio Humano**:
  - **Aceptado íntegramente**: Se aprobó la remediación de IK-01 mediante `./scripts/verify_repo.sh`, IK-02 e IK-03 mediante `docs/REPO_MAP.md` y `AGENTS.md`, e IK-04 mediante `.gitignore` y `scripts/check_repo_contract.py`.
- **Impacto / Artefactos modificados**:
  - `results/implicit-knowledge.md`
  - `docs/REPO_MAP.md`
  - `.gitignore`

---

## Entrada 8: Guardrail Determinista: check_repo_contract.py
- **Fecha**: 2026-10-29
- **Herramienta utilizada**: Antigravity Assistant / Gemini 3.8 Flash
- **Etapa**: Automatización de Guardrails y Seguridad
- **Intención / Prompt clave**:
  > *"Convertir la regla crítica de integridad y readiness del repositorio en una comprobación determinista de software ejecutable por humanos, agentes y CI."*
- **Propuesta de la IA**:
  - Propuso un script en Python que valida la existencia de archivos esenciales (`AGENTS.md`, `README.md`, `REQUIREMENTS.md`, `SPEC.md`, `ARCHITECTURE.md`, `TASKS.md`, `docs/REPO_MAP.md`, `.gitignore`, `scripts/verify_repo.sh`).
  - Amplió el script para verificar que `SPEC.md` referencie IDs `FR-` y `AC-`, que `AGENTS.md` contenga los comandos estándar, que exista la carpeta `results/` y que no haya archivos sensibles (`.env`, `*.key`) ni binarios `.pyc` rastreados en git.
- **Decisión y Criterio Humano**:
  - **Aceptado**: Se verificó que el script proporcione salidas legibles (`REPO_CONTRACT: PASS` o `REPO_CONTRACT: FAIL`) con código de salida 0 o 1 estricto, integrándose perfectamente en el pipeline.
- **Impacto / Artefactos modificados**:
  - `scripts/check_repo_contract.py`
  - `.gitignore` (purga de archivos `.pyc` de git cache)

---

## Entrada 9: Integración Continua (CI) y Contrato de Verificación Compartido
- **Fecha**: 2026-10-29
- **Herramienta utilizada**: Antigravity Assistant / Gemini 3.8 Flash
- **Etapa**: Verificación Reproducible y CI
- **Intención / Prompt clave**:
  > *"Crear un único comando de verificación para el agente y desarrollador, y asegurar que el pipeline de CI ejecute exactamente el mismo contrato."*
- **Propuesta de la IA**:
  - Diseñó `./scripts/verify_repo.sh` ejecutando `pytest -q`, `ruff check .` y `python3 scripts/check_repo_contract.py`.
  - Diseñó `.github/workflows/verify.yml` para GitHub Actions ejecutando `./scripts/verify_repo.sh`.
  - Configuró reglas de estilo y longitud de línea en `pyproject.toml` para `ruff`.
- **Decisión y Criterio Humano**:
  - **Aceptado**: Se comprobó que el flujo garantice paridad absoluta: si el agente ve `VERIFY_REPO: PASS` en su entorno local, el CI en GitHub Actions pasará con exactamente el mismo resultado.
- **Impacto / Artefactos modificados**:
  - `scripts/verify_repo.sh`
  - `pyproject.toml`
  - `requirements.txt` (adición de `ruff>=0.1.0`)
  - `.github/workflows/verify.yml`

---

## Entrada 10: Comparación Experimental AFTER y Evaluación de Autonomía
- **Fecha**: 2026-10-29
- **Herramienta utilizada**: Antigravity Assistant / Gemini 3.8 Flash
- **Etapa**: Ejecución AFTER y Evaluación Final
- **Intención / Prompt clave**:
  > *"Ejecutar la misma tarea CR-01 en el repositorio preparado para agentes usando el mismo prompt estricto, registrar métricas comparativas y determinar qué decisiones siguen requiriendo intervención humana."*
- **Propuesta de la IA**:
  - El agente del AFTER completó la implementación en menos turnos, sin fallos de comandos, modificando exactamente 4 archivos de código y pruebas, respetando todas las rutas protegidas y pasando `./scripts/verify_repo.sh` en 0.28s.
  - La IA redactó el análisis de impacto y la auditoría AFTER arrojando un puntaje de 98/100 (delta +57).
- **Decisión y Criterio Humano**:
  - **Validación del resultado**: Se constató empíricamente la efectividad del concepto Agent-Ready: el agente no requirió pistas manuales, no modificó archivos fuera de alcance y entregó evidencia verificable sin ambigüedad.
  - **Identificación de límites humanos**: Se concluyó que aunque el agente es 100% autónomo para tareas bien delimitadas dentro de los boundaries, la formulación de requisitos de negocio, la priorización y la aprobación de cambios que rompan compatibilidad o modifiquen arquitectura siguen reservadas al criterio del ingeniero humano.
- **Impacto / Artefactos modificados**:
  - `results/after-agent-run.md`
  - `REPOSITORY_READINESS_AUDIT.md` (Sección AFTER y delta)
  - `results/readiness-improvement-report.md`
