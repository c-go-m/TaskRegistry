# Definition of Done (DoD) — TaskRegistry

> **Versión:** 1.0
> **Última actualización:** 2026-06-26

---

## Criterios obligatorios para toda tarea de código

Una historia o tarea se considera **completada** solo si cumple **todos** los siguientes criterios:

### 1. Código
- [ ] El código sigue la estructura modular definida en ADR-002
- [ ] El código sigue las convenciones de nombres definidas (PascalCase para clases, snake_case para funciones/variables/archivos)
- [ ] El código pasa el linter (`ruff check .`) sin errores
- [ ] El código pasa el formateo (`ruff format .`) sin modificaciones pendientes
- [ ] No hay código comentado ni `print()` de debugging (usar logging en su lugar)

### 2. TDD (Test-Driven Development)
Toda tarea que involucre escribir código de lógica debe seguir el ciclo TDD:
- [ ] **RED:** Se escribe el test que falla antes de implementar
- [ ] **GREEN:** Se implementa el código mínimo para que el test pase
- [ ] **REFACTOR:** Se refactoriza el código manteniendo los tests verdes
- [ ] Cobertura mínima: las nuevas líneas de código deben tener test asociado

### 3. Tests
- [ ] Los tests unitarios nuevos pasan correctamente
- [ ] Los tests existentes siguen funcionando (no se rompió nada)
- [ ] Se ejecuta `pytest` y todos los tests pasan

### 4. Commits (Conventional Commits)
- [ ] Cada commit sigue el formato estándar:
  | Tipo | Uso |
  |------|-----|
  | `feat:` | Nueva funcionalidad |
  | `fix:` | Corrección de bug |
  | `test:` | Añadir o modificar tests |
  | `refactor:` | Cambios que no agregan funcionalidad ni corrigen bugs |
  | `docs:` | Documentación |
  | `chore:` | Tareas de mantenimiento (dependencias, config, CI) |
  | `ci:` | Cambios en CI/CD |

### 5. Validación manual
- [ ] La funcionalidad se probó manualmente en el navegador (si aplica)
- [ ] No se rompieron otras funcionalidades existentes

### 6. Documentación
- [ ] Si la tarea agrega configuración nueva, se actualizó `.env.example`
- [ ] Si la tarea agrega un endpoint nuevo, este aparece en Swagger UI (`/docs`)
- [ ] Si la tarea cambia la estructura de BD, se actualizaron los modelos y migraciones

---

## Criterios específicos para el Sprint 0 (Configuración)

Además de los criterios generales:
- [ ] El proyecto arranca correctamente con `python run.py`
- [ ] Swagger UI está accesible en `http://localhost:8000/docs`
- [ ] Ruff no reporta errores en los archivos creados
- [ ] El repositorio está en GitHub con al menos un commit inicial
- [ ] El README.md tiene las instrucciones básicas de instalación
