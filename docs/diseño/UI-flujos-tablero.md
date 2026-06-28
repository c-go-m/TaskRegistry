# Flujos de Navegación — Tablero de Control

> Diagramas de interacción para el Tablero de Control de métricas.

---

## Índice

- [Flujo General](#flujo-general)
- [Flujo: Aplicar Filtros](#flujo-aplicar-filtros)
- [Flujo: Colapsar/Expandir Proyectos](#flujo-colapsarexpandir-proyectos)

---

## Flujo General

```mermaid
graph TD
    A[Sidebar: Click "Tablero"] --> B[Vista Tablero]
    
    B --> C[Carga inicial]
    C --> D[Filtros default: semana actual]
    D --> E[GET /tablero con defaults]
    E --> F[Renderiza tarjetas + desglose]
    
    F --> G[Usuario modifica filtros]
    G --> H{Click "Aplicar"?}
    H -->|Sí| I[HTMX GET /tablero con nuevos filtros]
    I --> J[Actualiza tarjetas]
    J --> K[Actualiza desglose]
    K --> F
    
    F --> L[Click cabecera proyecto]
    L --> M[Toggle colapsar/expandir]
    M --> F
    
    F --> N[Click "Limpiar filtros"]
    N --> O[Reset a semana actual + Todos]
    O --> I
```

---

## Flujo: Aplicar Filtros

```mermaid
sequenceDiagram
    actor U as Usuario
    participant T as Tablero
    participant S as Servidor
    participant BD as Base de Datos
    
    U->>T: Modifica fecha "Desde" a 01/06/2026
    U->>T: Modifica fecha "Hasta" a 15/06/2026
    U->>T: Selecciona Proyecto "Backend"
    U->>T: Click "Aplicar"
    
    T->>S: GET /tablero?desde=2026-06-01&hasta=2026-06-15&proyecto_id=1 (HTMX)
    
    S->>BD: SELECT COUNT(*), SUM(tiempo_invertido) FROM tareas WHERE proyecto_id=1 AND fecha_inicio BETWEEN '2026-06-01' AND '2026-06-15'
    BD-->>S: {total_tareas: 4, tiempo_total: 12.5}
    
    S->>BD: SELECT t.*, p.nombre FROM tareas t JOIN proyectos p ON t.proyecto_id=p.id WHERE ... ORDER BY p.nombre, t.fecha_inicio DESC
    BD-->>S: Lista de tareas agrupadas por proyecto
    
    S->>S: Calcula promedios y porcentajes
    S-->>T: HTMX swap: reemplaza #summary-cards y #project-breakdown
    
    T->>U: Tarjetas actualizadas
    T->>U: Desglose actualizado
```

---

## Flujo: Colapsar/Expandir Proyectos

```mermaid
sequenceDiagram
    actor U as Usuario
    participant P as Cabecera Proyecto
    participant C as Contenido (tareas)
    
    Note over U,C: Estado inicial: todos expandidos
    
    U->>P: Click en cabecera "Backend"
    P->>P: Icono ▼ → ▶
    P->>C: x-collapse: contrae contenido
    C->>U: Tareas del proyecto ocultas
    
    U->>P: Click nuevamente
    P->>P: Icono ▶ → ▼
    P->>C: x-collapse: expande contenido
    C->>U: Tareas del proyecto visibles
    
    Note over U,C: No hay llamada al servidor (es solo visual)
    Note over U,C: Al cambiar filtros, todos los proyectos se expanden por defecto
```

---

## Estado de cada pantalla

| Pantalla | Estados |
|----------|---------|
| **Tablero** | Carga inicial (skeleton) → Con datos → Vacío (sin tareas en rango) → Error de carga |

---

## Micro-interacciones

| Interacción | Comportamiento |
|-------------|---------------|
| **Aplicar filtros** | HTMX actualiza tarjetas y desglose sin recargar la página. Transición fade de 200ms. |
| **Colapsar proyecto** | Solo visual (Alpine.js `x-collapse`). Sin llamada al servidor. |
| **Reset filtros** | Botón "Limpiar filtros" restaura valores por defecto y dispara actualización HTMX. |

---

## Documentos relacionados

- [Design System](./UI-design-system.md) — Guía de estilos y componentes
- [Mockups del Tablero de Control](./UI-mockups-tablero.md) — Wireframes detallados

---

> **Última actualización:** 22/06/2026  
> **Versión:** 1.0  
> **Estado:** Aprobado por el usuario
