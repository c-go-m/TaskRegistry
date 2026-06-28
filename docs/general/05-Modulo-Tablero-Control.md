# Módulo 5: Tablero de Control

> Visualización de métricas de tareas y tiempo invertido, filtrable por proyecto y rango de fechas.

---

## Propósito

Proporcionar una vista rápida y clara del trabajo realizado: cuántas tareas se completaron, cuánto tiempo llevaron y cómo se distribuye el esfuerzo entre proyectos.

---

## Filtros disponibles

| Filtro | Tipo | Comportamiento |
|--------|------|----------------|
| **Rango de fechas** | Datepicker (desde / hasta) | Obligatorio. Por defecto: semana actual (lunes a domingo) |
| **Proyecto** | Dropdown | Opcional. "Todos" por defecto. Filtra por proyecto específico |
| **Estado** | Dropdown | Opcional. "Todos" por defecto. Permite filtrar por estado de tarea |

---

## Componentes del tablero

### 1. Tarjetas de resumen

```
┌──────────────┐  ┌──────────────┐  ┌──────────────────┐
│  📋 Tareas   │  │  ⏱ Tiempo   │  │  📊 Promedio     │
│              │  │  total       │  │  por tarea       │
│     42       │  │   68.5 h     │  │   1.63 h         │
└──────────────┘  └──────────────┘  └──────────────────┘
```

| Métrica | Descripción |
|---------|-------------|
| Tareas | Cantidad total de tareas en el rango filtrado |
| Tiempo total | Suma de `tiempo_invertido` de todas las tareas |
| Promedio por tarea | `tiempo_total / cantidad_tareas` |

### 2. Desglose por proyecto (secciones colapsables)

```
▼ Backend (4 tareas — 12.5 h)
  ├─ Configurar BD de pruebas        2.5 h    Ejecutada
  ├─ Revisión PR #42                 1.0 h    Sincronizada
  ├─ Tests unitarios                 4.0 h    Ejecutada
  └─ Refactor módulo auth            5.0 h    Sincronizada

▼ Frontend (3 tareas — 8.0 h)
  ├─ Documentar API                  3.0 h    En proceso
  ├─ Componente tabla                2.5 h    Ejecutada
  └─ Fix bug login                   2.5 h    Ejecutada

═══════════════════════════════════════════════
Total: 7 tareas — 20.5 h
```

Cada sección de proyecto muestra:
- Nombre del proyecto
- Cantidad de tareas en ese proyecto
- Subtototal de tiempo invertido
- Lista de tareas con: título, tiempo, estado

### 3. Tabla detalle completa (opcional)

Debajo del desglose, una tabla plana con todas las tareas filtradas:

| Proyecto | Título | Fecha inicio | Fecha fin | Tiempo | Estado |
|----------|--------|-------------|-----------|--------|--------|
| Backend | Configurar BD | 12/06/2026 | 12/06/2026 | 2.5h | Ejecutada |
| Frontend | Componente tabla | 11/06/2026 | 11/06/2026 | 2.5h | Ejecutada |
| ... | ... | ... | ... | ... | ... |

---

## Vista funcional completa

```
+--------------------------------------------------+
│ 📊 Tablero de Control                             │
+--------------------------------------------------+
│ Filtros:                                          │
│ Desde: [10/06/2026]  Hasta: [17/06/2026]         │
│ Proyecto: [Todos ▼]  Estado: [Todos ▼]  [Aplicar] │
+--------------------------------------------------+
│                                                    │
│ ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │
│ │ Tareas       │  │ Tiempo total │  │ Promedio │ │
│ │      7       │  │    20.5 h    │  │  2.93 h  │ │
│ └──────────────┘  └──────────────┘  └──────────┘ │
│                                                    │
│ ▼ Backend (4 tareas — 12.5 h)                     │
│   ├─ Configurar BD de pruebas     2.5h  Ejecutada │
│   ├─ Revisión PR #42              1.0h  Sincroniz │
│   ├─ Tests unitarios              4.0h  Ejecutada │
│   └─ Refactor módulo auth         5.0h  Sincroniz │
│                                                    │
│ ▼ Frontend (3 tareas — 8.0 h)                     │
│   ├─ Documentar API               3.0h  En proceso│
│   ├─ Componente tabla             2.5h  Ejecutada │
│   └─ Fix bug login                2.5h  Ejecutada │
│                                                    │
+--------------------------------------------------+
```

---

## Notas de diseño

- El tablero debe **actualizarse** al cambiar los filtros sin necesidad de recargar
- Las tarjetas de resumen deben ser visibles **siempre**, incluso si no hay datos (mostrar 0)
- Si no hay tareas en el rango filtrado, mostrar mensaje:
  > "No hay tareas en el rango seleccionado. Prueba con otro filtro."
- El desglose por proyecto debe poder **colapsarse/expandirse** para facilitar la navegación
- Opcional: botón para **exportar** la vista actual a CSV o PDF (fuera de MVP, pero considerar para futura iteración)
