# Módulo 4: Sincronización con Azure DevOps

> Permite enviar tareas seleccionadas desde la aplicación hacia Azure DevOps, creando Work Items de tipo Task y asociándolos a una HU existente.

---

## Propósito

Al finalizar la semana (o cuando sea necesario), el usuario puede seleccionar las tareas en estado `Ejecutada` dentro de un rango de fechas y sincronizarlas a Azure DevOps. Esto evita tener que ingresar manualmente cada tarea en Azure DevOps y mantiene la trazabilidad histórica en la aplicación local.

---

## Configuración de conexión

Datos que deben configurarse **una sola vez** y persistirse en la base de datos local:

| Parámetro | Ejemplo | Notas |
|-----------|---------|-------|
| `azure_devops_org_url` | `https://dev.azure.com/mi-organizacion` | URL de la organización |
| `azure_devops_project` | `MiProyecto` | Nombre del proyecto en Azure DevOps |
| `azure_devops_pat` | `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` | Personal Access Token con permisos para crear Work Items |

> **Importante:** El PAT debe almacenarse de forma segura (ej. cifrado en SQLite o en el keychain del sistema operativo).

---

## Flujo de sincronización

```
[Usuario]                          [App]                              [Azure DevOps]
   │                                  │                                     │
   │ 1. Abre vista "Sincronizar"      │                                     │
   │─────────────────────────────────>│                                     │
   │                                  │                                     │
   │ 2. Selecciona rango de fechas    │                                     │
   │─────────────────────────────────>│                                     │
   │                                  │                                     │
   │ 3. App muestra tareas            │                                     │
   │    en estado "Ejecutada"         │                                     │
   │<─────────────────────────────────│                                     │
   │                                  │                                     │
   │ 4. Marca tareas con checkbox     │                                     │
   │ 5. Ingresa ID de HU destino      │                                     │
   │ 6. Presiona "Sincronizar"        │                                     │
   │─────────────────────────────────>│                                     │
   │                                  │ 7. Por cada tarea:                  │
   │                                  │    POST /workitems/$Task            │
   │                                  │────────────────────────────────────>│
   │                                  │    Response: 201 + Work Item ID     │
   │                                  │<────────────────────────────────────│
   │                                  │                                     │
   │                                  │ 8. Guarda ID_azure_devops           │
   │                                  │    y ID_hu_azure_devops             │
   │                                  │ 9. Cambia estado a "Sincronizada"   │
   │                                  │                                     │
   │ 10. Muestra resultado            │                                     │
   │<─────────────────────────────────│                                     │
```

---

## Pantalla funcional de sincronización

```
+--------------------------------------------------+
│ Sincronizar con Azure DevOps                      │
+--------------------------------------------------+
│ Rango de fechas:                                  │
│ Desde: [10/06/2026]  Hasta: [17/06/2026]         │
│                                                   │
│ ID de HU destino (Work Item): [HUS-987   ]        │
│                                                   │
│ Tareas disponibles para sincronizar:              │
│ +------------------------------------------------+│
│ | ☐ | Título              | Proyecto  | Tiempo   |│
│ | ☑ | Configurar BD       | Backend   | 2.5h     |│
│ | ☑ | Revisión PR #42     | Backend   | 1.0h     |│
│ | ☐ | Documentar API      | Frontend  | 3.0h     |│
│ | ☑ | Tests unitarios     | Backend   | 4.0h     |│
│ +------------------------------------------------+│
│                                                   │
│ [Seleccionar todas]  [Deseleccionar todas]        │
│                                                   │
│ ⚠ Las tareas en estado "Ejecutada" aparecen aquí. │
│   Las tareas ya sincronizadas no se muestran.     │
│                                                   │
│ [Sincronizar N tareas seleccionadas]              │
+--------------------------------------------------+
```

---

## Comportamiento ante errores

### Error parcial (fallan algunas tareas)

La sincronización se procesa **tarea por tarea**. Si falla la tarea 3 de 5:

- Las tareas 1 y 2 quedan como `Sincronizada` (ya se crearon en Azure)
- La tarea 3 queda como `Ejecutada` (no se creó en Azure)
- Las tareas 4 y 5 se intentan sincronizar (no se detienen por el error anterior)
- Al finalizar se muestra un resumen:
  ```
  ✅ 4 tareas sincronizadas correctamente
  ❌ 1 tarea falló (Configurar BD) — Error: [mensaje]
  ```

### Error de conexión / autenticación

- Se muestra un mensaje claro indicando el problema
- Ninguna tarea cambia de estado
- Se sugiere verificar la configuración de conexión

---

## Integración técnica (Azure DevOps REST API)

> Información de referencia para el desarrollador.

### Endpoint utilizado

```
POST https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/$Task?api-version=7.0
```

### Headers

```
Authorization: Basic {base64(":" + PAT)}
Content-Type: application/json-patch+json
```

### Body (JSON Patch)

```json
[
  {
    "op": "add",
    "path": "/fields/System.Title",
    "value": "Título de la tarea"
  },
  {
    "op": "add",
    "path": "/fields/System.Description",
    "value": "Descripción de la tarea"
  },
  {
    "op": "add",
    "path": "/relations/-",
    "value": {
      "rel": "System.LinkTypes.Hierarchy-Reverse",
      "url": "https://dev.azure.com/{org}/{project}/_apis/wit/workitems/{HU_ID}"
    }
  }
]
```

### Response exitosa

```
HTTP 201
{
  "id": 12345,
  "rev": 1,
  "fields": {
    "System.Title": "...",
    "System.State": "To Do",
    ...
  },
  "_links": { ... }
}
```

El `id` del response se guarda como `id_azure_devops` en la tarea local.

---

## Notas adicionales

- La sincronización es **solo de subida** (App → Azure). No hay sincronización inversa en el MVP.
- Cada tarea se sincroniza **una sola vez**. Una vez en estado `Sincronizada`, no se puede volver a sincronizar.
- La app guarda un **historial de IDs de HU** usados recientemente para autocompletar en futuras sincronizaciones.
- El campo `id_hu_azure_devops` se almacena en la tarea local para trazabilidad futura.
