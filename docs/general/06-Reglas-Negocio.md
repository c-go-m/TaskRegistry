# Reglas de Negocio

> Reglas generales que aplican a todos los módulos del sistema.

---

## Reglas generales

| # | Regla | Aplica a |
|---|-------|----------|
| 1 | **Una tarea pertenece a un solo proyecto.** No se puede asignar una tarea a múltiples proyectos. | Tareas |
| 2 | **No se puede eliminar un proyecto que tenga tareas asociadas.** Solo se puede archivar. Para eliminar, deben moverse o eliminarse las tareas primero. | Proyectos |
| 3 | **La fecha de fin no puede ser anterior a la fecha de inicio.** El sistema debe validarlo al guardar. | Tareas |
| 4 | **El tiempo invertido se calcula automáticamente** como `(fecha_fin - fecha_inicio)` en horas decimales, pero el usuario puede sobrescribirlo manualmente. Si se modifican las fechas, se recalcula. | Tareas |
| 5 | **La sincronización es de solo creación (App → Azure).** No hay actualización de tareas existentes en Azure DevOps ni sincronización inversa. | Sincronización |
| 6 | **Cada tarea se sincroniza una sola vez.** Al pasar a estado `Sincronizada`, queda bloqueada en solo lectura. | Tareas / Sincronización |
| 7 | **Solo las tareas en estado `Ejecutada` pueden sincronizarse.** La app debe advertir si se intenta sincronizar tareas en otro estado. | Sincronización |
| 8 | **Los archivos adjuntos se almacenan localmente** en el sistema de archivos, dentro del directorio de datos de la aplicación. | Documentación |
| 9 | **Límite de 50 MB por archivo adjunto** en MVP. Sin restricción de tipo MIME, pero con advertencia para archivos ejecutables. | Documentación |
| 10 | **Los proyectos archivados se ocultan de las vistas por defecto**, pero sus tareas y documentos se conservan. Se pueden consultar activando un filtro "Mostrar archivados". | Proyectos |

---

## Reglas de estados de tarea

| # | Regla |
|---|-------|
| 11 | El usuario puede cambiar libremente entre `Nueva` ↔ `En proceso` ↔ `Ejecutada`. |
| 12 | No se puede volver de `Ejecutada` a `Nueva` o `En proceso` **a menos que** la tarea no haya sido sincronizada. |
| 13 | Una vez sincronizada (`Sincronizada`), no se puede modificar ningún campo ni cambiar de estado. |
| 14 | Si la sincronización falla para una tarea, la tarea permanece en estado `Ejecutada` y puede reintentarse. |

---

## Reglas de integridad referencial

| # | Regla |
|---|-------|
| 15 | Al archivar un proyecto, todas sus tareas y documentos se conservan. |
| 16 | Al eliminar un proyecto (solo permitido si no tiene tareas), se eliminan también sus documentos y archivos del disco. |
| 17 | Al eliminar un documento, todos sus archivos adjuntos se eliminan del disco. |
| 18 | Las tareas sincronizadas mantienen los IDs de Azure DevOps incluso si el proyecto se archiva posteriormente. |

---

## Reglas de sincronización con Azure DevOps

| # | Regla |
|---|-------|
| 19 | La conexión se configura una sola vez (URL, proyecto, PAT) y se persiste localmente. |
| 20 | El PAT debe almacenarse de forma segura (cifrado en base de datos o keychain del SO). |
| 21 | El ID de la HU destino debe ingresarse manualmente cada vez que se sincroniza. |
| 22 | La app debe mantener un historial de los últimos IDs de HU usados para autocompletar. |
| 23 | Si la sincronización falla a mitad de camino, se registra éxito/fallo por cada tarea individual. |

---

## Reglas de UI/UX

| # | Regla |
|---|-------|
| 24 | Las tareas sincronizadas deben tener un indicador visual claro (ej. icono de check azul, badge). |
| 25 | El tiempo invertido editado manualmente debe diferenciarse visualmente del calculado. |
| 26 | Las advertencias deben ser claras y accionables (ej. "Esta tarea cambiará a solo lectura al sincronizarse"). |
| 27 | El tablero debe mostrar siempre las tarjetas de resumen, incluso si los valores son 0. |
