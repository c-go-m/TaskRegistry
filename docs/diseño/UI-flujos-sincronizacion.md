# Flujos de Navegación — Sincronización Azure

> Diagramas de interacción para la sincronización de tareas con Azure DevOps.
> **Nota:** Integrado en el módulo de Tareas, no es una página independiente.

---

## Índice

- [Flujo General Integrado](#flujo-general-integrado)
- [Flujo: Activar Filtro Pendientes](#flujo-activar-filtro-pendientes)
- [Flujo: Modal Sincronización](#flujo-modal-sincronización)
- [Flujo: Validación de HU](#flujo-validación-de-hu)
- [Flujo: Progreso de Sincronización](#flujo-progreso-de-sincronización)
- [Flujo: Manejo de Errores](#flujo-manejo-de-errores)

---

## Flujo General Integrado

```mermaid
graph TD
    A[Vista Lista Tareas] --> B[Toggle Pendientes ON]
    B --> C[Filtra tareas Ejecutada]
    
    C --> D[Selecciona tareas con checkbox]
    D --> E[Barra inferior activa]
    E --> F[Click Sincronizar]
    
    F --> G[Abre Modal Sincronización]
    G --> H[Ingresa ID HU]
    H --> I[Click Verificar]
    
    I --> J{HU existe?}
    J -->|Sí| K[✅ HU verificada]
    J -->|No| L[❌ Error HU no existe]
    L --> H
    
    K --> M[Revisa resumen tareas]
    M --> N[Click Sincronizar N tareas]
    
    N --> O[Modal cambia a Progreso]
    O --> P[Tarea por tarea]
    
    P --> Q{Éxito?}
    Q -->|Sí| R[✅ Marca Sincronizada + ID Azure]
    Q -->|No| S[❌ Marca fallo + mensaje error]
    
    R --> T{Siguiente tarea?}
    S --> T
    T -->|Sí| P
    T -->|No| U[Modal Resultado Final]
    
    U --> V[Click Cerrar]
    V --> W[Lista Tareas actualizada con HTMX]
    W --> A
```

---

## Flujo: Activar Filtro Pendientes

```mermaid
sequenceDiagram
    actor U as Usuario
    participant L as Vista Lista
    participant S as Servidor
    participant BD as Base de Datos
    
    U->>L: Activa toggle "Pendientes de sincronizar"
    L->>S: GET /tareas?sync_pendientes=true (HTMX hx-get)
    S->>BD: SELECT * FROM tareas WHERE estado='Ejecutada' ORDER BY fecha_inicio DESC
    BD-->>S: Lista de tareas ejecutadas
    S-->>L: HTMX reemplaza #task-list
    
    Note over U,L: Aparecen solo tareas en estado Ejecutada.
    Note over U,L: Tareas Sincronizadas aún visibles pero con checkbox disabled.
    
    U->>L: Desactiva toggle
    L->>S: GET /tareas (sin filtro pendientes)
    S->>BD: SELECT con filtros normales
    BD-->>S: Resultados
    S-->>L: HTMX reemplaza #task-list
```

---

## Flujo: Modal Sincronización

```mermaid
sequenceDiagram
    actor U as Usuario
    participant L as Lista Tareas
    participant M as Modal
    participant S as Servidor
    participant BD as Base de Datos
    participant AZ as Azure DevOps
    
    U->>L: Selecciona 3 tareas con checkbox
    L->>U: Barra inferior "3 seleccionadas"
    U->>L: Click "Sincronizar"
    
    L->>M: Abre modal con tareas preseleccionadas
    M->>S: GET /sincronizacion/historial-hu
    S->>BD: SELECT DISTINCT id_hu FROM historial_hu ORDER BY ultimo_uso DESC LIMIT 5
    BD-->>S: ["HUS-987", "HUS-452", "HUS-891", "HUS-123"]
    S-->>M: Chips de historial
    
    U->>M: Click chip "HUS-987"
    M->>M: Autocompleta input con "HUS-987"
    
    U->>M: Click "Verificar"
    M->>S: POST /sincronizacion/verificar-hu {id_hu: "HUS-987"}
    
    S->>AZ: GET https://dev.azure.com/{org}/{project}/_apis/wit/workitems/987?api-version=7.0
    alt HU existe
        AZ-->>S: 200 OK {id: 987, fields: {System.Title: "...", System.WorkItemType: "..."}}
        S-->>M: {valida: true, titulo: "Sprint 30 - Backend", tipo: "User Story"}
        M->>U: ✅ Check verde + "HU verificada: Sprint 30 - Backend"
        M->>U: Botón "Sincronizar" habilitado
    else HU no existe o error
        AZ-->>S: 404 Not Found
        S-->>M: {valida: false, error: "HU no encontrada"}
        M->>U: ❌ Error + mensaje explicativo
        M->>U: Botón "Sincronizar" deshabilitado
    end
    
    U->>M: Click "Sincronizar 3 tareas"
    M->>S: POST /sincronizacion/ejecutar {ids: [1, 3, 7], id_hu: "HUS-987"}
    S-->>M: Inicia procesamiento async
```

---

## Flujo: Validación de HU (detalle)

```mermaid
sequenceDiagram
    actor U as Usuario
    participant M as Modal
    participant S as Servidor
    participant AZ as Azure DevOps API
    
    U->>M: Ingresa "HUS-987"
    U->>M: Click "Verificar"
    M->>M: Muestra spinner en botón
    M->>S: POST /sincronizacion/verificar-hu {id_hu: "HUS-987"}
    
    S->>S: Extrae número del ID (987)
    S->>AZ: GET /{org}/{project}/_apis/wit/workitems/987?api-version=7.0
    S->>AZ: Headers: Authorization Basic + PAT
    
    alt 200 OK
        AZ-->>S: {id: 987, fields: {System.WorkItemType: "User Story", System.Title: "Sprint 30 - Backend"}}
        S->>S: Verifica que WorkItemType = "User Story"
        alt Es HU
            S-->>M: {valida: true, titulo: "Sprint 30 - Backend", tipo: "User Story"}
            M->>U: ✅ HU verificada: "Sprint 30 - Backend"
            M->>U: Input borde verde
            M->>U: Botón Sincronizar habilitado
        else No es HU (ej. Task, Bug)
            S-->>M: {valida: false, error: "El ID 987 no es una User Story (es: Task)"}
            M->>U: ⚠️ Advertencia: no es una HU
        end
    else 401 Unauthorized
        AZ-->>S: 401
        S-->>M: {valida: false, error: "Error de autenticación. Verifica tu PAT."}
        M->>U: ❌ Error de autenticación
    else 404 Not Found
        AZ-->>S: 404
        S-->>M: {valida: false, error: "La HU no existe en el proyecto configurado."}
        M->>U: ❌ HU no encontrada
    else Error de conexión
        AZ-->>X: Timeout / Network error
        S-->>M: {valida: false, error: "No se pudo conectar con Azure DevOps."}
        M->>U: ❌ Error de conexión
    end
```

---

## Flujo: Progreso de Sincronización

```mermaid
sequenceDiagram
    participant M as Modal
    participant S as Servidor
    participant BD as Base de Datos
    participant AZ as Azure DevOps API
    
    Note over M,AZ: Por cada tarea seleccionada
    
    S->>M: Actualiza progreso: tarea 1/3
    S->>AZ: POST /{org}/{project}/_apis/wit/workitems/$Task
    S->>AZ: Body: JSON Patch con título, descripción, relación HU
    
    alt 201 Created
        AZ-->>S: {id: 12351, ...}
        S->>BD: UPDATE tareas SET estado='Sincronizada', id_azure_devops=12351, id_hu_azure_devops='HUS-987'
        S->>M: {tarea_id: 1, estado: 'success', id_azure: 12351}
        M->>U: ✅ Configurar BD → ID: 12351
    else Error
        AZ-->>S: 4xx/5xx
        S->>BD: No se actualiza estado (permanece Ejecutada)
        S->>M: {tarea_id: 1, estado: 'error', mensaje: 'Error 401 - No autorizado'}
        M->>U: ❌ Configurar BD → Error: 401
    end
    
    S->>M: Actualiza progreso: tarea 2/3
    S->>AZ: POST /workitems/$Task (siguiente tarea)
    AZ-->>S: 201 {id: 12352}
    S->>BD: UPDATE estado, id_azure_devops
    S-->>M: {estado: 'success', id_azure: 12352}
    
    S->>M: Actualiza progreso: tarea 3/3
    S->>AZ: POST /workitems/$Task
    AZ-->>S: 201 {id: 12353}
    S->>BD: UPDATE estado, id_azure_devops
    S-->>M: {estado: 'success', id_azure: 12353}
    
    S->>BD: INSERT historial_hu (id_hu, ultimo_uso)
    S-->>M: {completado: true, resumen: {exitosas: 3, fallidas: 0}}
    M->>U: ✅ Sincronización completada
```

---

## Flujo: Manejo de Errores

### Error parcial

```mermaid
sequenceDiagram
    participant M as Modal
    participant S as Servidor
    
    Note over M,S: Tarea 1 y 2 OK, tarea 3 falla
    
    S->>M: {tarea_id: 1, estado: 'success', id_azure: 12351}
    S->>M: {tarea_id: 2, estado: 'success', id_azure: 12352}
    S->>M: {tarea_id: 3, estado: 'error', mensaje: 'Error 401 - Token expirado'}
    
    S->>M: {completado: true, resumen: {exitosas: 2, fallidas: 1}}
    
    M->>U: Muestra resultado parcial
    M->>U: "2 sincronizadas | 1 falló"
    M->>U: "Fix bug login → Error 401 - Token expirado"
    M->>U: "Puede reintentarse. Permanecerá como Ejecutada."
```

### Error de conexión (falla total)

```mermaid
sequenceDiagram
    participant M as Modal
    participant S as Servidor
    participant AZ as Azure DevOps
    
    S->>AZ: POST /workitems/$Task (tarea 1)
    AZ-->>S: Timeout / Network error
    
    S->>M: {tarea_id: 1, estado: 'error', mensaje: 'Error de conexión con Azure DevOps'}
    
    S->>AZ: POST /workitems/$Task (tarea 2 - reintenta)
    AZ-->>S: Timeout
    
    S->>M: {tarea_id: 2, estado: 'error', mensaje: 'Error de conexión'}
    
    S->>S: Detiene procesamiento (error de conexión general)
    S->>M: {completado: true, resumen: {exitosas: 0, fallidas: 2}, detenido_por: 'error_conexion'}
    
    M->>U: ❌ Error de conexión
    M->>U: "No se pudo conectar con Azure DevOps."
    M->>U: "Ninguna tarea fue modificada."
    M->>U: "Verifica tu conexión a internet y la configuración en .env"
```

---

## Micro-interacciones

| Interacción | Comportamiento |
|-------------|---------------|
| **Toggle Pendientes** | Slide suave del toggle. El contenido de la lista se desvanece y reaparece (HTMX swap con transición). |
| **Seleccionar tarea** | Card obtiene borde indigo-500 + fondo indigo-50/10. Checkbox se llena. |
| **Barra inferior aparece** | Slide-up desde abajo (200ms) cuando hay >= 1 selección. |
| **Barra inferior desaparece** | Slide-down (200ms) cuando selección = 0. |
| **Click chip HU** | El chip seleccionado se resalta con borde indigo. El valor se copia al input. |
| **Verificar HU** | Spinner en botón + input se pone en estado "verificando..." (borde azul + icono). |
| **Verificación exitosa** | Input borde verde + check ✅ + animación de confirmación. |
| **Verificación fallida** | Input borde rojo + shake + icono ❌. |
| **Tarea sincronizada en progreso** | Aparece con fade-in en la lista del modal. Icono ✅ animado. |
| **Resultado final** | Barra de progreso se completa al 100% con animación. Resumen aparece con fade-in. |
| **Error en tarea** | Fondo rojo suave en la fila + icono ❌ con animación de aparición. |

---

## Estados del Modal

| Estado | Descripción |
|--------|-------------|
| **Inicial** | Input HU vacío, botón "Verificar" deshabilitado, botón "Sincronizar" deshabilitado. Chips de historial visibles. |
| **HU ingresada** | Input con texto, botón "Verificar" habilitado. Sincronizar sigue deshabilitado. |
| **Verificando** | Spinner en botón, input en estado "verificando...", botones deshabilitados. |
| **HU verificada** | Input verde, check ✅, mensaje "HU verificada", botón Sincronizar habilitado. |
| **HU inválida** | Input rojo, mensaje de error, botón Sincronizar deshabilitado. |
| **Sincronizando** | Barra de progreso, lista de tareas con estado en vivo, botón Cancelar. |
| **Completado** | Resumen final, botón Cerrar. |
| **Error total** | Mensaje de error, botón Cerrar. |

---

## Documentos relacionados

- [Design System](./UI-design-system.md) — Guía de estilos y componentes
- [Mockups de Sincronización](./UI-mockups-sincronizacion.md) — Wireframes detallados del modal
- [Mockups del Módulo Tareas](./UI-mockups-tareas.md) — Lista de tareas donde se integra
- [Reglas de Negocio](../general/06-Reglas-Negocio.md) — Reglas RN-5, RN-6, RN-7, RN-19, RN-20, RN-21, RN-22, RN-23
- [ADR Stack Tecnológico](../architecture/ADR-001-stack-tecnologico.md) — FastAPI + Azure DevOps REST API

---

> **Última actualización:** 22/06/2026  
> **Versión:** 1.0  
> **Estado:** Aprobado por el usuario
