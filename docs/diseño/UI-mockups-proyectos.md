# Mockups — Módulo Proyectos

> Wireframes y especificaciones visuales para el módulo de Gestión de Proyectos.
> Basado en el Design System definido en [UI-design-system.md](./UI-design-system.md).

---

## Índice

- [Layout Global (Híbrido)](#layout-global-híbrido)
- [Vista: Lista de Proyectos](#vista-lista-de-proyectos)
- [Vista: Detalle de Proyecto](#vista-detalle-de-proyecto)
- [Vista: Formulario Crear/Editar](#vista-formulario-creareditar)
- [Modal: Confirmación de Archivar](#modal-confirmación-de-archivar)
- [Estado Vacío](#estado-vacío)
- [Estados de Carga](#estados-de-carga)

---

## Layout Global (Híbrido)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ┌──────────┬──────────────────────────────────────────────────────────┐ │
│  │          │  ◁ TaskRegistry                         ☀️  ⚙️  👤      │ │
│  │          │  ───────────── Top Bar ─────────────────────────────────  │ │
│  │          │                                                          │ │
│  │  📂      │  ← Contenido del módulo activo →                        │ │
│  │  Proy.   │                                                          │ │
│  │          │                                                          │ │
│  │  📋      │                                                          │ │
│  │  Tareas  │                                                          │ │
│  │          │                                                          │ │
│  │  📊      │                                                          │ │
│  │  Tablero │                                                          │ │
│  │          │                                                          │ │
│  │  🔄      │                                                          │ │
│  │  Sincr.  │                                                          │ │
│  │          │                                                          │ │
│  │  📁      │                                                          │ │
│  │  Docs    │                                                          │ │
│  │          │                                                          │ │
│  ├──────────┤                                                          │ │
│  │  🎨      │                                                          │ │
│  │  Tema    │                                                          │ │
│  └──────────┴──────────────────────────────────────────────────────────┘ │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Especificaciones

| Elemento | Descripción |
|----------|-------------|
| **Sidebar** | `w-64` expandido, `w-16` colapsado. Fondo blanco (claro) / slate-800 (oscuro). Item activo con fondo indigo-100. Icono + tooltip al colapsar. |
| **Top Bar** | Altura `h-14`. Logo + nombre de la app a la izquierda. Acciones a la derecha: tema (sol/luna), configuración, perfil. |
| **Contenido** | Ocupa el resto del viewport. Padding estándar `p-6`. Scroll vertical si es necesario. |

---

## Vista: Lista de Proyectos

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Proyectos                                            [+ Nuevo]        │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │  🔍  Buscar proyecto...                                      ⌨️  │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  Mostrar archivados     ═══○═══  (toggle indigo-600)                    │
│                                                                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐        │
│  │ 📁 Backend       │  │ 🖥️ Frontend     │  │ 📱 Mobile App   │        │
│  │                 │  │                 │  │                 │        │
│  │ 🟢 Activo       │  │ 🟢 Activo       │  │ 🟢 Activo       │        │
│  │ 12 tareas       │  │  8 tareas       │  │  5 tareas       │        │
│  │                 │  │                 │  │                 │        │
│  │ API REST, BD...  │  │ React, CSS...  │  │ Flutter, Dart.. │        │
│  │                 │  │                 │  │                 │        │
│  │ Última: hace 2h  │  │ Última: hace 1d │  │ Última: hace 3d │        │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘        │
│                                                                         │
│  ┌─────────────────┐  ┌─────────────────┐                              │
│  │ ⚙️ DevOps        │  │ 📊 Data Infra   │                              │
│  │                 │  │                 │                              │
│  │ ⚪ Archivado     │  │ ⚪ Archivado     │  ← Opacos, badge gris      │
│  │  3 tareas       │  │  0 tareas       │                              │
│  │                 │  │                 │                              │
│  │ Terraform, CI..  │  │ Python, SQL...  │                              │
│  │                 │  │                 │                              │
│  │ Última: hace 2s  │  │ Última: hace 1m │                              │
│  └─────────────────┘  └─────────────────┘                              │
└─────────────────────────────────────────────────────────────────────────┘
```

### Especificaciones

| Elemento | Detalle |
|----------|---------|
| **Encabezado** | Título "Proyectos" + botón "+ Nuevo" (primario). Alineación: título a la izquierda, botón a la derecha. |
| **Buscador** | Input con icono de lupa a la izquierda. Placeholder "Buscar proyecto...". Filter inline con HTMX (sin recarga). |
| **Toggle archivados** | Componente switch con label "Mostrar archivados". Por defecto OFF. Al activarlo, se muestran cards de proyectos archivados con opacidad reducida (`opacity-60`). |
| **Cards de proyecto** | 3 columnas en desktop, 2 en tablet, 1 en móvil. Grid Tailwind: `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6`. |
| **Card activo** | Borde izquierdo indigo-500 (`border-l-4 border-l-indigo-500`). Badge verde "Activo". |
| **Card archivado** | Opacidad reducida. Badge gris "Archivado". Aparecen solo con el toggle activado. |
| **Click en card** | Navega a `/proyectos/{id}` (detalle del proyecto). Cursor pointer con hover ring. |
| **Contenido de card** | Nombre (H3), badge estado, conteo tareas, descripción resumida (2 líneas truncadas), última actividad. |
| **Proyectos sin tareas** | Badge "0 tareas" en gris claro. Texto pequeño "Sin actividad aún". |

---

## Vista: Detalle de Proyecto

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ← Volver a Proyectos                     [Editar]  [Archivar]         │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
│  📁 Backend                                              🟢 Activo     │
│  ═════════════════════════════════════════════════════════════════════  │
│                                                                         │
│  API REST, base de datos, infraestructura y servicios del backend.      │
│                                                                         │
│  🗓️ Creado el 10/06/2026   ·   📋 12 tareas   ·   📎 3 documentos      │
│                                                                         │
│  ┌─────────────────┬─────────────────┬─────────────────┐                │
│  │   📋 Tareas     │   ⏱ Tiempo      │   📎 Documentos │                │
│  │     12          │    32.5 h       │      3          │                │
│  └─────────────────┴─────────────────┴─────────────────┘                │
│                                                                         │
│  ┌───── Tareas ───────┬────── Documentación ──────────┐                │
│  │                     │                               │                │
│  │   (●) Tareas       │   (○) Documentación           │  ← Tabs       │
│  │                     │                               │                │
│  │  ┌──────────────────────────────────────────────┐  │                │
│  │  │ Filtros: [Estado] [Fecha]                    │  │                │
│  │  ├──────────────────────────────────────────────┤  │                │
│  │  │ ☐ Configurar BD de pruebas    2.5h  🟢 Ejec. │  │                │
│  │  │ ☐ Revisión PR #42             1.0h  🔵 Sinc. │  │                │
│  │  │ ☐ Tests unitarios             4.0h  🟢 Ejec. │  │                │
│  │  │ ☐ Refactor módulo auth        5.0h  🔵 Sinc. │  │                │
│  │  └──────────────────────────────────────────────┘  │                │
│  │                                                     │                │
│  │  [+ Nueva tarea]                                    │                │
│  └─────────────────────────────────────────────────────┘                │
└─────────────────────────────────────────────────────────────────────────┘
```

### Especificaciones

| Elemento | Detalle |
|----------|---------|
| **Barra de navegación** | "← Volver a Proyectos" (link terciario). Acciones: [Editar] (secundario) + [Archivar] (secundario con icono). |
| **Cabecera del proyecto** | Icono carpeta + nombre (H1). Badge de estado a la derecha. |
| **Metadatos** | Descripción + fecha de creación + conteo de tareas y documentos. |
| **Tarjetas de resumen** | 3 mini-cards con icono + número + label. Fondo indigo-50 en claro, indigo-900/20 en oscuro. |
| **Tabs** | "Tareas" (activo) y "Documentación". El contenido del tab se carga con HTMX. |
| **Panel de tareas (tab activo)** | Tabla de tareas del proyecto con filtros (estado, fechas) + botón "+ Nueva tarea". Checkbox para selección múltiple. |
| **Acciones de proyecto** | Editar → formulario pre-cargado. Archivar → modal de confirmación. |

---

## Vista: Formulario Crear/Editar

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ← Volver                                        [Guardar] [Cancelar]  │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
│  ➕ Nuevo Proyecto                         (ó "Editar Proyecto")       │
│  ═════════════════════════════════════════════════════════════════════  │
│                                                                         │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │                                                                    │ │
│  │  Nombre del proyecto  *                                            │ │
│  │  ┌──────────────────────────────────────────────────────────────┐  │ │
│  │  │ Backend API                                                  │  │ │
│  │  └──────────────────────────────────────────────────────────────┘  │ │
│  │  📝 Máx. 120 caracteres                                           │ │
│  │                                                                    │ │
│  │  Descripción (opcional)                                           │ │
│  │  ┌──────────────────────────────────────────────────────────────┐  │ │
│  │  │ API REST, base de datos, infraestructura y servicios del     │  │ │
│  │  │ backend de la aplicación.                                    │  │ │
│  │  │                                                              │  │ │
│  │  └──────────────────────────────────────────────────────────────┘  │ │
│  │                                                                    │ │
│  │  ┌──────────── SOLO EN EDICIÓN ─────────────────────────────────┐  │ │
│  │  │                                                              │  │ │
│  │  │  Estado                                                      │  │ │
│  │  │  ┌──────────────────────────────────┐                        │  │ │
│  │  │  │ ● Activo    ○ Archivado          │                        │  │ │
│  │  │  └──────────────────────────────────┘                        │  │ │
│  │  │                                                              │  │ │
│  │  └──────────────────────────────────────────────────────────────┘  │ │
│  │                                                                    │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  ⚠️ Al archivar un proyecto se oculta de la vista principal, pero sus  │
│     tareas y documentos se conservan. Puedes volver a activarlo.       │
│                                                                         │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │  [Guardar cambios]                    [Eliminar proyecto]          │ │
│  │                                     (solo si no tiene tareas)     │ │
│  └────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

### Especificaciones

| Elemento | Detalle |
|----------|---------|
| **Modo crear vs editar** | La misma plantilla sirve para ambos. En creación: título "Nuevo Proyecto", sección de estado oculta. En edición: título "Editar Proyecto", sección de estado visible. |
| **Nombre** | Input obligatorio. Validación de máximo 120 caracteres (HTML + backend). Hint text debajo. |
| **Descripción** | Textarea opcional. Sin límite estricto pero sugerencia visual de "texto largo". |
| **Estado (solo edición)** | Radio buttons: Activo / Archivado. Por defecto Activo. |
| **Advertencia de archivo** | Banner informativo con icono ⚠️ en amber, explicando el comportamiento del archivado. |
| **Botón eliminar** | Solo visible en edición. Deshabilitado si el proyecto tiene tareas. Tooltip explicando la restricción. |
| **Guardar** | Botón primario. En creación: "Crear Proyecto". En edición: "Guardar Cambios". |
| **Cancelar** | Botón secundario. Vuelve a la lista de proyectos (o al detalle si es edición). |

---

## Modal: Confirmación de Archivar

```
┌─────────────────────────────────────────────────────────────────────┐
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                                                              │   │
│  │     ⚠️         📁 Archivar "Backend"?                       │   │
│  │                                                              │   │
│  │   Al archivar este proyecto:                                 │   │
│  │                                                              │   │
│  │   ✅ Se ocultará de la lista principal                       │   │
│  │   ✅ Las tareas se conservan                                 │   │
│  │   ✅ Los documentos se conservan                             │   │
│  │   🔄 Puedes reactivarlo en cualquier momento                 │   │
│  │                                                              │   │
│  │  ┌─────────────────┐  ┌─────────────────────┐               │   │
│  │  │   Cancelar       │  │   Archivar proyecto │               │   │
│  │  └─────────────────┘  └─────────────────────┘               │   │
│  │                                                              │   │
│  └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

### Especificaciones

| Elemento | Detalle |
|----------|---------|
| **Overlay** | Fondo negro al 50% de opacidad. Click fuera cierra el modal. |
| **Icono** | Heroicon `ExclamationTriangleIcon` en amber-500, dentro de un círculo amber-100. |
| **Título** | "Archivar proyecto?" con el nombre del proyecto en bold. |
| **Cuerpo** | Lista de consecuencias con iconos de check. |
| **Acciones** | Cancelar (secundario) + Archivar (primario, emerald). |
| **Cierre** | Esc key, click fuera del modal, botón X (opcional). |

---

## Estado Vacío

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Proyectos                                            [+ Nuevo]        │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
│                                                                         │
│                       📂                                                │
//                      📂                                                │
│                                                                         │
│                   No hay proyectos aún                                  │
│                                                                         │
│              Crea tu primer proyecto para empezar                       │
│              a registrar tareas y organizar tu trabajo.                 │
│                                                                         │
│                      [+ Nuevo Proyecto]                                 │
│                                                                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Especificaciones

| Elemento | Detalle |
|----------|---------|
| **Icono** | Heroicon `FolderOpenIcon` en outline, `w-16 h-16`, color slate-300. |
| **Título** | "No hay proyectos aún" en text-lg semibold. |
| **Subtítulo** | Texto descriptivo en text-sm slate-500. |
| **CTA** | Botón primario "+ Nuevo Proyecto" que abre el formulario de creación. |

---

## Estados de Carga

### Skeleton para lista de proyectos

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐      │
│  │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │  │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │  │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │      │
│  │ ▓▓▓▓▓▓           │  │ ▓▓▓▓▓▓           │  │ ▓▓▓▓▓▓           │      │
│  │ ▓▓               │  │ ▓▓               │  │ ▓▓               │      │
│  │ ▓▓▓▓▓▓▓▓▓▓▓      │  │ ▓▓▓▓▓▓▓▓▓▓▓      │  │ ▓▓▓▓▓▓▓▓▓▓▓      │      │
│  │ ▓▓▓▓▓▓           │  │ ▓▓▓▓▓▓           │  │ ▓▓▓▓▓▓           │      │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Especificaciones

| Elemento | Detalle |
|----------|---------|
| **Skeleton** | Cards con `animate-pulse`. Fondos slate-200 en claro, slate-700 en oscuro. |
| **Duración** | Hasta que HTMX complete la carga del contenido. |
| **Transición** | Los skeletons se reemplazan suavemente con `hx-swap-oob` o transición de opacidad. |

---

## Documentos relacionados

- [Design System](./UI-design-system.md) — Guía de estilos y componentes
- [Flujos de Navegación - Proyectos](./UI-flujos-proyectos.md) — Diagramas de interacción
- [Reglas de Negocio](../general/06-Reglas-Negocio.md) — Reglas aplicables a proyectos

---

> **Última actualización:** 22/06/2026  
> **Versión:** 1.0  
> **Estado:** Aprobado por el usuario
