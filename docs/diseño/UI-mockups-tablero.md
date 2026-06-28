# Mockups — Módulo Tablero de Control

> Wireframes y especificaciones visuales para el Tablero de Control de métricas.
> Basado en el Design System definido en [UI-design-system.md](./UI-design-system.md).

---

## Índice

- [Vista: Tablero Completo](#vista-tablero-completo)
- [Componentes](#componentes)
  - [Filtros](#filtros)
  - [Tarjetas de Resumen](#tarjetas-de-resumen)
  - [Desglose por Proyecto](#desglose-por-proyecto)
- [Estados](#estados)
  - [Estado con datos](#estado-con-datos)
  - [Estado vacío](#estado-vacío)
  - [Estado de carga](#estado-de-carga)
- [Micro-interacciones](#micro-interacciones)

---

## Vista: Tablero Completo

```
┌─────────────────────────────────────────────────────────────────────────┐
│  📊 Tablero de Control                                                  │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
│  ┌─────── Filtros ─────────────────────────────────────────────────┐   │
│  │                                                                  │   │
│  │  Desde: [10/06/2026]   Hasta: [17/06/2026]                     │   │
│  │                                                                  │   │
│  │  Proyecto: [Todos           ▼]   Estado: [Todos      ▼]         │   │
│  │                                                                  │   │
│  │  Semana actual: Lun 10 Jun — Dom 16 Jun             [Aplicar]   │   │
│  │                                                                  │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌────────────────────┐  ┌────────────────────┐  ┌──────────────────┐  │
│  │  📋                │  │  ⏱                 │  │  📊              │  │
│  │  Tareas            │  │  Tiempo total      │  │  Promedio        │  │
│  │                    │  │                    │  │                  │  │
│  │       7            │  │      20.5 h        │  │     2.93 h       │  │
│  │                    │  │                    │  │                  │  │
│  │  +2 vs semana ant  │  │  +5.0 h vs ant     │  │  +0.5 h vs ant  │  │
│  └────────────────────┘  └────────────────────┘  └──────────────────┘  │
│                                                                         │
│  ─── Desglose por proyecto ──────────────────────────────────────────  │
│                                                                         │
│  ▼ Backend                                 4 tareas  —  12.5 h  (61%) │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │  🟢 Configurar BD de pruebas                2.5h    12/06       │  │
│  │  🔵 Revisión PR #42                         1.0h    11/06       │  │
│  │  🟢 Tests unitarios mod auth                4.0h    11/06       │  │
│  │  🔵 Refactor módulo auth                    5.0h    10/06       │  │
│  │                                         ─────                     │  │
│  │  Total proyecto:                           12.5h                  │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  ▶ Frontend                                3 tareas  —  5.5 h  (27%) │
│                                                                         │
│  ▼ DevOps                                  2 tareas  —  2.5 h  (12%) │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │  🟠 Configurar pipeline CI/CD              1.5h    12/06       │  │
│  │  🔵 Documentar procesos de release         1.0h    10/06       │  │
│  │                                         ─────                     │  │
│  │  Total proyecto:                            2.5h                  │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                         │
│  ════════════════════════════════════════════════════════════════════  │
│  Total general: 7 tareas  |  20.5 h                                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Componentes

### Filtros

```
┌───────────────────────────────────────────────────────────────────────┐
│                                                                       │
│  Desde: [10/06/2026]   Hasta: [17/06/2026]                          │
│                                                                       │
│  Proyecto: [Todos           ▼]   Estado: [Todos      ▼]              │
│                                                                       │
│  Semana actual: Lun 10 Jun — Dom 16 Jun             [Aplicar]        │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

| Elemento | Especificación |
|----------|---------------|
| **Fondo** | `bg-slate-50 dark:bg-slate-800/50` con borde sutil y `rounded-xl` |
| **Desde / Hasta** | Input date. Default: lunes de la semana actual → domingo de la semana actual |
| **Proyecto** | Dropdown: "Todos" + proyectos activos. |
| **Estado** | Dropdown: "Todos" + 4 estados. |
| **Indicador semanal** | Texto informativo debajo de los datepickers: "Semana actual: Lun 10 Jun — Dom 16 Jun". Ayuda visual para el rango default. |
| **Botón Aplicar** | `btn-primary` tamaño sm. Dispara `GET /tablero?desde=...&hasta=...&proyecto_id=...&estado=...` |

### Tarjetas de Resumen

```
┌────────────────────┐  ┌────────────────────┐  ┌──────────────────┐
│  📋                │  │  ⏱                 │  │  📊              │
│  Tareas            │  │  Tiempo total      │  │  Promedio        │
│                    │  │                    │  │                  │
│       7            │  │      20.5 h        │  │     2.93 h       │
│                    │  │                    │  │                  │
│  +2 vs semana ant  │  │  +5.0 h vs ant     │  │  +0.5 h vs ant  │
└────────────────────┘  └────────────────────┘  └──────────────────┘
```

| Elemento | Especificación |
|----------|---------------|
| **Layout** | 3 columnas en desktop, 2 en tablet, 1 en móvil. `grid grid-cols-1 md:grid-cols-3 gap-4`. |
| **Card** | `bg-white dark:bg-slate-800 rounded-xl border p-5 text-center` |
| **Icono** | Heroicon outline en `w-8 h-8` color `text-indigo-500` |
| **Label** | `text-sm font-medium text-slate-500` |
| **Valor** | `text-3xl font-bold text-slate-900 dark:text-slate-100` |
| **Variación** | `text-xs text-emerald-600` (verde si positiva, red si negativa, oculto si 0). Contenido: "+X vs semana ant" |
| **Borde izquierdo** | Cada card tiene `border-l-4` con color distintivo: Tareas → indigo-500, Tiempo → teal-500, Promedio → amber-500 |

### Desglose por Proyecto

```
▼ Backend                                 4 tareas  —  12.5 h  (61%)
┌──────────────────────────────────────────────────────────────────────┐
│  🟢 Configurar BD de pruebas                2.5h    12/06           │
│  🔵 Revisión PR #42                         1.0h    11/06           │
│  🟢 Tests unitarios mod auth                4.0h    11/06           │
│  🔵 Refactor módulo auth                    5.0h    10/06           │
│                                        ─────                         │
│  Total proyecto:                           12.5h                     │
└──────────────────────────────────────────────────────────────────────┘
```

| Elemento | Especificación |
|----------|---------------|
| **Cabecera** | Clickable. `flex items-center justify-between p-3 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-700/50 transition-colors cursor-pointer` |
| **Icono colapsar** | `▶` / `▼` con `transition-transform duration-200`. Alpine.js `x-collapse` para el contenido. |
| **Nombre proyecto** | `text-base font-semibold text-slate-900 dark:text-slate-100` |
| **Conteo tareas** | `text-sm text-slate-500` |
| **Subtotal tiempo** | `text-sm font-medium text-slate-700 dark:text-slate-300` |
| **Porcentaje** | `text-xs text-slate-400` — muestra % del tiempo total que representa este proyecto |
| **Estado por defecto** | Todos expandidos |
| **Transición colapsar** | `x-collapse.duration.200ms` de Alpine.js |
| **Lista de tareas** | `space-y-1 px-3 pb-3` |
| **Item tarea** | `flex items-center justify-between py-1 text-sm` |
| **Indicador estado** | Círculo de 8px con color según estado. `w-2 h-2 rounded-full inline-block mr-2` |
| **Título tarea** | `text-slate-700 dark:text-slate-300` |
| **Tiempo + fecha** | `text-slate-500 text-xs` |
| **Total proyecto** | `border-t border-slate-200 dark:border-slate-700 pt-2 mt-2 flex justify-between font-medium text-sm text-slate-700 dark:text-slate-300` |

### Total General

```
════════════════════════════════════════════════════════════════════════
Total general: 7 tareas  |  20.5 h
```

| Elemento | Especificación |
|----------|---------------|
| **Estilo** | Línea separadora `border-t-2 border-slate-200 dark:border-slate-700` con padding superior |
| **Texto** | `text-sm font-semibold text-slate-700 dark:text-slate-300 text-right` |

---

## Estados

### Estado con datos

Las tarjetas y el desglose se renderizan con datos reales. Es el estado principal del tablero.

### Estado vacío (sin tareas en el rango)

```
┌────────────────────┐  ┌────────────────────┐  ┌──────────────────┐
│  📋                │  │  ⏱                 │  │  📊              │
│  Tareas            │  │  Tiempo total      │  │  Promedio        │
│                    │  │                    │  │                  │
│       0            │  │       0.0 h        │  │     0.00 h       │
│                    │  │                    │  │                  │
│                    │  │                    │  │                  │
└────────────────────┘  └────────────────────┘  └──────────────────┘

🔍  No hay tareas en el rango seleccionado.

     Prueba con otro filtro o rango de fechas.
```

| Elemento | Especificación |
|----------|---------------|
| **Tarjetas** | Muestran `0`, `0.0 h`, `0.00 h`. Sin variación semanal. |
| **Desglose** | No se renderiza (no hay proyectos con tareas en el rango). |
| **Mensaje vacío** | Heroicon `MagnifyingGlassIcon` + texto centrado. Botón "Limpiar filtros" que resetea a valores por defecto. |

### Estado de carga (skeleton)

```
┌────────────────────┐  ┌────────────────────┐  ┌──────────────────┐
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓   │  │  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓   │  │  ▓▓▓▓▓▓▓▓▓▓▓▓▓  │
│  ▓▓▓▓▓             │  │  ▓▓▓▓▓             │  │  ▓▓▓▓▓           │
│        ▓▓▓         │  │       ▓▓▓▓         │  │       ▓▓▓       │
└────────────────────┘  └────────────────────┘  └──────────────────┘

▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓    ▓▓  ▓▓▓▓▓▓▓    (▓▓%)
▓▓ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓    ▓▓▓     ▓▓▓
▓▓ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓    ▓▓▓     ▓▓▓
                        ─────
▓▓▓▓▓▓▓▓▓▓▓:                    ▓▓▓▓▓
```

| Elemento | Especificación |
|----------|---------------|
| **Tarjetas** | `animate-pulse` con bloques de colores slate-200/700 simulando el texto |
| **Desglose** | 2-3 filas de skeleton simulando las cabeceras de proyecto y sus tareas |

---

## Micro-interacciones

| Interacción | Comportamiento | Implementación |
|-------------|---------------|----------------|
| **Hover en tarjeta** | Sombra `shadow-sm` → `shadow-md`. Transición 150ms. | `transition-shadow duration-150 hover:shadow-md` |
| **Click colapsar/expandir** | Icono rota 180° (▶ → ▼). Contenido se desliza con Alpine.js. | `x-data="{ open: true }"` + `x-collapse` |
| **Aplicar filtros** | Las tarjetas y desglose se actualizan vía HTMX con transición fade. | HTMX `hx-swap` con transición CSS |
| **Variación semanal** | Tooltip al hover: "Semana anterior: X tareas" | Tooltip personalizado con Alpine.js |
| **Número cambia** | Leve animación de escala al actualizarse el valor (cuando cambia con HTMX). | `transition-transform duration-300` |
| **Hover en item de tarea** | Fondo sutil `hover:bg-slate-50 dark:hover:bg-slate-700/30` | `transition-colors duration-150` |

---

## Documentos relacionados

- [Design System](./UI-design-system.md) — Guía de estilos y componentes
- [Flujos del Tablero de Control](./UI-flujos-tablero.md) — Diagramas de interacción
- [Reglas de Negocio](../general/06-Reglas-Negocio.md) — Reglas RN-27

---

> **Última actualización:** 22/06/2026  
> **Versión:** 1.0  
> **Estado:** Aprobado por el usuario
