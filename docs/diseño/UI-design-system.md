# UI Design System — TaskRegistry

> Guía de estilos y componentes para la aplicación TaskRegistry.
> Stack: FastAPI + Jinja2/HTMX/Alpine.js + Tailwind CSS v3 + Heroicons.

---

## Índice

- [Paleta de Colores](#paleta-de-colores)
- [Modo Claro / Oscuro](#modo-claro--oscuro)
- [Tipografía](#tipografía)
- [Espaciado y Grid](#espaciado-y-grid)
- [Componentes Base](#componentes-base)
- [Iconografía](#iconografía)
- [Sombras y Elevaciones](#sombras-y-elevaciones)
- [Transiciones y Animaciones](#transiciones-y-animaciones)

---

## Paleta de Colores

### Colores principales

| Token | Color | Tailwind | Hex | Uso |
|-------|-------|----------|-----|-----|
| **Primario** | Indigo | `indigo-500` | `#6366F1` | Botones principales, links, tabs activos |
| Primario claro | Indigo claro | `indigo-50` | `#EEF2FF` | Fondos de sección, hover en sidebar |
| Primario oscuro | Indigo oscuro | `indigo-700` | `#4338CA` | Hover en botones primarios |
| **Secundario** | Teal | `teal-500` | `#14B8A6` | Acentos, badges, highlights |
| Secundario claro | Teal claro | `teal-100` | `#CCFBF1` | Fondos de badges secundarios |
| **Accent** | Amber | `amber-500` | `#F59E0B` | Alertas, advertencias, estrellas |

### Colores semánticos

| Token | Color | Tailwind | Hex | Uso |
|-------|-------|----------|-----|-----|
| **Success** | Emerald | `emerald-500` | `#10B981` | Tareas ejecutadas, operaciones exitosas |
| **Error** | Red | `red-500` | `#EF4444` | Errores, eliminación, campos inválidos |
| **Warning** | Amber | `amber-500` | `#F59E0B` | Advertencias, alertas |
| **Info** | Sky | `sky-500` | `#0EA5E9` | Información, tooltips |
| **Sync (Azure)** | Blue | `blue-500` | `#3B82F6` | Estados sincronizados, conexión Azure |

### Colores neutrales (surface)

| Elemento | Claro | Oscuro |
|----------|-------|--------|
| Fondo página | `slate-50` (`#F8FAFC`) | `slate-900` (`#0F172A`) |
| Superficie (cards) | `white` (`#FFFFFF`) | `slate-800` (`#1E293B`) |
| Superficie elevada | `white` con `shadow` | `slate-750` (`#1a2332`) |
| Sidebar fondo | `white` | `slate-800` |
| Sidebar item hover | `indigo-50` | `slate-700` |
| Sidebar item activo | `indigo-100` | `indigo-900/30` |
| Texto primario | `slate-900` (`#0F172A`) | `slate-100` (`#F1F5F9`) |
| Texto secundario | `slate-500` (`#64748B`) | `slate-400` (`#94A3B8`) |
| Texto terciario | `slate-400` (`#94A3B8`) | `slate-500` (`#64748B`) |
| Bordes | `slate-200` (`#E2E8F0`) | `slate-700` (`#334155`) |
| Divider | `slate-200` (`#E2E8F0`) | `slate-700` (`#334155`) |
| Placeholder input | `slate-400` (`#94A3B8`) | `slate-500` (`#64748B`) |

---

## Modo Claro / Oscuro

### Estrategia

- Clase `dark` en el elemento `<html>` controlada por Alpine.js
- Selector en la topbar (ícono ☀️ / 🌙)
- Persistencia en `localStorage` (`taskregistry-theme`)
- Transición suave: `transition-colors duration-200`
- Sigue la convención **Tailwind dark mode class strategy**

### Estados de badges por tema

| Badge | Claro | Oscuro |
|-------|-------|--------|
| Activo | `bg-emerald-100 text-emerald-700` | `bg-emerald-900/30 text-emerald-400` |
| Archivado | `bg-slate-100 text-slate-600` | `bg-slate-700 text-slate-300` |
| Sincronizado | `bg-sky-100 text-sky-700` | `bg-sky-900/30 text-sky-400` |
| En proceso | `bg-amber-100 text-amber-700` | `bg-amber-900/30 text-amber-400` |
| Nueva | `bg-indigo-100 text-indigo-700` | `bg-indigo-900/30 text-indigo-400` |
| Ejecutada | `bg-emerald-100 text-emerald-700` | `bg-emerald-900/30 text-emerald-400` |

---

## Tipografía

### Familia

```css
font-family: 'Inter', system-ui, -apple-system, sans-serif;
```

### Jerarquía de tamaños

| Nivel | Tailwind | Tamaño | Peso | Uso |
|-------|----------|--------|------|-----|
| **H1** | `text-3xl font-semibold leading-tight` | 30px | SemiBold (600) | Título de página |
| **H2** | `text-2xl font-semibold` | 24px | SemiBold (600) | Título de sección |
| **H3** | `text-xl font-semibold` | 20px | SemiBold (600) | Subtítulo de card |
| **H4** | `text-lg font-medium` | 18px | Medium (500) | Encabezado de grupo |
| **Body** | `text-base` | 16px | Regular (400) | Texto corrido |
| **Body small** | `text-sm` | 14px | Regular (400) | Metadatos, descripciones |
| **Caption** | `text-xs` | 12px | Medium (500) | Badges, etiquetas |
| **Mono** | `font-mono text-sm` | 14px | Regular (400) | IDs, código, rutas |

### Altura de línea

- Tight: `leading-tight` (1.25) — encabezados
- Normal: `leading-normal` (1.5) — cuerpo
- Relaxed: `leading-relaxed` (1.625) — textos largos

---

## Espaciado y Grid

### Sistema de espaciado (Tailwind)

| Token | Valor | Uso |
|-------|-------|-----|
| `p-4` | 16px | Padding interno de cards |
| `p-5` | 20px | Padding interno de cards grandes |
| `p-6` | 24px | Padding de secciones |
| `gap-4` | 16px | Separación en grids |
| `gap-6` | 24px | Separación en grids grandes |
| `space-y-4` | 16px | Separación vertical entre items |
| `space-y-6` | 24px | Separación vertical entre secciones |
| `space-y-8` | 32px | Separación vertical entre bloques grandes |

### Layout de página estándar

```html
<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
  <!-- contenido -->
</div>
```

### Sidebar

| Estado | Ancho |
|--------|-------|
| Expandido | `w-64` (256px) |
| Colapsado | `w-16` (64px) — solo iconos |

### Grid de cards

| Pantalla | Columnas |
|----------|----------|
| Móvil (< 640px) | 1 columna |
| Tablet (640-1024px) | 2 columnas |
| Desktop (> 1024px) | 3 columnas |

---

## Componentes Base

### Botones

#### Primario
```
bg-indigo-600 hover:bg-indigo-700 active:bg-indigo-800
text-white font-medium text-sm
px-4 py-2 rounded-lg
shadow-sm hover:shadow-md
transition-all duration-150
disabled:opacity-50 disabled:cursor-not-allowed
```

#### Secundario (outline)
```
bg-white dark:bg-slate-800
border border-slate-300 dark:border-slate-600
hover:bg-slate-50 dark:hover:bg-slate-700
text-slate-700 dark:text-slate-200 font-medium text-sm
px-4 py-2 rounded-lg
transition-all duration-150
```

#### Terciario (ghost)
```
text-indigo-600 dark:text-indigo-400
hover:text-indigo-700 dark:hover:text-indigo-300
hover:bg-indigo-50 dark:hover:bg-indigo-900/20
font-medium text-sm
px-3 py-2 rounded-lg
transition-all duration-150
```

#### Peligro
```
bg-red-600 hover:bg-red-700 active:bg-red-800
text-white font-medium text-sm
px-4 py-2 rounded-lg
shadow-sm
transition-all duration-150
```

#### Tamaños
| Tamaño | Clases |
|--------|--------|
| xs | `px-2.5 py-1.5 text-xs` |
| sm | `px-3 py-2 text-sm` |
| md (default) | `px-4 py-2 text-sm` |
| lg | `px-6 py-3 text-base` |

---

### Cards

```html
<div class="
  bg-white dark:bg-slate-800
  rounded-xl
  border border-slate-200 dark:border-slate-700
  shadow-sm hover:shadow-md
  transition-all duration-200
  p-5
">
  <!-- contenido -->
</div>
```

### Variantes de card

| Variante | Clases adicionales |
|----------|-------------------|
| Activo (proyecto) | `border-l-4 border-l-indigo-500` |
| Archivado | `opacity-60` |
| Clickable | `cursor-pointer hover:ring-2 hover:ring-indigo-500` |

---

### Inputs

```html
<input
  type="text"
  class="
    w-full
    border border-slate-300 dark:border-slate-600
    rounded-lg
    px-3 py-2 text-sm
    bg-white dark:bg-slate-800
    text-slate-900 dark:text-slate-100
    placeholder:text-slate-400 dark:placeholder:text-slate-500
    focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500
    transition-all duration-150
    disabled:bg-slate-100 dark:disabled:bg-slate-700 disabled:cursor-not-allowed
  "
/>
```

### Grupos de input con label

```html
<div class="space-y-1">
  <label class="block text-sm font-medium text-slate-700 dark:text-slate-300">
    Nombre del proyecto
  </label>
  <input ... />
  <p class="text-xs text-slate-400">Máx. 120 caracteres</p>
</div>
```

---

### Textarea

```html
<textarea
  rows="4"
  class="
    w-full
    border border-slate-300 dark:border-slate-600
    rounded-lg
    px-3 py-2 text-sm
    bg-white dark:bg-slate-800
    text-slate-900 dark:text-slate-100
    placeholder:text-slate-400
    focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500
    transition-all duration-150
    resize-vertical
  "
></textarea>
```

---

### Select / Dropdown

```html
<select
  class="
    w-full
    border border-slate-300 dark:border-slate-600
    rounded-lg
    px-3 py-2 text-sm
    bg-white dark:bg-slate-800
    text-slate-900 dark:text-slate-100
    focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500
    transition-all duration-150
  "
>
  <option value="">Todos</option>
  <option value="activo">Activo</option>
</select>
```

---

### Tabs

```html
<div class="border-b border-slate-200 dark:border-slate-700">
  <nav class="flex space-x-6" role="tablist">
    <button
      class="
        pb-3 text-sm font-medium border-b-2 transition-colors duration-150
        aria-selected:text-indigo-600 aria-selected:border-indigo-600
        aria-selected:dark:text-indigo-400 aria-selected:dark:border-indigo-400
        not-aria-selected:text-slate-500 not-aria-selected:border-transparent
        not-aria-selected:hover:text-slate-700
      "
      role="tab"
      aria-selected="true"
    >
      Tareas
      <span class="ml-2 text-xs text-slate-400">(12)</span>
    </button>
    <button
      class="
        pb-3 text-sm font-medium border-b-2 transition-colors duration-150
        text-slate-500 border-transparent hover:text-slate-700
      "
      role="tab"
      aria-selected="false"
    >
      Documentación
      <span class="ml-2 text-xs text-slate-400">(3)</span>
    </button>
  </nav>
</div>
```

---

### Badges

```html
<span class="
  inline-flex items-center gap-1
  px-2.5 py-0.5 rounded-full
  text-xs font-medium
  {variante}
">
  <!-- icono opcional -->
  Estado
</span>
```

#### Variantes

| Estado | Clases claro | Clases oscuro |
|--------|-------------|---------------|
| Activo | `bg-emerald-100 text-emerald-700` | `bg-emerald-900/30 text-emerald-400` |
| Archivado | `bg-slate-100 text-slate-600` | `bg-slate-700 text-slate-300` |
| Nueva | `bg-indigo-100 text-indigo-700` | `bg-indigo-900/30 text-indigo-400` |
| En proceso | `bg-amber-100 text-amber-700` | `bg-amber-900/30 text-amber-400` |
| Ejecutada | `bg-emerald-100 text-emerald-700` | `bg-emerald-900/30 text-emerald-400` |
| Sincronizada | `bg-sky-100 text-sky-700` | `bg-sky-900/30 text-sky-400` |

---

### Toggle Switch

```html
<button
  x-data="{ on: false }"
  @click="on = !on"
  :class="on ? 'bg-indigo-600' : 'bg-slate-300 dark:bg-slate-600'"
  class="
    relative inline-flex h-6 w-11 items-center rounded-full
    transition-colors duration-200
    focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2
  "
  role="switch"
  :aria-checked="on"
>
  <span
    :class="on ? 'translate-x-6' : 'translate-x-1'"
    class="
      inline-block h-5 w-5 transform rounded-full bg-white shadow-sm
      transition-transform duration-200
    "
  />
</button>
```

---

### Tablas

```html
<div class="overflow-x-auto rounded-lg border border-slate-200 dark:border-slate-700">
  <table class="min-w-full divide-y divide-slate-200 dark:divide-slate-700">
    <thead class="bg-slate-50 dark:bg-slate-800/50">
      <tr>
        <th class="px-4 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
          Título
        </th>
        <th class="px-4 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
          Proyecto
        </th>
        <th class="px-4 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
          Tiempo
        </th>
      </tr>
    </thead>
    <tbody class="divide-y divide-slate-200 dark:divide-slate-700 bg-white dark:bg-slate-800">
      <tr class="hover:bg-slate-50 dark:hover:bg-slate-700/50 transition-colors">
        <td class="px-4 py-3 text-sm text-slate-900 dark:text-slate-100">
          Configurar BD
        </td>
        <td class="px-4 py-3 text-sm text-slate-500">
          Backend
        </td>
        <td class="px-4 py-3 text-sm text-slate-900 dark:text-slate-100">
          2.5h
        </td>
      </tr>
    </tbody>
  </table>
</div>
```

---

### Modales (Confirmación)

```html
<!-- Overlay -->
<div
  x-show="open"
  class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
  @click.away="open = false"
>
  <!-- Modal -->
  <div
    class="
      bg-white dark:bg-slate-800
      rounded-xl shadow-xl
      max-w-md w-full mx-4
      p-6
    "
  >
    <div class="flex items-start gap-4">
      <div class="flex-shrink-0 w-10 h-10 rounded-full bg-amber-100 dark:bg-amber-900/30 flex items-center justify-center">
        <!-- Icono warning -->
      </div>
      <div class="flex-1">
        <h3 class="text-lg font-semibold text-slate-900 dark:text-slate-100">
          ¿Archivar proyecto?
        </h3>
        <p class="mt-2 text-sm text-slate-500">
          Al archivar este proyecto, se ocultará de la vista principal pero sus tareas y documentos se conservarán.
        </p>
      </div>
    </div>
    <div class="mt-6 flex justify-end gap-3">
      <button class="btn-secondary" @click="open = false">Cancelar</button>
      <button class="btn-primary">Archivar</button>
    </div>
  </div>
</div>
```

---

### Tooltips

```html
<div class="relative group">
  <button>ℹ️</button>
  <div
    class="
      absolute bottom-full left-1/2 -translate-x-1/2 mb-2
      px-2 py-1 text-xs font-medium text-white
      bg-slate-800 dark:bg-slate-700
      rounded shadow-sm
      opacity-0 group-hover:opacity-100
      transition-opacity duration-150
      pointer-events-none
      whitespace-nowrap
    "
  >
    Información adicional
  </div>
</div>
```

---

### Estados vacíos (Empty state)

```html
<div class="text-center py-12">
  <!-- Icono ilustrativo (Heroicons) -->
  <svg class="mx-auto h-12 w-12 text-slate-400" ...>
  <h3 class="mt-4 text-lg font-semibold text-slate-900 dark:text-slate-100">
    No hay proyectos aún
  </h3>
  <p class="mt-2 text-sm text-slate-500 max-w-sm mx-auto">
    Crea tu primer proyecto para empezar a registrar tareas y organizar tu trabajo.
  </p>
  <div class="mt-6">
    <button class="btn-primary">+ Nuevo Proyecto</button>
  </div>
</div>
```

---

### Estados de carga (Loading / Skeleton)

```html
<div class="animate-pulse space-y-4">
  <div class="h-4 bg-slate-200 dark:bg-slate-700 rounded w-3/4"></div>
  <div class="h-4 bg-slate-200 dark:bg-slate-700 rounded w-1/2"></div>
  <div class="h-4 bg-slate-200 dark:bg-slate-700 rounded w-2/3"></div>
</div>
```

---

### Toasts / Notificaciones

```html
<div
  x-data="{ show: false }"
  x-init="$watch('show', val => val && setTimeout(() => show = false, 4000))"
  x-show="show"
  class="
    fixed bottom-4 right-4 z-50
    bg-slate-800 dark:bg-slate-700
    text-white text-sm
    px-4 py-3 rounded-lg shadow-lg
    flex items-center gap-3
  "
>
  <!-- Heroicon check/exclamation -->
  <span>Proyecto archivado correctamente</span>
  <button @click="show = false" class="text-slate-400 hover:text-white">&times;</button>
</div>
```

---

## Iconografía

### Librería: **Heroicons** (v2)

- **Outline** (24×24) — Navegación, botones secundarios, enlaces
- **Solid** (20×20) — Acciones principales, estados, badges
- **Mini** (16×16) — Elementos pequeños, etiquetas, metadata

### Tamaños estándar

| Contexto | Tamaño |
|----------|--------|
| Sidebar item | `w-6 h-6` (outline) |
| Acciones en tabla | `w-5 h-5` |
| Botones pequeños | `w-4 h-4` |
| Badges y chips | `w-3 h-3` |
| Estados vacíos | `w-12 h-12` |

### Iconos por módulo

| Módulo | Icono (Outline) | Icono (Solid activo) |
|--------|------------------|----------------------|
| Proyectos | `FolderOpenIcon` | `FolderIcon` |
| Tareas | `ClipboardDocumentListIcon` | `CheckCircleIcon` |
| Tablero | `ChartBarSquareIcon` | `ChartBarIcon` |
| Sincronización | `ArrowPathIcon` | `ArrowPathRoundedSquareIcon` |
| Documentación | `DocumentTextIcon` | `DocumentIcon` |

---

## Sombras y Elevaciones

| Nivel | Tailwind | Uso |
|-------|----------|-----|
| **sm** | `shadow-sm` | Cards, inputs |
| **md** | `shadow-md` | Card hover, sidebar |
| **lg** | `shadow-lg` | Modales, dropdowns |
| **xl** | `shadow-xl` | Modales grandes, notificaciones toast |

---

## Transiciones y Animaciones

### Transiciones estándar

```css
/* Transición general de componentes */
transition-all duration-150 ease-in-out

/* Color mode */
transition-colors duration-200

/* Shadow en hover */
transition-shadow duration-200

/* Sidebar */
transition-width duration-200 ease-in-out
```

### Animaciones de entrada

| Uso | Clase Tailwind |
|-----|---------------|
| Aparición de elementos | `animate-fade-in` |
| Slide down | Tailwind `animate` personalizado |
| Loading | `animate-pulse` |
| Spinner | `animate-spin` |

---

## Accesibilidad (WCAG)

| Requisito | Implementación |
|-----------|---------------|
| **Contraste mínimo** | Ratio 4.5:1 para texto normal, 3:1 para texto grande. Verificado con la paleta elegida. |
| **Focus visible** | `focus:outline-none focus:ring-2 focus:ring-indigo-500` en todos los inputs y botones |
| **Navegación por teclado** | `tabindex` correcto, roles ARIA en tabs (`role="tablist"`, `role="tab"`, `aria-selected`) |
| **Labels asociados** | `label for="id"` o `aria-label` en todos los inputs |
| **Modo oscuro** | Clase `dark` en `<html>` con persistencia en localStorage |
| **Iconos decorativos** | `aria-hidden="true"` en iconos decorativos |
| **Estados** | `disabled`, `aria-disabled`, `aria-current`, `aria-checked` según corresponda |

---

## Documentos relacionados

- [Mockups del Módulo Proyectos](./UI-mockups-proyectos.md)
- [Flujos de Navegación - Proyectos](./UI-flujos-proyectos.md)

---

> **Última actualización:** 22/06/2026  
> **Versión:** 1.0  
> **Estado:** Aprobado por el usuario
