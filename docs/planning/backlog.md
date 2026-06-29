# Backlog del Proyecto — TaskRegistry

> **Proyecto:** TaskRegistry — Bitácora personal de tareas laborales
> **Última actualización:** 2026-06-28

---

## Épicas

| ID | Épica | Prioridad |
|----|-------|-----------|
| E-01 | **Configuración del proyecto (Sprint 0)** | 🔴 Crítica |
| E-02 | **Módulo Proyectos** — CRUD de proyectos | 🔴 Crítica |
| E-03 | **Módulo Tareas** — Registro diario de tareas | 🔴 Crítica |
| E-04 | **Módulo Documentación** — Adjuntar docs a proyectos | 🔴 Crítica |
| E-05 | **Módulo Sincronización Azure** — Sincronización batch a Azure DevOps | 🔴 Crítica |
| E-06 | **Módulo Tablero de Control** — Métricas y dashboards | 🔴 Crítica |

---

## Historias de Usuario (Backlog completo)

### E-01: Configuración del proyecto
- [x] HU-001: Como desarrollador, quiero tener Python y pip funcionando para poder instalar dependencias
- [x] HU-002: Como desarrollador, quiero tener la estructura de carpetas del proyecto creada para organizar el código
- [x] HU-003: Como desarrollador, quiero tener el archivo de dependencias (requirements.txt) para instalar las librerías necesarias
- [x] HU-004: Como desarrollador, quiero tener el archivo pyproject.toml configurado con Ruff y pytest
- [x] HU-005: Como desarrollador, quiero tener el archivo main.py funcional que levante FastAPI para verificar que todo funciona
- [x] HU-006: Como desarrollador, quiero tener el repositorio Git inicializado y conectado a GitHub para versionar el código
- [x] HU-007: Como desarrollador, quiero tener CI/CD configurado con GitHub Actions para automatizar lint y tests
- [x] HU-008: Como desarrollador, quiero tener el core del proyecto configurado (config, database, dependencies, logging)

### E-02: Módulo Proyectos
- [x] HU-009: Como usuario, quiero crear un proyecto con nombre y descripción para organizar mis tareas _(2026-06-28 - modelo y esquemas)_
- [x] HU-010: Como usuario, quiero ver la lista de proyectos para seleccionar uno _(2026-06-28 - servicio CRUD)_
- [x] HU-011: Como usuario, quiero editar un proyecto para actualizar su información _(2026-06-28 - API REST)_
- [x] HU-012: Como usuario, quiero archivar un proyecto para ocultarlo de la vista principal _(2026-06-28 - API REST)_

### E-03: Módulo Tareas
- [ ] HU-013: Como usuario, quiero registrar una tarea con fecha, proyecto, descripción y tiempo invertido
- [ ] HU-014: Como usuario, quiero ver mis tareas filtradas por proyecto y rango de fechas
- [ ] HU-015: Como usuario, quiero editar una tarea para corregir datos
- [ ] HU-016: Como usuario, quiero cambiar el estado de una tarea (pendiente → en progreso → completada)

### E-04: Módulo Documentación
- [ ] HU-017: Como usuario, quiero adjuntar archivos a un proyecto para tener la documentación técnica centralizada
- [ ] HU-018: Como usuario, quiero ver y descargar los archivos adjuntos de un proyecto

### E-05: Módulo Sincronización Azure
- [ ] HU-019: Como usuario, quiero configurar la conexión con Azure DevOps (URL, proyecto, PAT)
- [ ] HU-020: Como usuario, quiero seleccionar tareas y sincronizarlas a una HU de Azure DevOps

### E-06: Módulo Tablero de Control
- [ ] HU-021: Como usuario, quiero ver métricas de tiempo invertido por proyecto en un rango de fechas
- [ ] HU-022: Como usuario, quiero visualizar mi productividad con gráficos y resúmenes
