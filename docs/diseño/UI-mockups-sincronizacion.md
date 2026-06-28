# Mockups — Módulo Sincronización Azure

> Especificaciones visuales para la sincronización de tareas con Azure DevOps.
> **Enfoque:** Integrado en la lista de tareas (no módulo separado).

---

## ⚙️ Configuración (Environment Variables)

La conexión con Azure DevOps se configura **exclusivamente vía variables de entorno**, sin UI:

```bash
# .env
AZURE_DEVOPS_ORG_URL=https://dev.azure.com/mi-organizacion
AZURE_DEVOPS_PROJECT=MiProyecto
AZURE_DEVOPS_PAT=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

No se requiere ninguna pantalla de configuración dentro de la app.

---

## 📋 Flujo integrado en la lista de tareas

La sincronización ocurre **dentro del módulo de Tareas**, sin páginas adicionales:

```
Vista Lista Tareas
       │
       ├── [Toggle "Pendientes de sincronizar"]
       │       └── Filtra solo tareas en estado "Ejecutada"
       │
       ├── [Checkbox en tareas]
       │       └── Selecciona tareas a sincronizar
       │
       ├── [Barra inferior "Sincronizar N"]
       │       └── Abre modal
       │             │
       │             ├── Paso 1: Ingresar ID HU + Verificar
       │             ├── Paso 2: Revisar tareas seleccionadas
       │             ├── Paso 3: Click "Sincronizar"
       │             ├── Paso 4: Progreso en vivo
       │             └── Paso 5: Resultados
       │
       └── [Al cerrar modal]
               └── Lista se actualiza (badges → Sincronizada)
```

---

## 🖼️ Wireframe 1: Lista de Tareas con filtro "Pendientes"

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Tareas                                              [+ Nueva tarea]   │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                         │
│  ┌─────── Filtros ─────────────────────────────────────────────────┐   │
│  │                                                                  │   │
│  │  Proyecto: [Todos ▼]    Estado: [Todos ▼]                      │   │
│  │                                                                  │   │
│  │  Desde: [12/06/2026]   Hasta: [19/06/2026]        [Aplicar]    │   │
│  │                                                                  │   │
│  │  🔍 Buscar por título...                                        │   │
│  │                                                                  │   │
│  │  ◉ Pendientes de sincronizar           ← Toggle nuevo           │   │
│  │                                                                  │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ☐ Seleccionar todo                                                    │
│                                                                         │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ ☑ │ 🟢  Configurar BD de pruebas        │  Backend │ 12/06    │    │
│  │    │                                     │  ⏱ 2.5h  │          │    │
│  │    │ Desc: Crear base de datos para...   │  🔄 Pend. sync     │    │
│  └────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ ☑ │ 🟢  Tests unitarios mod auth            │  Backend │ 11/06 │    │
│  │    │                                     │  ⏱ 4.0h  │          │    │
│  │    │ Desc: Escribir tests para...        │  🔄 Pend. sync     │    │
│  └────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ ☑ │ 🟢  Fix bug login redirect             │  Frontend │ 10/06│    │
│  │    │                                     │  ⏱ 2.5h  │          │    │
│  │    │ Desc: El login no redirige...        │  🔄 Pend. sync     │    │
│  └────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  ┌────────────────────────────────────────────────────────────────┐    │
│  │ ☐ │ 🔵  Revisión PR #42                  │  Backend │ 11/06    │    │
│  │    │                                     │  ⏱ 1.0h  │          │    │
│  │    │ Desc: Revisar pull request...       │  🔗 Sincronizada   │    │
│  │    │                                     │  ID: 12345         │    │
│  └────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  ════════════════════════════════════════════════════════════════════  │
│  ☑ 3 tareas seleccionadas                             [Sincronizar]   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Comportamiento del toggle "Pendientes de sincronizar"

| Estado | Comportamiento |
|--------|---------------|
| **OFF (default)** | Lista normal de tareas con todos los filtros habituales |
| **ON** | Se añade filtro `estado=Ejecutada`. Las tareas `Sincronizada` se muestran igual pero con checkbox deshabilitado para distinguir las ya sincronizadas |
| **Combinación con otros filtros** | El toggle se suma a los filtros existentes. Si ya hay un filtro de estado, el toggle lo sobreescribe a `Ejecutada` |

---

## 🪟 Wireframe 2: Modal — Ingresar ID de HU

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│     ┌─────────────────────────────────────────────────────────┐     │
│     │                                                         │     │
│     │   🔄  Sincronizar con Azure DevOps                      │     │
│     │   ──────────────────────────────────────────────────    │     │
│     │                                                         │     │
│     │   ID de HU destino *                                    │     │
│     │   ┌────────────────────────────────────────────────┐    │     │
│     │   │  HUS-987                              [Verificar] │    │     │
│     │   └────────────────────────────────────────────────┘    │     │
│     │                                                         │     │
│     │   📋 Últimas HUs usadas:                                │     │
│     │   [HUS-987] [HUS-452] [HUS-891] [HUS-123]              │     │
│     │                                                         │     │
│     │   ── Tareas a sincronizar (3) ────                      │     │
│     │                                                         │     │
│     │   ┌─────────────────────────────────────────────────┐   │     │
│     │   │  🟢 Configurar BD de pruebas           2.5h    │   │     │
│     │   │  🟢 Tests unitarios mod auth           4.0h    │   │     │
│     │   │  🟢 Fix bug login redirect             2.5h    │   │     │
│     │   │                                         ─────  │   │     │
│     │   │  Total:                                9.0h    │   │     │
│     │   └─────────────────────────────────────────────────┘   │     │
│     │                                                         │     │
│     │   ⚠️  Las tareas se marcarán como "Sincronizada"       │     │
│     │      y quedarán en solo lectura.                        │     │
│     │                                                         │     │
│     │  ┌──────────────────┐  ┌────────────────────────────┐   │     │
│     │  │    Cancelar       │  │  Sincronizar 3 tareas     │   │     │
│     │  └──────────────────┘  └────────────────────────────┘   │     │
│     │                        (deshabilitado hasta verificar)  │     │
│     └─────────────────────────────────────────────────────────┘     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Botón "Verificar"

| Estado | Comportamiento |
|--------|---------------|
| **Input vacío** | Botón deshabilitado |
| **Click "Verificar"** | Spinner en botón + llamada a Azure DevOps REST API para validar que el Work Item existe y es una HU |
| **HU existe** | ✅ Check verde + Tooltip "HU verificada — HUS-987" + Botón "Sincronizar" se habilita |
| **HU no existe** | ❌ Borde rojo + Tooltip "La HU HUS-987 no existe en Azure DevOps. Verifica el ID." |
| **Error de conexión** | ⚠️ Warning + "No se pudo conectar con Azure DevOps. Verifica tu conexión y configuración." |

---

## 🔄 Wireframe 3: Modal — Progreso de Sincronización

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│     ┌─────────────────────────────────────────────────────────┐     │
│     │                                                         │     │
│     │   🔄  Sincronizando con Azure DevOps...                 │     │
│     │   ──────────────────────────────────────────────────    │     │
│     │                                                         │     │
│     │   HU destino: HUS-987                                   │     │
│     │                                                         │     │
│     │   ┌─────────────────────────────────────────────────┐   │     │
│     │   │  ███████████████████░░░░░░░░░░░░░  60%          │   │     │
│     │   │  2 de 3 tareas sincronizadas                     │   │     │
│     │   └─────────────────────────────────────────────────┘   │     │
│     │                                                         │     │
│     │   ✅  Configurar BD de pruebas         ✔️ ID: 12351     │     │
│     │   ✅  Tests unitarios mod auth         ✔️ ID: 12352     │     │
│     │   🔄  Fix bug login redirect          ⏳ enviando...   │     │ ← animación
│     │                                                         │     │
│     │  ┌────────────────────────────┐                         │     │
│     │  │    Cancelar (no recomendado) │                       │     │
│     │  └────────────────────────────┘                         │     │
│     └─────────────────────────────────────────────────────────┘     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Comportamiento del progreso

| Elemento | Detalle |
|----------|---------|
| **Barra de progreso** | Indeterminada mientras se procesa. Muestra porcentaje (tareas completadas / total). |
| **Ítem completado** | ✅ Check verde + "ID: 12351" devuelto por Azure DevOps. |
| **Ítem en progreso** | 🔄 Spinner + "enviando..." |
| **Ítem pendiente** | ⏳ Sin ícono, atenuado. |
| **Ítem fallido** | ❌ Cruz roja + mensaje de error. Tarea permanece en estado `Ejecutada`. |
| **Cancelar** | Botón secundario atenuado con advertencia "No recomendado: las tareas ya enviadas quedarán sincronizadas". Detiene el procesamiento de las restantes. |

---

## ✅ Wireframe 4: Modal — Resultado Final

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│     ┌─────────────────────────────────────────────────────────┐     │
│     │                                                         │     │
│     │   ✅  Sincronización completada                         │     │
│     │   ──────────────────────────────────────────────────    │     │
│     │                                                         │     │
│     │   HU destino: HUS-987                                   │     │
│     │                                                         │     │
│     │   ┌─────────────────────────────────────────────────┐   │     │
│     │   │  ✅ Configurar BD de pruebas   → ID: 12351     │   │     │
│     │   │  ✅ Tests unitarios mod auth   → ID: 12352     │   │     │
│     │   │  ❌ Fix bug login redirect     → Error: 401    │   │     │
│     │   │                                No autorizado   │   │     │
│     │   └─────────────────────────────────────────────────┘   │     │
│     │                                                         │     │
│     │   ─────────────────────────────────────                 │     │
│     │   ✅ 2 sincronizadas  |  ❌ 1 falló                     │     │
│     │                                                         │     │
│     │   ❓ La tarea "Fix bug login" puede                     │     │
│     │      reintentarse cuando resuelvas el error.            │     │
│     │      Permanecerá en estado "Ejecutada".                 │     │
│     │                                                         │     │
│     │  ┌──────────────────────────────┐                       │     │
│     │  │         Cerrar               │                       │     │
│     │  └──────────────────────────────┘                       │     │
│     │                                                         │     │
│     └─────────────────────────────────────────────────────────┘     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Resultados posibles

| Escenario | Mensaje |
|-----------|---------|
| **Todo OK** | 🎉 "3 tareas sincronizadas correctamente" + botón "Cerrar" |
| **Error parcial** | ⚠️ "2 sincronizadas | 1 falló" + detalle del error + "La tarea fallida puede reintentarse" |
| **Error total** | ❌ "No se pudo sincronizar ninguna tarea" + "Verifica tu conexión y configuración de Azure DevOps" |
| **Error de autenticación** | ❌ "Error de autenticación. Verifica tu PAT de Azure DevOps." |

---

## 🪟 Wireframe 5: Modal — Mensaje de error (HU no existe)

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│     ┌─────────────────────────────────────────────────────────┐     │
│     │                                                         │     │
│     │   ❌  HU no encontrada                                 │     │
│     │   ──────────────────────────────────────────────────    │     │
│     │                                                         │     │
│     │   La HU "HUS-999" no existe en el proyecto              │     │
│     │   "MiProyecto" de Azure DevOps.                         │     │
│     │                                                         │     │
│     │   Posibles causas:                                      │     │
│     │   • El ID es incorrecto                                 │     │
│     │   • La HU está en otro proyecto                         │     │
│     │   • No tienes permisos para verla                       │     │
│     │                                                         │     │
│     │  ┌──────────────────┐                                   │     │
│     │  │     Cerrar        │                                   │     │
│     │  └──────────────────┘                                   │     │
│     │                                                         │     │
│     └─────────────────────────────────────────────────────────┘     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📝 Consideraciones adicionales

| Aspecto | Decisión |
|---------|----------|
| **¿Dónde se configura?** | Solo `.env` (AZURE_DEVOPS_ORG_URL, AZURE_DEVOPS_PROJECT, AZURE_DEVOPS_PAT) |
| **Validación HU** | Botón "Verificar" en el modal que consulta Azure DevOps REST API. Si falla, muestra error y no habilita "Sincronizar". |
| **Historial HU** | Tabla `historial_hu` en SQLite. Últimos 5 IDs como chips. Se actualiza después de cada sincronización exitosa. |
| **Procesamiento** | Tarea por tarea (no batch). Si falla una, las siguientes se intentan igual. |
| **Tiempo de espera** | Timeout de 30s por tarea. Si excede, se marca como fallida y continúa. |
| **¿Qué pasa si cierro el modal?** | Si está en progreso: las tareas ya enviadas quedan sincronizadas. Las pendientes/no enviadas quedan ejecutadas. |

---

## Documentos relacionados

- [Design System](./UI-design-system.md) — Guía de estilos y componentes
- [Mockups del Módulo Tareas](./UI-mockups-tareas.md) — Lista de tareas base donde se integra la sincronización
- [Flujos de Sincronización](./UI-flujos-sincronizacion.md) — Diagramas de navegación
- [Reglas de Negocio](../general/06-Reglas-Negocio.md) — Reglas RN-5, RN-6, RN-7, RN-19, RN-20, RN-21, RN-22, RN-23

---

> **Última actualización:** 22/06/2026  
> **Versión:** 1.0  
> **Estado:** Aprobado por el usuario
