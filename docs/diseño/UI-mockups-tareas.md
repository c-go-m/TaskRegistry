# Mockups — Módulo Tareas

> Wireframes y especificaciones visuales para el módulo de Registro de Tareas.
> Basado en el Design System definido en [UI-design-system.md](./UI-design-system.md).

---

## Índice

- [Vista: Lista de Tareas (Cards)](#vista-lista-de-tareas-cards)
- [Vista: Detalle/Edición de Tarea](#vista-detalleedición-de-tarea)
- [Vista: Crear Tarea](#vista-crear-tarea)
- [Estado Vacío](#estado-vacío)
- [Estados de Carga](#estados-de-carga)

---

## Vista: Lista de Tareas (Cards)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Tareas                                              [+ Nueva tarea]   │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
│  ┌─────── Filtros ─────────────────────────────────────────────────┐   │
│  │                                                                  │   │
│  │  Proyecto: [Todos     ▼]    Estado: [Todos       ▼]             │   │
│  │                                                                  │   │
│  │  Desde: [12/06/2026]  Hasta: [19/06/2026]          [Aplicar]   │   │
│  │                                                                  │   │
│  │  🔍 Buscar por título...                                         │   │
│  │                                                                  │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ☐ Seleccionar todo                                                    │
│                                                                         │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ ☐ │ 🟢  Configurar BD de pruebas        │  Backend │ 12/06    │    │
│  │    │                                     │  ⏱ 2.5h  │          │    │
│  │    │ Desc: Crear base de datos para...   │  ✏️ manual            │    │
│  │    │                                     │                      │    │
│  │    └─────────────────────────────────────┴──────────────────────┘    │
│  └────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ ☐ │ 🔵  Revisión PR #42                  │  Backend │ 11/06    │    │
│  │    │                                     │  ⏱ 1.0h  │          │    │
│  │    │ Desc: Revisar pull request #42...   │  Sincronizada        │    │
│  │    │                                     │  🔗 ID: 12345       │    │
│  │    └─────────────────────────────────────┴──────────────────────┘    │
│  └────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ ☑ │ 🟠  Documentar API de usuarios        │ Frontend │ 10/06  │    │
│  │    │                                     │  ⏱ 3.0h  │          │    │
│  │    │ Desc: Documentar endpoints de...    │  En proceso          │    │
│  │    └─────────────────────────────────────┴──────────────────────┘    │
│  └────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ ☐ │ 🟢  Tests unitarios mod auth            │ Backend │ 10/06 │    │
│  │    │                                     │  ⏱ 4.0h  │          │    │
│  │    │ Desc: Escribir tests para...        │  Ejecutada          │    │
│  │    └─────────────────────────────────────┴──────────────────────┘    │
│  └────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ ☐ │ 🟣  Fix bug login redirect             │ Frontend │ 09/06 │    │
│  │    │                                     │  ⏱ 2.5h  │          │    │
│  │    │ Desc: El login no redirige...       │  Nueva              │    │
│  │    └─────────────────────────────────────┴──────────────────────┘    │
│  └────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  ════════════════════════════════════════════════════════════════════  │
│  ☑ 1 tarea seleccionada                                     [Sincronizar] │
│  (solo visible si hay tareas Ejecutada seleccionadas)                  │
└─────────────────────────────────────────────────────────────────────────┘
```

### Especificaciones

| Elemento | Detalle |
|----------|---------|
| **Encabezado** | Título "Tareas" + botón "+ Nueva tarea" (primario). |
| **Panel de filtros** | Fondo slate-50 (claro) / slate-800 (oscuro). 3 controles: Proyecto (dropdown), Estado (dropdown), Rango fechas (2 datepickers). Botón "Aplicar" que dispara HTMX. |
| **Buscador** | Input con icono de lupa. Filtra por título con debounce 300ms. |
| **Cards de tarea** | Cada card ocupa el ancho completo del contenedor (full-width). Diseño horizontal compacto. |
| **Checkbox** | A la izquierda del card. Para selección múltiple (especialmente para sincronizar). |
| **Indicador de estado** | Círculo de color a la izquierda del título: |
| | 🟣 `Nueva` → indigo-500 |
| | 🟠 `En proceso` → amber-500 |
| | 🟢 `Ejecutada` → emerald-500 |
| | 🔵 `Sincronizada` → sky-500 |
| **Título** | Link al detalle de la tarea (h3 semibold). Si está sincronizada, se muestra en texto normal (no link). |
| **Proyecto** | Badge pequeño con el nombre del proyecto. |
| **Fecha** | Formato dd/mm. |
| **Tiempo** | Icono ⏱ + valor en horas. Si el tiempo fue editado manualmente, mostrar icono ✏️ junto al tiempo. |
| **Descripción** | Texto truncado a 1 línea con ellipsis. |
| **Estado** | Badge con el nombre del estado y color correspondiente. |
| **Tarea sincronizada** | Badge azul + 🔗 ID de Azure DevOps. Card con opacidad reducida. Sin checkbox (no seleccionable). |
| **Tarea manual (tiempo editado)** | Icono ✏️ indicador junto al tiempo. Tooltip: "Tiempo editado manualmente". |
| **Seleccionar todo** | Checkbox en la cabecera de la lista. Selecciona/deselecciona todas las tareas seleccionables (excluye sincronizadas). |
| **Barra de acciones** | Barra inferior fija (o sticky) que aparece cuando hay selección. Muestra conteo + botón "Sincronizar N tareas" si hay ejecutadas seleccionadas. |
| **Paginación / Load more** | Al final de la lista, si hay más resultados: botón "Cargar más" o scroll infinito con HTMX. |

---

## Vista: Crear Tarea

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ← Volver a Tareas                              [Guardar] [Cancelar]   │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
│  ➕ Nueva Tarea                                                        │
│  ═════════════════════════════════════════════════════════════════════  │
│                                                                         │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │                                                                    │ │
│  │  ┌─────────────── LEFT COLUMN ───────────────┬── RIGHT ──────────┐ │
│  │  │                                            │                    │ │
│  │  │  Título *                                  │  Proyecto *        │ │
│  │  │  ┌──────────────────────────────────────┐  │  ┌──────────────┐ │ │
│  │  │  │ Configurar BD de pruebas             │  │  │ Backend    ▼│ │ │
│  │  │  └──────────────────────────────────────┘  │  └──────────────┘ │ │
│  │  │  Máx. 200 caracteres                       │                    │ │
│  │  │                                            │  Estado            │ │
│  │  │  Descripción                               │  ┌──────────────┐ │ │
│  │  │  ┌──────────────────────────────────────┐  │  │ Nueva      ▼│ │ │
│  │  │  │ Crear base de datos PostgreSQL para  │  │  └──────────────┘ │ │
│  │  │  │ los tests unitarios del módulo de    │  │                    │ │
│  │  │  │ autenticación...                     │  │                    │ │
│  │  │  │                                      │  │                    │ │
│  │  │  └──────────────────────────────────────┘  │                    │ │
│  │  │                                            │                    │ │
│  │  │  ─── Rango de fechas ─────                 │                    │ │
│  │  │                                            │                    │ │
│  │  │  Fecha inicio        Fecha fin             │                    │ │
│  │  │  ┌─────────────┐    ┌──────────────┐      │                    │ │
│  │  │  │ 12/06/2026  │    │ 12/06/2026   │      │                    │ │
│  │  │  └─────────────┘    └──────────────┘      │                    │ │
│  │  │                                            │                    │ │
│  │  │  ⏱ Tiempo invertido:  [2.5] horas  ↺     │                    │ │
│  │  │  (calculado automáticamente)              │                    │ │
│  │  │                                            │                    │ │
│  │  └────────────────────────────────────────────┴────────────────────┘ │
│  │                                                                    │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  [Guardar tarea]  [Cancelar]                                            │
└─────────────────────────────────────────────────────────────────────────┘
```

### Especificaciones

| Elemento | Detalle |
|----------|---------|
| **Layout** | 2 columnas: izquierda (campos principales) y derecha (metadatos). En móvil colapsa a 1 columna. |
| **Título** | Input obligatorio, maxlength 200. |
| **Proyecto** | Dropdown con todos los proyectos activos. Obligatorio. |
| **Descripción** | Textarea opcional. |
| **Estado** | Dropdown con estados permitidos. Por defecto "Nueva". Según reglas: se puede saltar de Nueva → Ejecutada directamente. |
| **Fechas** | Dos datepickers. `fecha_fin` debe ser >= `fecha_inicio`. Validación visual (borde rojo si inválido). |
| **Tiempo invertido** | Input numérico. Se actualiza automáticamente al cambiar fechas (HTMX). Icono ↺ indica que se recalcula. Si el usuario escribe manualmente, el icono cambia a ✏️ y se marca como manual. |
| **Botón Guardar** | Primario. Al hacer clic, muestra spinner y deshabilita para evitar doble envío. |
| **Cancelar** | Vuelve a la lista de tareas. |

---

## Vista: Detalle/Edición de Tarea

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ← Volver a Tareas                              [Guardar] [Cancelar]   │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
│  ✏️ Editar Tarea                              (o vista detalle)        │
│  ═════════════════════════════════════════════════════════════════════  │
│                                                                         │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │                                                                    │ │
│  │  ┌─────────────── LEFT COLUMN ───────────────┬── RIGHT ──────────┐ │
│  │  │                                            │                    │ │
│  │  │  Título                                     │  Proyecto         │ │
│  │  │  ┌──────────────────────────────────────┐  │  ┌──────────────┐ │ │
│  │  │  │ Revisión PR #42                      │  │  │ Backend    ▼│ │ │
│  │  │  └──────────────────────────────────────┘  │  └──────────────┘ │ │
│  │  │                                            │                    │ │
│  │  │  Descripción                               │  Estado            │ │
│  │  │  ┌──────────────────────────────────────┐  │  ┌──────────────┐ │ │
│  │  │  │ Revisar y aprobar el pull request    │  │  │ Sincronizada▼│ │ │
│  │  │  │ #42 del módulo de autenticación...   │  │  └──────────────┘ │ │
│  │  │  │                                      │  │  ⛔ Bloqueado     │ │
│  │  │  └──────────────────────────────────────┘  │                    │ │
│  │  │                                            │                    │ │
│  │  │  Fecha inicio       Fecha fin              │  ─── Azure ─────  │ │
│  │  │  ┌─────────────┐  ┌──────────────┐        │                    │ │
│  │  │  │ 11/06/2026  │  │ 11/06/2026   │        │  🔗 ID Azure:      │ │
│  │  │  └─────────────┘  └──────────────┘        │  12345             │ │
│  │  │                                            │                    │ │
│  │  │  ⏱ Tiempo invertido:  [1.0] horas  ✏️    │  📎 HU asociada:   │ │
│  │  │  (editado manualmente)                     │  HUS-987           │ │
│  │  │                                            │                    │ │
│  │  └────────────────────────────────────────────┴────────────────────┘ │
│  │                                                                    │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  ⚠️  Tarea sincronizada — No se puede modificar.                       │
│      Los campos están deshabilitados.                                  │
│                                                                         │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │  ⏱ Historial de tiempo                                             │ │
│  │  ┌──────────────────────────────────────────────────────────────┐  │ │
│  │  │  11/06/2026 — 1.0h (calculado)                              │  │ │
│  │  │  12/06/2026 — 2.5h (editado manualmente por el usuario)     │  │ │
│  │  └──────────────────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  [Guardar cambios]  [Eliminar tarea]                                    │
└─────────────────────────────────────────────────────────────────────────┘
```

### Especificaciones

| Elemento | Detalle |
|----------|---------|
| **Modo vista vs edición** | La misma URL sirve para ambos (`/tareas/{id}`). Si está sincronizada, se muestra en **solo lectura** con campos deshabilitados y banner informativo. Si no, todos los campos son editables. |
| **Estado bloqueado** | Si la tarea está sincronizada, el dropdown de estado muestra "Sincronizada" deshabilitado con icono ⛔. |
| **Campos Azure** | Solo visibles si la tarea tiene `id_azure_devops`. Sección separada. |
| **Tiempo editado manualmente** | Icono ✏️ + texto "(editado manualmente)" en gris. Tooltip con fecha de última modificación. |
| **Historial de tiempo** | Sección expandible que muestra el historial de cambios de tiempo. Sencillo, solo para referencia. |
| **Banner de tarea sincronizada** | Fondo amber-50 con borde amber-200, icono ⚠️. Texto claro: "Esta tarea está sincronizada con Azure DevOps y no puede modificarse." |
| **Botón eliminar** | Solo visible si la tarea NO está sincronizada. Dispara modal de confirmación. |

---

## Estado Vacío

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Tareas                                              [+ Nueva tarea]   │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
│  ┌─────── Filtros ─────────────────────────────────────────────────┐   │
│  │  Proyecto: [Todos ▼]  Estado: [Todos ▼]                        │   │
│  │  Desde: [__]  Hasta: [__]  [Aplicar]                           │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│                                                                         │
│                          📋                                              │
│                                                                         │
│                     No hay tareas registradas                           │
│                                                                         │
│                Registra tu primera tarea para empezar                   │
│                a llevar control de tu trabajo diario.                   │
│                                                                         │
│                      [+ Nueva tarea]                                   │
│                                                                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Empty state con filtros activos

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Tareas                                              [+ Nueva tarea]   │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
│  ┌─────── Filtros ─────────────────────────────────────────────────┐   │
│  │  Proyecto: [Backend ▼]  Estado: [Ejecutada ▼]                  │   │
│  │  Desde: [01/01/2026]  Hasta: [01/03/2026]  [Aplicar]           │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│                                                                         │
│                          🔍                                              │
│                                                                         │
│            No hay tareas con los filtros seleccionados                  │
│                                                                         │
│          Prueba con otros filtros o      [Limpiar filtros]              │
│          crea una nueva tarea.                                          │
│                                                                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Estados de Carga (Skeleton)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Tareas                                              [+ Nueva tarea]   │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
│  ┌─────── Filtros ─────────────────────────────────────────────────┐   │
│  │  ▓▓▓▓▓▓▓▓▓▓   ▓▓▓▓▓▓▓▓▓▓   ▓▓▓▓▓▓   ▓▓▓▓▓▓    ▓▓▓▓▓▓         │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │  ▓ │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓         │ ▓▓▓▓▓▓ │ ▓▓▓▓▓      │    │
│  │    │                                     │ ▓▓▓▓   │             │    │
│  │    │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓           │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓      │    │
│  └────────────────────────────────────────────────────────────────┘    │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │  ▓ │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓         │ ▓▓▓▓▓▓ │ ▓▓▓▓▓      │    │
│  │    │                                     │ ▓▓▓▓   │             │    │
│  │    │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓           │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓      │    │
│  └────────────────────────────────────────────────────────────────┘    │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │  ▓ │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓         │ ▓▓▓▓▓▓ │ ▓▓▓▓▓      │    │
│  │    │                                     │ ▓▓▓▓   │             │    │
│  │    │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓           │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓      │    │
│  └────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Resumen de componentes reutilizados

| Componente | Módulo Proyectos | Módulo Tareas |
|-------------|-----------------|---------------|
| Layout híbrido | ✅ | ✅ (hereda) |
| Cards en lista | ✅ Cards de proyecto | ✅ Cards de tarea (full-width) |
| Página dedicada crear/editar | ✅ | ✅ |
| Formulario 2 columnas | ❌ (simple) | ✅ (más campos) |
| Badges de estado | ✅ Activo/Archivado | ✅ Nueva/En proceso/Ejecutada/Sincronizada |
| Toggle (mostrar archivados) | ✅ | N/A |
| Panel de filtros | ❌ (solo búsqueda) | ✅ (proyecto + estado + fechas) |
| Buscador | ✅ | ✅ |
| Estado vacío | ✅ | ✅ |
| Modal confirmación | ✅ Archivar | ✅ Eliminar tarea |
| Skeleton loading | ✅ | ✅ |
| Barra de selección múltiple | ❌ | ✅ (para sincronizar) |

---

## Documentos relacionados

- [Design System](./UI-design-system.md) — Guía de estilos y componentes
- [Mockups del Módulo Proyectos](./UI-mockups-proyectos.md) — Referencia del layout híbrido
- [Flujos de Navegación - Tareas](./UI-flujos-tareas.md) — Diagramas de interacción
- [Reglas de Negocio](../general/06-Reglas-Negocio.md) — Reglas RN-1, RN-3, RN-4, RN-6, RN-11, RN-12, RN-13, RN-14

---

> **Última actualización:** 22/06/2026  
> **Versión:** 1.0  
> **Estado:** Pendiente de aprobación
