# Flujos de Navegación — Módulo Documentación

> Diagramas de interacción para la gestión de documentos de proyectos.

---

## Índice

- [Flujo General](#flujo-general)
- [Flujo: Crear Documento](#flujo-crear-documento)
- [Flujo: Editar Documento](#flujo-editar-documento)
- [Flujo: Abrir Archivo Adjunto](#flujo-abrir-archivo-adjunto)
- [Flujo: Eliminar Documento](#flujo-eliminar-documento)

---

## Flujo General

```mermaid
graph TD
    A[Detalle Proyecto] --> B[Tab "Tareas"]
    A --> C[Tab "Documentación"]
    
    C --> D[Lista de Documentos]
    
    D --> E[Click "+ Nuevo documento"]
    E --> F[Formulario Crear]
    F -->|Guardar| G[Toast "Documento creado"]
    G --> D
    F -->|Cancelar| D
    
    D --> H[Click en card documento]
    H --> I[Detalle/Edición Documento]
    
    I --> J[Modificar campos]
    J -->|Guardar| K[Toast "Documento actualizado"]
    K --> I
    
    I --> L[Agregar archivo]
    L --> M[Selector de archivos nativo]
    M --> N[Lista de archivos actualizada]
    N --> J
    
    I --> O[Click "Abrir" en archivo]
    O --> P[Abre con programa asociado del SO]
    
    I --> Q[Click "Eliminar" en archivo]
    Q --> R[Archivo eliminado de la lista]
    
    I --> S[Click "Eliminar documento"]
    S --> T[Modal confirmación]
    T -->|Confirmar| U[Toast "Documento eliminado"]
    U --> D
    T -->|Cancelar| I
```

---

## Flujo: Crear Documento

```mermaid
sequenceDiagram
    actor U as Usuario
    participant P as Detalle Proyecto
    participant F as Formulario
    participant S as Servidor
    participant BD as Base de Datos
    
    U->>P: Click tab "Documentación"
    U->>P: Click "+ Nuevo documento"
    P->>F: Navegar a /documentos/nuevo?proyecto_id=1
    
    U->>F: Ingresa título (obligatorio)
    U->>F: Ingresa descripción (opcional)
    U->>F: Click "+ Seleccionar archivos"
    F->>U: Selector de archivos nativo
    U->>F: Selecciona 1 o varios archivos
    F->>U: Muestra archivos seleccionados con nombre y tamaño
    
    alt Archivo > 50 MB
        F->>U: ⚠️ Advertencia: "El archivo excede el límite de 50 MB"
    end
    alt Archivo ejecutable (.exe, .bat, .sh)
        F->>U: ⚠️ Advertencia: "Estás adjuntando un archivo ejecutable"
    end
    
    U->>F: Click "Guardar documento"
    F->>S: POST /documentos {titulo, descripcion, proyecto_id, archivos[]}
    S->>BD: INSERT documento
    S->>S: Copia archivos a data/docs/{proyecto_id}/{documento_id}/
    S->>BD: INSERT archivos_adjuntos
    S-->>F: Redirect 303 /proyectos/{id}
    F->>P: Tab Documentación con lista actualizada
    P->>U: Toast "Documento creado correctamente"
```

---

## Flujo: Editar Documento

```mermaid
sequenceDiagram
    actor U as Usuario
    participant D as Lista Documentos
    participant F as Formulario
    participant S as Servidor
    participant BD as Base de Datos
    
    U->>D: Click en card documento
    D->>F: Navegar a /documentos/{id}
    F->>S: GET /documentos/{id}
    S-->>F: Datos del documento + archivos adjuntos
    F->>U: Formulario pre-cargado
    
    U->>F: Modifica título/descripción
    U->>F: Click "🗑️" en archivo existente
    F->>F: Archivo marcado para eliminar
    
    alt Nuevos archivos
        U->>F: Click "+ Agregar archivos"
        F->>U: Selector de archivos
        U->>F: Selecciona nuevos archivos
    end
    
    U->>F: Click "Guardar cambios"
    F->>S: PUT /documentos/{id} {titulo, desc, archivos_eliminar[], archivos_nuevos[]}
    S->>BD: UPDATE documento
    S->>S: Elimina archivos del disco (los marcados)
    S->>BD: DELETE archivos_adjuntos (los marcados)
    S->>S: Copia nuevos archivos al disco
    S->>BD: INSERT archivos_adjuntos (los nuevos)
    S-->>F: Redirect 303 /documentos/{id}
    F->>U: Detalle actualizado + toast "Documento actualizado"
```

---

## Flujo: Abrir Archivo Adjunto

```mermaid
sequenceDiagram
    actor U as Usuario
    participant D as Detalle Documento
    participant SO as Sistema Operativo
    
    U->>D: Click "Abrir" en "consultas_prod.sql"
    D->>SO: Abre ruta local del archivo
    SO->>U: Abre el archivo con el programa asociado (.sql → editor de texto)
```

> **Nota:** No hay llamada al servidor. Es un enlace directo al archivo local (`file:///...`).

---

## Flujo: Eliminar Documento

```mermaid
sequenceDiagram
    actor U as Usuario
    participant D as Detalle Documento
    participant M as Modal
    participant S as Servidor
    participant BD as Base de Datos
    participant DISCO as Sistema Archivos
    
    U->>D: Click "Eliminar documento"
    D->>M: Modal confirmación
    M->>U: "¿Eliminar documento? Los archivos adjuntos también se eliminarán del disco."
    
    U->>M: Click "Eliminar"
    M->>S: DELETE /documentos/{id}
    S->>BD: SELECT archivos_adjuntos WHERE documento_id = ?
    S->>DISCO: Eliminar carpeta data/docs/{proyecto_id}/{documento_id}/
    S->>BD: DELETE archivos_adjuntos WHERE documento_id = ?
    S->>BD: DELETE documento WHERE id = ?
    S-->>M: Redirect 303 /proyectos/{proyecto_id}
    M->>U: Toast "Documento eliminado" + vuelve a la lista
```

---

## Estados de cada pantalla

| Pantalla | Estados |
|----------|---------|
| **Lista documentos (en proyecto)** | Carga → Vacío (sin documentos) → Lista con datos → Error |
| **Detalle/edición documento** | Carga → Formulario editable → Error (documento no encontrado) |
| **Crear documento** | Inicial → Con archivos seleccionados → Guardando → Éxito → Error |

---

## Documentos relacionados

- [Design System](./UI-design-system.md) — Guía de estilos y componentes
- [Mockups del Módulo Documentación](./UI-mockups-documentacion.md) — Wireframes detallados
- [Mockups del Módulo Proyectos](./UI-mockups-proyectos.md) — Vista de detalle donde se integran los tabs
- [Reglas de Negocio](../general/06-Reglas-Negocio.md) — Reglas RN-8, RN-9, RN-17

---

> **Última actualización:** 22/06/2026  
> **Versión:** 1.0  
> **Estado:** Pendiente de aprobación
