# Mockups — Módulo Documentación

> Wireframes y especificaciones visuales para el módulo de Documentación de Proyectos.
> **Nota:** Se accede desde la pestaña "Documentación" en el detalle de cada proyecto.

---

## Índice

- [Vista: Lista de Documentos (dentro del proyecto)](#vista-lista-de-documentos-dentro-del-proyecto)
- [Vista: Detalle/Edición de Documento](#vista-detalleedición-de-documento)
- [Vista: Crear Documento](#vista-crear-documento)
- [Estado Vacío](#estado-vacío)
- [Estados de Carga](#estados-de-carga)

---

## Vista: Lista de Documentos (dentro del proyecto)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ← Volver a Proyectos                         [Editar]  [Archivar]     │
│                                                                         │
│  📁 Backend                                              🟢 Activo     │
│  ═════════════════════════════════════════════════════════════════════  │
│                                                                         │
│  ┌───── Tareas ───────┬────── Documentación ─────────┐                 │
│  │                     │                               │                 │
│  │   (○) Tareas       │   (●) Documentación           │  ← Tab activo  │
│  │                     │                               │                 │
│  │                     │   [+ Nuevo documento]         │                 │
│  │                     │                               │                 │
│  │                     │  ┌────────────────────────────────────────┐   │
│  │                     │  │ 📄 Consultas SQL de producción        │   │
│  │                     │  │ Consultas útiles para troubleshoot    │   │
│  │                     │  │ 📎 3 archivos  ·  12/06/2026         │   │
│  │                     │  └────────────────────────────────────────┘   │
│  │                     │                                               │
│  │                     │  ┌────────────────────────────────────────┐   │
│  │                     │  │ 📄 Información de ambientes            │   │
│  │                     │  │ URLs, credenciales y config ambientes │   │
│  │                     │  │ 📎 1 archivo  ·  10/06/2026           │   │
│  │                     │  └────────────────────────────────────────┘   │
│  │                     │                                               │
│  │                     │  ┌────────────────────────────────────────┐   │
│  │                     │  │ 📄 Guía de deploy                     │   │
│  │                     │  │ Pasos para hacer deploy en cada amb.  │   │
│  │                     │  │ 📎 2 archivos  ·  05/06/2026          │   │
│  │                     │  └────────────────────────────────────────┘   │
│  │                     │                                               │
│  └─────────────────────────────────────────────────────────────────────┘
└─────────────────────────────────────────────────────────────────────────┘
```

### Especificaciones

| Elemento | Detalle |
|----------|---------|
| **Contexto** | Se muestra como el tab "Documentación" dentro de la vista de detalle de proyecto. |
| **Encabezado del tab** | Título "Documentación" + botón "+ Nuevo documento" (primario). |
| **Cards de documento** | Mismo estilo que las cards de proyecto: `bg-white dark:bg-slate-800 rounded-xl border p-5 hover:shadow-md transition-shadow cursor-pointer`. |
| **Icono** | Heroicon `DocumentTextIcon` outline en slate-400. |
| **Título** | Link al detalle del documento. `text-base font-semibold text-indigo-600 dark:text-indigo-400`. |
| **Descripción** | Una línea truncada con ellipsis. `text-sm text-slate-500`. |
| **Metadatos** | 📎 N archivos + fecha de creación. `text-xs text-slate-400`. |
| **Click en card** | Navega a `/documentos/{id}` (detalle del documento). |
| **Grid** | Una columna (full-width cards). Espaciado `space-y-3`. |

---

## Vista: Detalle/Edición de Documento

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ← Volver a Backend / Documentación            [Guardar] [Cancelar]     │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
│  ✏️ Editar Documento                          (o "Detalle Documento")  │
│  ═════════════════════════════════════════════════════════════════════  │
│                                                                         │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │                                                                    │ │
│  │  Título del documento                                             │ │
│  │  ┌──────────────────────────────────────────────────────────────┐  │ │
│  │  │ Consultas SQL de producción                                 │  │ │
│  │  └──────────────────────────────────────────────────────────────┘  │ │
│  │                                                                    │ │
│  │  Descripción                                                      │ │
│  │  ┌──────────────────────────────────────────────────────────────┐  │ │
│  │  │ Consultas útiles para troubleshooting en producción,         │  │ │
│  │  │ incluyendo consultas de rendimiento y monitoreo.             │  │ │
│  │  └──────────────────────────────────────────────────────────────┘  │ │
│  │                                                                    │ │
│  │  ─── Archivos adjuntos ─────────────────────                       │ │
│  │                                                                    │ │
│  │  ┌──────────────────────────────────────────────────────────────┐  │ │
│  │  │  📎 consultas_prod.sql         12.4 KB     [Abrir]    [🗑️]   │  │ │
│  │  │  📎 indices_lentos.sql          3.1 KB     [Abrir]    [🗑️]   │  │ │
│  │  │  📎 stored_procs.sql            8.7 KB     [Abrir]    [🗑️]   │  │ │
│  │  └──────────────────────────────────────────────────────────────┘  │ │
│  │                                                                    │ │
│  │  [+ Agregar archivos]                                             │ │
│  │                                                                    │ │
│  │  ⚠️ Límite: 50 MB por archivo. Archivos ejecutables (.exe,       │ │
│  │     .bat, .sh) mostrarán una advertencia.                         │ │
│  │                                                                    │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  🗓️ Creado: 12/06/2026  ·  Última modificación: 15/06/2026           │
│                                                                         │
│  [Guardar cambios]  [Eliminar documento]                                │
└─────────────────────────────────────────────────────────────────────────┘
```

### Especificaciones

| Elemento | Detalle |
|----------|---------|
| **Layout** | Una sola columna (formulario vertical). Simple y directo. |
| **Título** | Input obligatorio, maxlength 200. |
| **Descripción** | Textarea opcional. |
| **Archivos adjuntos** | Lista de archivos con: icono, nombre, tamaño, botón "Abrir" (abre con programa asociado del SO) y botón eliminar 🗑️. |
| **Agregar archivos** | Botón secundario que abre el selector de archivos nativo (`<input type="file" multiple>`). |
| **Advertencia** | Banner informativo con el límite de 50 MB y advertencia de archivos ejecutables. |
| **Metadatos** | Fechas de creación y última modificación en texto pequeño al final. |
| **Eliminar documento** | Botón peligro. Dispara modal de confirmación: "¿Eliminar documento? Los archivos adjuntos también se eliminarán del disco." |
| **Botón Abrir** | Enlace al archivo local. El navegador lo abre con el programa asociado del SO. |

---

## Vista: Crear Documento

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ← Volver a Backend / Documentación            [Guardar] [Cancelar]     │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
│  ➕ Nuevo Documento                                                    │
│  ═════════════════════════════════════════════════════════════════════  │
│                                                                         │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │                                                                    │ │
│  │  Título del documento *                                           │ │
│  │  ┌──────────────────────────────────────────────────────────────┐  │ │
│  │  │                                                              │  │ │
│  │  └──────────────────────────────────────────────────────────────┘  │ │
│  │  Máx. 200 caracteres                                             │ │
│  │                                                                    │ │
│  │  Descripción (opcional)                                           │ │
│  │  ┌──────────────────────────────────────────────────────────────┐  │ │
│  │  │                                                              │  │ │
│  │  │                                                              │  │ │
│  │  └──────────────────────────────────────────────────────────────┘  │ │
│  │                                                                    │ │
│  │  ─── Archivos adjuntos ─────────────────────                       │ │
│  │                                                                    │ │
│  │  [+ Seleccionar archivos]                                         │ │
│  │  No hay archivos seleccionados                                    │ │
│  │                                                                    │ │
│  │  ⚠️ Límite: 50 MB por archivo. Archivos ejecutables (.exe,       │ │
│  │     .bat, .sh) mostrarán una advertencia.                         │ │
│  │                                                                    │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  [Guardar documento]  [Cancelar]                                        │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Estado Vacío

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ← Volver a Proyectos                                                   │
│                                                                         │
│  📁 Backend                                              🟢 Activo     │
│  ═════════════════════════════════════════════════════════════════════  │
│                                                                         │
│  ┌───── Tareas ───────┬────── Documentación ─────────┐                 │
│  │                     │                               │                 │
│  │   (○) Tareas       │   (●) Documentación           │                 │
│  │                     │                               │                 │
│  │                     │   [+ Nuevo documento]         │                 │
│  │                     │                               │                 │
│  │                     │        📄                      │                 │
│  │                     │                               │                 │
│  │                     │   No hay documentos aún       │                 │
│  │                     │                               │                 │
│  │                     │  Agrega documentación técnica │                 │
│  │                     │  para este proyecto.          │                 │
│  │                     │                               │                 │
│  └─────────────────────────────────────────────────────────────────────┘
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Documentos relacionados

- [Design System](./UI-design-system.md) — Guía de estilos y componentes
- [Mockups del Módulo Proyectos](./UI-mockups-proyectos.md) — Vista de detalle con tabs donde se integra
- [Flujos del Módulo Documentación](./UI-flujos-documentacion.md) — Diagramas de interacción
- [Reglas de Negocio](../general/06-Reglas-Negocio.md) — Reglas RN-8, RN-9, RN-17

---

> **Última actualización:** 22/06/2026  
> **Versión:** 1.0  
> **Estado:** Pendiente de aprobación
