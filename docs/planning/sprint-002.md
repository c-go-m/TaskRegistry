# Sprint 2A — Infraestructura UI: Tailwind + Base Template + Refactor Proyectos

> **Proyecto:** TaskRegistry
> **Sprint:** 2A (UI Infrastructure — Part 1)
> **Épica asociada:** E-07 (Infraestructura UI/UX)
> **Duración estimada:** 1 sesión
> **Objetivo:** Configurar Tailwind CSS v3, crear el template base Jinja2 (`base.html`), refactorizar todos los templates del módulo Proyectos para que extiendan la base con clases Tailwind, y redirigir la raíz a la interfaz web de Proyectos.

---

## Relación con otras épicas

| Épica | Estado | Dependencia |
|-------|--------|-------------|
| E-01 Configuración | ✅ Completada | Sin cambios |
| E-02 Proyectos (CRUD) | ✅ Completada | **Se refactorizan sus templates** (solo vista, no lógica) |
| E-07 Infraestructura UI | 🆕 En este sprint (Parte 1) | Crea la base para todos los módulos futuros |
| E-03 Tareas | ⏳ Pendiente | Depende de este sprint (usará `base.html`) |

> **Importante:** No se modifica ni el modelo, ni los servicios, ni los endpoints de E-02. Solo se refactoriza la capa de presentación (templates) para usar la nueva infraestructura.

---

## Tareas del Sprint 2A

| # | Tarea | Descripción | Archivos a crear/modificar |
|---|-------|-------------|---------------------------|
| 1 | **Configurar Tailwind CSS CLI** | Instalar Tailwind vía npm, configurar `tailwind.config.js`, crear input CSS, generar output | `package.json`, `tailwind.config.js`, `src/input.css`, `static/css/tailwind.css` (generado), `.gitignore` (mod), `.github/workflows/ci.yml` (mod) |
| 2 | **Crear template base (`base.html`)** | Template base Jinja2 con bloques (`title`, `head_extra`, `content`, `scripts`), carga de HTMX + Alpine.js + Tailwind CSS | `templates/base.html` |
| 3 | **Refactorizar `list.html`** | Migrar a Tailwind + extender `base.html`. Mantener buscador, toggle archivados, grid de cards, HTMX. | `proyectos/templates/proyectos/list.html` |
| 4 | **Refactorizar `form.html`** | Migrar a Tailwind + extender `base.html`. Formulario crear/editar con hints. | `proyectos/templates/proyectos/form.html` |
| 5 | **Refactorizar partials HTMX** | Migrar a Tailwind `_project_grid.html` y `_project_grid_container.html` (no extienden base.html, son partials) | `proyectos/templates/proyectos/_project_grid.html`, `proyectos/templates/proyectos/_project_grid_container.html` |
| 6 | **Limpiar `estilos.css`** | Reducir o eliminar `estilos.css` tras la migración a Tailwind | `static/css/estilos.css` |
| 7 | **Redirigir raíz a Proyectos** | Cambiar raíz de `/docs` a `/proyectos/` | `main.py` (mod) |
| 8 | **Tests de regresión** | Verificar que nada se rompe tras la refactorización | — |

---

## Tarea 1: Configurar Tailwind CSS CLI

### Archivos a crear

#### `package.json`
```json
{
  "name": "taskregistry",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "build:css": "npx @tailwindcss/cli -i ./src/input.css -o ./static/css/tailwind.css --watch",
    "build:css:prod": "npx @tailwindcss/cli -i ./src/input.css -o ./static/css/tailwind.css"
  },
  "devDependencies": {
    "@tailwindcss/cli": "^4.0.0",
    "tailwindcss": "^4.0.0"
  }
}
```

#### `tailwind.config.js`
```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./**/templates/**/*.html",
  ],
  darkMode: "class",  // Activado manualmente por Alpine.js
  theme: {
    extend: {
      colors: {
        primary: {
          50: "#EEF2FF",
          100: "#E0E7FF",
          200: "#C7D2FE",
          300: "#A5B4FC",
          400: "#818CF8",
          500: "#6366F1",
          600: "#4F46E5",
          700: "#4338CA",
          800: "#3730A3",
          900: "#312E81",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "-apple-system", "sans-serif"],
        mono: ["ui-monospace", "Cascadia Code", "Fira Code", "monospace"],
      },
    },
  },
  plugins: [],
};
```

#### `src/input.css`
```css
@import "tailwindcss";
@config "../tailwind.config.js";

/* Estilos personalizados que Tailwind no cubre */
@layer base {
  html {
    scroll-behavior: smooth;
  }
}

@layer utilities {
  .scrollbar-thin {
    scrollbar-width: thin;
  }
}
```

#### Comandos de build
```powershell
cd C:\Repos\Personal\IA\TaskRegistry
npm install
npm run build:css
```

### Archivos a modificar

#### `.gitignore` — Agregar:
```
# Node / Tailwind
node_modules/
src/input.css
```

> Nota: `static/css/tailwind.css` generado **no** se ignora — debe estar en el repo para que CI/CD funcione sin npm.

#### `.github/workflows/ci.yml` — Agregar step de build CSS:
```yaml
- name: Build Tailwind CSS
  run: |
    npm ci
    npm run build:css:prod
```

### Verificación
```powershell
# 1. npm install sin errores
# 2. npm run build:css genera static/css/tailwind.css
# 3. El archivo generado contiene las clases de Tailwind
```

---

## Tarea 2: Crear template base (`templates/base.html`)

### Archivo a crear

#### `templates/base.html`
```html
<!DOCTYPE html>
<html lang="es" x-data="{ dark: localStorage.getItem('taskregistry-theme') === 'dark' }"
      :class="{ 'dark': dark }">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}TaskRegistry{% endblock %}</title>
    <link rel="stylesheet" href="/static/css/tailwind.css">
    {% block head_extra %}{% endblock %}
</head>
<body class="bg-slate-50 dark:bg-slate-900 text-slate-900 dark:text-slate-100 font-sans antialiased min-h-screen transition-colors duration-200">
    <div id="app" class="min-h-screen flex flex-col">
        {# En Sprint 2B aquí se agregará sidebar + topbar #}
        {% block topbar %}{% endblock %}

        <main class="flex-1">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                {% block content %}{% endblock %}
            </div>
        </main>
    </div>

    <script src="https://unpkg.com/htmx.org@1.9.12"
            integrity="sha384-ujb1lZYygJmzgSwoxRggbCHcjc0rB2XoQrxeTUQyRjrOnlCoYta87iKBWq3EsdM2"
            crossorigin="anonymous"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.13.0/dist/cdn.min.js"
            integrity="sha384-+3TqJxN8gJfF2PkH5G0g6Jom5HzGajrFT5NkQ6MGVhKZmF8Xp3+VO2SFL3HneGs"
            crossorigin="anonymous"></script>
    {% block scripts %}{% endblock %}
</body>
</html>
```

### Bloques disponibles para las templates hijas:

| Bloque | Propósito |
|--------|-----------|
| `title` | Título de la pestaña (default: "TaskRegistry") |
| `head_extra` | CSS adicional, meta tags, etc. |
| `topbar` | Barra superior (se implementa en Sprint 2B) |
| `content` | Contenido principal de la página |
| `scripts` | JavaScript adicional al final del body |

### Diseño responsive
- Móvil: padding lateral `px-4`
- Tablet: `sm:px-6`
- Desktop: `lg:px-8`
- Ancho máximo: `max-w-7xl` (1280px)

---

## Tarea 3: Refactorizar `list.html`

### Cambios principales

| Aspecto | Antes (CSS vanilla) | Después (Tailwind) |
|---------|---------------------|--------------------|
| Layout | `<div class="app-container">` | `{% extends "base.html" %}` + bloque `content` |
| Header | `.page-header` | Clases Tailwind: `flex justify-between items-center mb-6 pb-4 border-b border-slate-200 dark:border-slate-700` |
| Título H1 | `.page-header h1` | `text-2xl font-semibold text-slate-900 dark:text-slate-100` |
| Botón primario | `.btn .btn-primary` | `inline-flex items-center gap-1.5 px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-lg shadow-sm hover:bg-indigo-700 transition-colors` |
| Toolbar | `.toolbar` | `flex items-center gap-4 mb-6 flex-wrap` |
| Search input | `.search-input` | `w-full max-w-xs px-3 py-2 pl-9 text-sm border border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all` |
| Grid de cards | `.project-grid` | `grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5` |
| Card | `.project-card` | `bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 border-l-4 border-l-indigo-500 shadow-sm hover:shadow-md hover:-translate-y-0.5 transition-all duration-200 p-5 flex flex-col gap-3 cursor-pointer` |
| Badge activo | `.badge .badge-active` | `inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400` |
| Empty state | `.empty-state` | `text-center py-16` |
| Toggle switch | `.toggle-switch` + JS | Mantener misma estructura pero con clases Tailwind |

### Estructura final esperada

```html
{% extends "base.html" %}

{% block title %}Proyectos - TaskRegistry{% endblock %}

{% block content %}
<div x-data="{ search: '', showArchived: false }">
    <!-- Header -->
    <div class="flex justify-between items-center mb-6 pb-4 border-b border-slate-200 dark:border-slate-700">
        <h1 class="text-2xl font-semibold">Proyectos</h1>
        <a href="/proyectos/nuevo"
           class="inline-flex items-center gap-1.5 px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-lg ..."
           hx-get="/proyectos/nuevo"
           hx-target="#main-content"
           hx-swap="innerHTML">
            + Nuevo Proyecto
        </a>
    </div>

    <!-- Toolbar -->
    <div class="flex items-center gap-4 mb-6 flex-wrap">
        <!-- Search -->
        <div class="relative flex-1 min-w-[200px] max-w-xs">
            <input type="text" x-model="search" placeholder="Buscar proyecto..."
                   class="w-full ..." />
        </div>
        <!-- Toggle -->
        <label class="flex items-center gap-2 text-sm text-slate-500">
            <input type="checkbox" x-model="showArchived" class="sr-only">
            <div class="relative w-11 h-6 rounded-full transition-colors duration-200"
                 :class="showArchived ? 'bg-indigo-600' : 'bg-slate-300 dark:bg-slate-600'">
                <div class="absolute top-0.5 left-0.5 w-5 h-5 rounded-full bg-white shadow-sm transition-transform duration-200"
                     :class="showArchived ? 'translate-x-5' : 'translate-x-0'"></div>
            </div>
            Mostrar archivados
        </label>
    </div>

    <!-- Grid container -->
    <div id="main-content">
        {% include "proyectos/_project_grid_container.html" %}
    </div>
</div>
{% endblock %}
```

### Consideraciones
- El buscador frontend y toggle de archivados se migra de JS vanilla a **Alpine.js** (`x-data`, `x-model`, `x-show`) ya que el DS lo incluye
- Los partials HTMX se mantienen como están pero con clases Tailwind
- El inline JS de `list.html` se puede reubicar en el bloque `scripts`

---

## Tarea 4: Refactorizar `form.html`

### Cambios principales

| Aspecto | Antes (CSS vanilla) | Después (Tailwind) |
|---------|---------------------|--------------------|
| Layout | `<div class="form-container">` | Extiende `base.html`, bloque `content` con `max-w-2xl` |
| Título H2 | `.form-container h2` | `text-xl font-semibold mb-5` |
| Labels | `.form-project label` | `block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5` |
| Inputs | `.form-project input[type="text"]` | `w-full px-3 py-2 text-sm border border-slate-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-800 ...` |
| Botón submit | `.btn .btn-primary` | Mismas clases que en list.html |
| Botón cancelar | `.btn .btn-secondary` | `inline-flex items-center px-4 py-2 text-sm font-medium rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 ...` |

---

## Tarea 5: Refactorizar partials HTMX

### `_project_grid_container.html`
- Wrapper que incluye `_project_grid.html`
- Se mantiene la misma lógica, solo cambian clases CSS a Tailwind

### `_project_grid.html`
- Grid de cards (migrar a Tailwind grid)
- Cada card con clases Tailwind (ver Tarea 3)
- Badges con Tailwind
- Botones de acción con Tailwind

> **Nota:** Los partials **no** extienden `base.html` porque son fragments HTML que se inyectan vía HTMX.

---

## Tarea 6: Limpiar `static/css/estilos.css`

### Estrategia
- Tailwind cubre **todo** el CSS actual (botones, cards, formularios, toggle, grid, empty state)
- Se elimina `estilos.css` por completo
- Si se descubre alguna regla que Tailwind no cubra, se pasa a `src/input.css` en la capa `@layer base` o `@layer utilities`

### Riesgo mitigado
- Los partials HTMX se renderizan con clases Tailwind, no dependen de `estilos.css`
- El layout base ya no referencia `estilos.css`, solo `tailwind.css`

---

## Tarea 7: Redirigir raíz a Proyectos

### Cambio en `main.py`

**Antes:**
```python
@app.get("/")
def root():
    return RedirectResponse(url="/docs")
```

**Después:**
```python
@app.get("/")
def root():
    return RedirectResponse(url="/proyectos/")
```

### Impacto
- Swagger UI sigue disponible en `http://localhost:8000/docs`
- La raíz `http://localhost:8000/` ahora lleva a la interfaz web de proyectos

---

## Tarea 8: Tests de regresión

### Tests existentes que deben seguir pasando
```powershell
pytest -v --cov=proyectos --cov=core
```

### Verificaciones adicionales
| # | Verificación |
|---|-------------|
| 1 | `GET /` redirige a `/proyectos/` (status 200, no 404) |
| 2 | `GET /proyectos/` retorna HTML con `<!DOCTYPE html>` |
| 3 | `GET /proyectos/nuevo` retorna formulario |
| 4 | `GET /proyectos/{id}/editar` retorna formulario precargado |
| 5 | Los partials HTMX se renderizan sin errores |
| 6 | Ruff check pasa sin errores |
| 7 | Los archivos CSS generados existen en `static/css/` |

---

## Criterios de aceptación del Sprint 2A

### Criterios generales (DoD)
- [ ] **TDD**: Toda tarea de código sigue RED → GREEN → REFACTOR
- [ ] **Tests**: Todos los tests existentes pasan con `pytest -v`
- [ ] **Ruff**: `ruff check .` pasa sin errores
- [ ] **Commits**: Siguen Conventional Commits (`feat:`, `test:`, `refactor:`, `docs:`, `chore:`)
- [ ] **Tailwind**: `npm run build:css` genera `static/css/tailwind.css` sin errores

### Criterios funcionales

| # | Criterio | Verificación |
|---|----------|--------------|
| 1 | Tailwind CSS configurado y funcional | `static/css/tailwind.css` existe y las páginas cargan estilos |
| 2 | `base.html` existe con bloques Jinja2 | Templates pueden extenderlo |
| 3 | `list.html` extiende `base.html` y se ve correctamente | Navegador muestra la lista de proyectos con estilos Tailwind |
| 4 | `form.html` extiende `base.html` y se ve correctamente | Formularios crear/editar con estilos Tailwind |
| 5 | Partial HTMX se renderizan con Tailwind | Grid de cards se ve igual o mejor que antes |
| 6 | `GET /` redirige a `/proyectos/` | `curl -sI http://localhost:8000/ | findstr Location` |
| 7 | Sin regresión visual ni funcional | Buscador, toggle, HTMX crear/editar/archivar funcionan igual |
| 8 | `estilos.css` eliminado o reducido al mínimo | No hay dependencia de CSS vanilla |

---

## Orden de implementación sugerido

1. **Tarea 1** → Configurar Tailwind (sin dependencias, necesario para todo lo demás)
2. **Tarea 2** → Crear `base.html` (depende de Tarea 1 para tener el CSS)
3. **Tarea 3** → Refactorizar `list.html` (depende de Tareas 1 y 2)
4. **Tarea 4** → Refactorizar `form.html` (depende de Tareas 1 y 2)
5. **Tarea 5** → Refactorizar partials (depende de Tarea 1)
6. **Tarea 6** → Limpiar `estilos.css` (depende de Tareas 3-5)
7. **Tarea 7** → Redirigir raíz (depende de Tareas 3-5 para que la redirección tenga sentido)
8. **Tarea 8** → Tests de regresión (depende de todas las anteriores)

Cada tarea de código sigue el ciclo **RED → GREEN → REFACTOR**.

---

## Notas de diseño

- **Alpine.js** se introduce en este sprint (aunque se usa más en 2B) porque el toggle de archivados y el buscador se migran de JS vanilla a Alpine.js como parte de la refactorización.
- **Heroicons** no se implementan en este sprint — los iconos en cards y botones se dejan como texto/emojis temporalmente. Los iconos SVG se agregarán en Sprint 2B junto con el sidebar.
- **Modo oscuro**: La clase `dark` en `<html>` ya está preparada en `base.html` con Alpine.js, pero el toggle visual se agrega en Sprint 2B. En este sprint, el modo oscuro funciona si se agrega la clase manualmente desde DevTools.
- **Sin sidebar aún**: El `base.html` tiene un bloque `topbar` vacío y el layout es de una sola columna. En Sprint 2B se agrega la estructura sidebar + topbar.

---

## Referencias

- [Design System](../diseño/UI-design-system.md) — Paleta Indigo, componentes, sidebar specs
- [Mockups Proyectos](../diseño/UI-mockups-proyectos.md) — Referencia visual de las vistas a refactorizar
- [Definition of Done](./definition-of-done.md) — Criterios obligatorios para toda tarea
- [Backlog del proyecto](./backlog.md) — Épica E-07
