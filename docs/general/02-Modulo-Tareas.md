# Módulo 2: Tareas

> Corazón de la aplicación. Cada tarea representa una actividad realizada, con control de tiempo y trazabilidad hasta Azure DevOps.

---

## Estructura de datos

| Campo | Tipo | Reglas |
|-------|------|--------|
| `id` | Entero (autoincremental) | Identificador único |
| `titulo` | Texto (obligatorio) | Máximo 200 caracteres |
| `descripcion` | Texto largo (opcional) | |
| `proyecto_id` | Relación → Proyecto | Obligatorio |
| `fecha_inicio` | Fecha (obligatorio) | Por defecto la fecha actual |
| `fecha_fin` | Fecha (obligatorio) | Debe ser >= `fecha_inicio` |
| `tiempo_invertido` | Decimal (horas) | Ver regla de cálculo abajo |
| `estado` | Texto | `Nueva` / `En proceso` / `Ejecutada` / `Sincronizada` |
| `id_azure_devops` | Texto (opcional) | ID del Work Item creado en Azure DevOps |
| `id_hu_azure_devops` | Texto (opcional) | ID del Work Item HU padre en Azure DevOps |

---

## Reglas del campo `tiempo_invertido`

- Se **calcula automáticamente** como `(fecha_fin - fecha_inicio)` en horas decimales
- El usuario puede **sobrescribirlo manualmente** (ej. trabajo en bloque de 2h aunque el calendario indique 8h)
- Si el usuario modifica `fecha_inicio` o `fecha_fin`, el tiempo se **recalcula automáticamente**
- Las tareas con tiempo editado manualmente deben tener un **indicador visual** que lo distinga

---

## Estados de una tarea

```
                  ┌─────────┐
                  │  Nueva   │
                  └────┬────┘
                       │ (manual)
                       ▼
                 ┌────────────┐
                 │ En proceso  │
                 └──────┬─────┘
                        │ (manual)
                        ▼
                  ┌───────────┐
                  │ Ejecutada  │
                  └──────┬────┘
                         │ (automático al sincronizar)
                         ▼
                   ┌──────────────┐
                   │ Sincronizada │
                   └──────────────┘
```

### Reglas de estados

| Transición | ¿Quién? | ¿Cuándo? |
|-----------|---------|----------|
| `Nueva` ↔ `En proceso` | Usuario | En cualquier momento |
| `En proceso` ↔ `Ejecutada` | Usuario | En cualquier momento |
| `Nueva` → `Ejecutada` | Usuario | Salto directo permitido |
| `Ejecutada` → `Sincronizada` | Sistema | Al completar la sincronización con Azure DevOps |
| `Sincronizada` → cualquier otro | **No permitido** | La tarea queda en solo lectura |

### Restricciones

- Una tarea en estado **`Sincronizada`** no puede editarse ni cambiar de estado
- Solo las tareas en estado **`Ejecutada`** pueden ser seleccionadas para sincronizar
- Si el usuario intenta sincronizar tareas en otro estado, la app debe mostrar una advertencia

---

## Funcionalidades

### Crear tarea
- Formulario con: proyecto, título, descripción, fecha inicio, fecha fin, tiempo invertido, estado
- Por defecto: fecha_inicio = hoy, estado = `Nueva`
- Tiempo invertido se calcula al seleccionar fechas (editable)

### Editar tarea
- Todos los campos editables **excepto** si el estado es `Sincronizada`
- Si se cambian las fechas, el tiempo invertido se recalcula

### Cambiar estado
- Desde la lista o detalle de la tarea
- Dropdown o botones con los estados permitidos según el estado actual

### Listar tareas
- Filtros: por proyecto, por estado, por rango de fechas
- Vista por defecto: ordenadas por fecha descendente

---

## Vistas funcionales

### Vista: Lista de tareas con filtros
```
+--------------------------------------------------+
| Proyecto: [Todos ▼]  Estado: [Todos ▼]           |
| Desde: [____]  Hasta: [____]           [Buscar]   |
+--------------------------------------------------+
| ☐ | Título              | Proyecto   | Tiempo | Estado     |
| ☐ | Configurar BD       | Backend    | 2.5h   | Ejecutada  |
| ☐ | Revisión PR #42     | Backend    | 1.0h   | Sincronizada|
| ☐ | Documentar API      | Backend    | 3.0h   | En proceso |
+--------------------------------------------------+
| [Sincronizar seleccionadas] (solo si hay Ejecutadas) |
```

### Vista: Detalle / edición de tarea
```
+--------------------------------------------------+
| Título:    [Configurar BD de pruebas           ] |
| Proyecto:  [Backend ▼]                            |
| Descripción:                                      |
| [ Crear base de datos PostgreSQL para pruebas... ] |
|                                                   |
| Fecha inicio: [12/06/2026]  Fecha fin: [12/06/2026] |
| Tiempo invertido: [2.5] horas  (calculado ├─✎─┤)  |
| Estado: [Ejecutada ▼]                            |
|                                                   |
| Azure DevOps ID: 12345  (solo si sincronizada)    |
| HU asociada:     HUS-987  (solo si sincronizada)  |
+--------------------------------------------------+
| [Guardar]  [Cancelar]                             |
+--------------------------------------------------+
```
