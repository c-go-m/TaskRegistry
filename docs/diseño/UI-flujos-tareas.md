# Flujos de Navegación — Módulo Tareas

> Diagramas de navegación e interacción para el módulo de Registro de Tareas.

---

## Índice

- [Flujo General del Módulo](#flujo-general-del-módulo)
- [Flujo: Crear Tarea](#flujo-crear-tarea)
- [Flujo: Editar Tarea](#flujo-editar-tarea)
- [Flujo: Cambio de Estado](#flujo-cambio-de-estado)
- [Flujo: Tiempo Invertido (Cálculo Automático)](#flujo-tiempo-invertido-cálculo-automático)
- [Flujo: Filtrar y Buscar Tareas](#flujo-filtrar-y-buscar-tareas)
- [Flujo: Selección Múltiple para Sincronizar](#flujo-selección-múltiple-para-sincronizar)
- [Micro-interacciones](#micro-interacciones)

---

## Flujo General del Módulo

```mermaid
graph TD
    A[Sidebar: Click "Tareas"] --> B[Vista Lista Tareas]
    
    B --> C[Panel de Filtros]
    C -->|Aplicar| B
    
    B --> D[Buscador por título]
    D -->|debounce 300ms| B
    
    B --> E[Click "+ Nueva tarea"]
    E --> F[Página Crear Tarea]
    F -->|Guardar| G[Toast: "Tarea creada"]
    G --> B
    F -->|Cancelar| B
    
    B --> H[Click en título de tarea]
    H --> I[Página Detalle/Edición Tarea]
    
    I --> J[Modificar campos]
    J -->|Guardar| K[Toast: "Tarea actualizada"]
    K --> I
    J -->|Cancelar| B
    
    I --> L[Click "Eliminar"]
    L --> M[Modal Confirmación]
    M -->|Confirmar| N[Toast: "Tarea eliminada"]
    N --> B
    M -->|Cancelar| I
    
    B --> O[Seleccionar tareas con checkbox]
    O --> P[Barra acciones: "Sincronizar N"]
    P --> Q[Ir a módulo Sincronización]
    
    B --> R[Cambio rápido de estado desde card]
    R -->|Click badge estado| S[Dropdown inline]
    S -->|Seleccionar nuevo estado| T[HX-PATCH /tareas/{id}/estado]
    T -->|Éxito| B
    T -->|Error| U[Toast error]
```

---

## Flujo: Crear Tarea

```mermaid
sequenceDiagram
    actor U as Usuario
    participant L as Vista Lista
    participant F as Formulario Crear
    participant S as Servidor
    participant BD as Base de Datos
    
    U->>L: Click "+ Nueva tarea"
    L->>F: Navegar a /tareas/nuevo
    F->>S: GET /tareas/nuevo (carga proyectos activos)
    S-->>F: Lista de proyectos para dropdown
    F->>U: Muestra formulario vacío
    
    U->>F: Selecciona proyecto
    U->>F: Ingresa título
    U->>F: Ingresa descripción
    U->>F: Selecciona fecha_inicio y fecha_fin
    F->>S: HTMX POST /tareas/calcular-tiempo (fechas)
    S-->>F: Tiempo calculado en horas
    F->>U: Muestra tiempo calculado en input
    
    U->>F: Ajusta tiempo manualmente (opcional)
    U->>F: Selecciona estado (opcional, default Nueva)
    U->>F: Click "Guardar tarea"
    
    F->>S: POST /tareas {titulo, desc, proyecto_id, fecha_inicio, fecha_fin, tiempo_invertido, estado}
    S->>S: Validaciones:
    S->>S: - título requerido, max 200 chars
    S->>S: - proyecto obligatorio
    S->>S: - fecha_fin >= fecha_inicio
    S->>S: - tiempo_invertido > 0
    
    alt Validación falla
        S-->>F: Error 422 + errores por campo
        F->>U: Muestra errores en rojo bajo cada campo
    else Validación OK
        S->>BD: INSERT tarea
        BD-->>S: tarea_id
        S-->>L: Redirect 303 /tareas
        L->>U: Lista actualizada + toast "Tarea creada"
    end
```

---

## Flujo: Editar Tarea

```mermaid
sequenceDiagram
    actor U as Usuario
    participant L as Vista Lista
    participant D as Página Detalle
    participant S as Servidor
    participant BD as Base de Datos
    
    U->>L: Click título de tarea
    L->>D: Navegar a /tareas/{id}
    D->>S: GET /tareas/{id}
    S-->>D: Datos de la tarea
    
    alt Estado = Sincronizada
        D->>U: Muestra formulario SOLO LECTURA
        D->>U: Banner "Tarea sincronizada - no editable"
        U->>D: No puede modificar nada
        U->>D: Click "← Volver"
    else Estado != Sincronizada
        D->>U: Muestra formulario editable
        
        U->>D: Modifica campos
        U->>D: Click "Guardar cambios"
        
        D->>S: PUT /tareas/{id} {campos modificados}
        S->>S: Validar cambios
        S->>BD: UPDATE tarea SET ... WHERE id=...
        BD-->>S: OK
        S-->>D: Redirect 303 /tareas/{id}
        D->>U: Toast "Tarea actualizada"
    end
```

---

## Flujo: Cambio de Estado

```mermaid
stateDiagram-v2
    [*] --> Nueva: Crear tarea
    Nueva --> En_proceso: Usuario cambia estado
    Nueva --> Ejecutada: Usuario (salto directo)
    En_proceso --> Nueva: Usuario revierte
    En_proceso --> Ejecutada: Usuario completa
    Ejecutada --> Sincronizada: Sistema (sincronización OK)
    
    note right of Sincronizada
        Estado terminal.
        Solo lectura.
        No se puede modificar.
    end note
```

### Transiciones permitidas

```mermaid
sequenceDiagram
    actor U as Usuario
    participant C as Card Tarea
    participant S as Servidor
    participant BD as Base de Datos
    
    U->>C: Click badge estado
    C->>U: Muestra dropdown inline con opciones permitidas
    
    alt Estado actual = Nueva
        C->>U: Opciones: [En proceso] [Ejecutada]
    else Estado actual = En proceso
        C->>U: Opciones: [Nueva] [Ejecutada]
    else Estado actual = Ejecutada
        C->>U: Opciones: [En proceso] (solo si no sincronizada)
    else Estado actual = Sincronizada
        C->>U: Sin opciones (dropdown deshabilitado)
    end
    
    U->>C: Selecciona nuevo estado
    C->>S: HX-PATCH /tareas/{id}/estado {estado: nuevo}
    S->>BD: UPDATE tareas SET estado=... WHERE id=...
    BD-->>S: OK
    S-->>C: HTMX swap: actualiza badge en card
    C->>U: Badge actualizado + toast "Estado actualizado"
```

---

## Flujo: Tiempo Invertido (Cálculo Automático)

```mermaid
sequenceDiagram
    actor U as Usuario
    participant F as Formulario
    participant S as Servidor
    
    Note over U,F: Cálculo automático
    
    U->>F: Cambia fecha_inicio o fecha_fin
    F->>S: POST /tareas/calcular-tiempo (fecha_inicio, fecha_fin)
    S->>S: Calcula diferencia en horas decimales
    S-->>F: {tiempo: 2.5, es_automatico: true}
    F->>U: Muestra tiempo actualizado
    F->>U: Icono ↺ "Calculado automáticamente"
    
    Note over U,F: Edición manual
    
    U->>F: Sobrescribe el valor de tiempo
    F->>F: Marca como "manual"
    F->>U: Icono ✏️ "Editado manualmente"
    F->>U: Hint "Al cambiar fechas se recalculará"
    
    Note over U,F: Recalcular después de manual
    
    U->>F: Cambia fecha_inicio
    F->>S: POST /tareas/calcular-tiempo (fechas)
    S-->>F: {tiempo: 3.0, es_automatico: true}
    F->>U: Muestra nuevo tiempo calculado
    F->>U: Marca como "automático" de nuevo
    F->>U: Hint "Sobrescribir manualmente si es necesario"
```

### Reglas de tiempo

| Situación | Comportamiento |
|-----------|---------------|
| Usuario cambia fechas | Se recalcula automáticamente. El campo se actualiza vía HTMX. |
| Usuario escribe manualmente | Se marca con flag `tiempo_manual=true`. Icono ✏️. |
| Usuario modifica fechas después de manual | Se recalcula. Se pierde el valor manual. Advertencia: "Se recalculará el tiempo" |
| Tiempo editado manualmente en lista | Icono ✏️ al lado del valor. Tooltip explicativo. |

---

## Flujo: Filtrar y Buscar Tareas

```mermaid
sequenceDiagram
    actor U as Usuario
    participant L as Vista Lista
    participant S as Servidor
    participant BD as Base de Datos
    
    Note over U,BD: Filtros combinados
    
    U->>L: Selecciona Proyecto "Backend"
    U->>L: Selecciona Estado "Ejecutada"
    U->>L: Selecciona Desde "01/06/2026" Hasta "15/06/2026"
    U->>L: Click "Aplicar"
    
    L->>S: GET /tareas?proyecto_id=1&estado=Ejecutada&desde=2026-06-01&hasta=2026-06-15
    S->>BD: SELECT ... WHERE proyecto_id=1 AND estado='Ejecutada' AND fecha_inicio BETWEEN ...
    BD-->>S: Resultados filtrados
    S-->>L: HTMX swap: reemplaza #task-list
    
    Note over U,BD: Búsqueda por título
    
    U->>L: Escribe "configurar" en buscador
    L->>S: GET /tareas?q=configurar (con debounce 300ms)
    S->>BD: SELECT ... WHERE titulo LIKE '%configurar%'
    BD-->>S: Resultados
    S-->>L: HTMX swap: reemplaza #task-list
```

### Especificaciones de filtros

| Filtro | Comportamiento | HTMX |
|--------|---------------|------|
| **Proyecto** | Dropdown. Al cambiar, filtra inmediatamente (sin botón Aplicar) | `hx-trigger="change"` |
| **Estado** | Dropdown. Al cambiar, filtra inmediatamente | `hx-trigger="change"` |
| **Fecha desde/hasta** | Datepickers. Requieren click en "Aplicar" | `hx-trigger="click"` en botón |
| **Búsqueda por título** | Input con debounce 300ms | `hx-trigger="keyup changed delay:300ms"` |

---

## Flujo: Selección Múltiple para Sincronizar

```mermaid
sequenceDiagram
    actor U as Usuario
    participant L as Vista Lista
    participant S as Servidor
    participant B as Barra Acciones
    
    Note over U,B: Selección de tareas
    
    U->>L: Click checkbox en tarea Ejecutada
    L->>L: Marca tarea como seleccionada
    
    L->>B: Muestra barra inferior fija
    B->>U: "1 tarea seleccionada" + [Sincronizar]
    
    U->>L: Click checkbox "Seleccionar todo"
    L->>L: Marca todas las tareas Ejecutadas
    
    B->>U: "4 tareas seleccionadas" + [Sincronizar 4]
    
    Note over U,B: Tareas no seleccionables
    
    U->>L: Click en tarea Sincronizada
    L->>U: Checkbox deshabilitado + tooltip "Ya sincronizada"
    
    Note over U,B: Acción de sincronizar
    
    U->>B: Click "Sincronizar 4"
    B->>S: POST /sincronizar/preparar {ids: [1,3,5,7]}
    S-->>B: Redirige a /sincronizacion?ids=1,3,5,7
    B->>U: Navega a módulo Sincronización
```

---

## Micro-interacciones

| Interacción | Comportamiento |
|-------------|---------------|
| **Hover en card de tarea** | Sombra pasa de `shadow-sm` a `shadow-md`. Leve elevación. |
| **Checkbox seleccionado** | Card obtiene borde indigo-500 + fondo indigo-50/10. Transición suave. |
| **Badge de estado clickeable** | Al hacer clic, se expande un dropdown inline con los estados permitidos. |
| **Cambio de estado** | El badge realiza una animación de "flash" (scale 1.1 → 1.0) al actualizarse vía HTMX. |
| **Tiempo editado manualmente** | Icono ↺ → ✏️ con animación de rotación. Tooltip informativo. |
| **Fecha inválida** | Borde rojo con shake suave si fecha_fin < fecha_inicio. |
| **Barra de selección** | Aparece desde abajo con slide-up (200ms). Desaparece si no hay selección. |
| **Tooltip en tarea sincronizada** | Al hacer hover sobre el checkbox deshabilitado: "Esta tarea ya fue sincronizada con Azure DevOps". |
| **Loading en botón Guardar** | Botón muestra spinner + "Guardando..." y se deshabilita. |

---

## Estados de cada pantalla

| Pantalla | Estados |
|----------|---------|
| **Lista de tareas** | Carga (skeleton) → Vacío (sin tareas nunca) → Vacío por filtros (con opción "Limpiar filtros") → Lista con datos → Error de carga |
| **Detalle/edición** | Carga (skeleton) → Formulario editable → Formulario solo lectura (sincronizada) → Error (tarea no encontrada) |
| **Crear tarea** | Inicial → Validación (errores inline) → Calculando tiempo (spinner) → Guardando → Éxito (redirect) → Error servidor |
| **Cambio de estado** | Dropdown cerrado → Dropdown abierto → Actualizando (spinner en badge) → Actualizado (flash) → Error |

---

## Documentos relacionados

- [Design System](./UI-design-system.md) — Guía de estilos y componentes
- [Mockups del Módulo Tareas](./UI-mockups-tareas.md) — Wireframes detallados
- [Mockups del Módulo Proyectos](./UI-mockups-proyectos.md) — Referencia del layout base
- [Reglas de Negocio](../general/06-Reglas-Negocio.md) — Reglas RN-1, RN-3, RN-4, RN-6, RN-11, RN-12, RN-13, RN-14

---

> **Última actualización:** 22/06/2026  
> **Versión:** 1.0  
> **Estado:** Pendiente de aprobación
