# ADR-002: Estructura del Proyecto

- **Estado:** Aceptado
- **Fecha:** 2026-06-20
- **Contexto:** Definir cómo se organizan los archivos y carpetas del proyecto

---

## Decisión

Se adopta una **estructura modular por dominio**. Cada módulo funcional de la aplicación (Proyectos, Tareas, Documentación, Sincronización, Tablero) es autocontenido con sus propios modelos, router, servicios, repositorios y templates.

---

## Opciones Consideradas

### Opción A — Capas planas
```
taskregistry/
├── main.py
├── database.py
├── models.py        # Todos los modelos juntos
├── routers/         # Todos los routers
├── services/        # Todos los servicios
└── templates/       # Todas las plantillas
```
- ✅ Simple inicialmente
- ❌ No escala — models.py y services.py se vuelven archivos enormes
- ❌ No refleja la organización de la documentación existente

### Opción B — Modular por dominio ✅
```
taskregistry/
├── core/             # Configuración compartida
├── proyectos/        # Todo lo de proyectos
├── tareas/           # Todo lo de tareas
├── documentos/       # Todo lo de documentos
├── sincronizacion/   # Todo lo de sincronización Azure
├── tablero/          # Todo lo de tablero de control
└── static/           # Assets globales
```
- ✅ Cada módulo es independiente y autocontenido
- ✅ Refleja la estructura de la documentación (un módulo = una carpeta)
- ✅ Fácil de navegar y mantener
- ✅ Escalable para features futuras

---

## Consecuencias

- Cada módulo contiene: `models.py`, `schemas.py`, `repository.py`, `service.py`, `router.py`, `templates/`
- El archivo `main.py` importa y monta cada router
- La configuración compartida (BD, dependencias, logging) vive en `core/`
- Los datos de usuario (BD, archivos) van en `data/` fuera del código fuente
