# Módulo 1: Proyectos

> Los proyectos son contenedores de tareas y documentación. Cada tarea pertenece a un solo proyecto.

---

## Estructura de datos

| Campo | Tipo | Reglas |
|-------|------|--------|
| `id` | Entero (autoincremental) | Identificador único |
| `nombre` | Texto (obligatorio) | Máximo 120 caracteres |
| `descripcion` | Texto largo (opcional) | |
| `fecha_creacion` | Fecha (automática) | Se asigna al crear el proyecto |
| `estado` | `Activo` / `Archivado` | Por defecto `Activo` |

---

## Funcionalidades

### Listar proyectos
- Se muestran solo los proyectos **Activos** por defecto
- Opción de filtro por nombre (buscador)
- Opción de ver proyectos **Archivados**

### Crear proyecto
- Formulario con: Nombre (obligatorio) + Descripción (opcional)
- Fecha de creación se asigna automáticamente
- Estado inicial: `Activo`

### Editar proyecto
- Se puede modificar nombre y descripción
- No se puede modificar la fecha de creación

### Archivar proyecto
- Cambia el estado a `Archivado`
- El proyecto se oculta de las vistas por defecto
- **No se eliminan** las tareas ni documentos asociados
- **Restricción:** No se puede eliminar un proyecto que tenga tareas asociadas

---

## Relaciones

- Un proyecto **tiene muchas** tareas
- Un proyecto **tiene muchos** documentos
- Al eliminar un proyecto (solo si no tiene tareas), se eliminan también sus documentos y archivos adjuntos

---

## Vistas funcionales

### Vista: Lista de proyectos
```
+--------------------------------------------------+
|  Buscar proyecto...                        [+ Nuevo] |
+--------------------------------------------------+
| [●] Proyecto A              Activo   10 tareas   |
| [●] Proyecto B              Activo    3 tareas   |
| [○] Proyecto C (Archivado)  Archivado  0 tareas  |
+--------------------------------------------------+
```

### Vista: Detalle de proyecto
```
+--------------------------------------------------+
| Proyecto A                        [Editar][Archivar] |
| Descripción: ...                                    |
+--------------------------------------------------+
| Tareas (10)  |  Documentación (5)                  |
+--------------------------------------------------+
```
