# Módulo 3: Documentación del Proyecto

> Cada proyecto puede contener múltiples documentos con archivos adjuntos. Ideal para almacenar consultas SQL, información de ambientes, guías técnicas, etc.

---

## Estructura de datos

| Campo | Tipo | Reglas |
|-------|------|--------|
| `id` | Entero (autoincremental) | Identificador único |
| `proyecto_id` | Relación → Proyecto | Obligatorio |
| `titulo` | Texto (obligatorio) | Máximo 200 caracteres |
| `descripcion` | Texto largo (opcional) | |
| `fecha_creacion` | Fecha (automática) | Se asigna al crear |
| `fecha_actualizacion` | Fecha (automática) | Se actualiza al modificar |

### Archivos adjuntos

Cada documento puede tener **uno o varios archivos adjuntos**.

| Campo | Tipo | Reglas |
|-------|------|--------|
| `id` | Entero (autoincremental) | Identificador único |
| `documento_id` | Relación → Documento | Obligatorio |
| `nombre_archivo` | Texto | Nombre original del archivo |
| `ruta_local` | Texto | Ruta en el sistema de archivos local |
| `tamano_bytes` | Entero | Tamaño del archivo |
| `tipo_mime` | Texto | Tipo MIME del archivo |

---

## Reglas de almacenamiento

- Los archivos se guardan en el **sistema de archivos local**, en una carpeta `docs/` dentro del directorio de datos de la aplicación
- Estructura de carpetas sugerida:
  ```
  datos/
  └── docs/
      └── {proyecto_id}/
          └── {documento_id}/
              ├── archivo1.pdf
              └── archivo2.png
  ```
- **Límite por archivo:** 50 MB (configurable, pero sugerido para MVP)
- **Sin restricción de tipo MIME** en MVP, pero mostrar advertencia al adjuntar archivos ejecutables (`.exe`, `.bat`, `.sh`, etc.)

---

## Funcionalidades

### Agregar documento a un proyecto
- Formulario: título (obligatorio) + descripción (opcional)
- Selector de archivos para adjuntar uno o múltiples archivos
- Los archivos se copian a la carpeta local de documentos

### Editar documento
- Modificar título y descripción
- Agregar o eliminar archivos adjuntos

### Eliminar documento
- Confirmación antes de eliminar
- Se eliminan también todos los archivos adjuntos del disco

### Visualizar documentos
- Lista de documentos dentro de la vista de detalle del proyecto
- Cada documento muestra: título, descripción (resumida), cantidad de archivos, fecha de creación
- Al hacer clic en un archivo adjunto, se abre con el **programa asociado del sistema operativo**

---

## Vista funcional

### Vista: Documentos de un proyecto
```
+--------------------------------------------------+
| Proyecto: Backend                   [+ Nuevo doc] |
+--------------------------------------------------+
| ● Consultas SQL de producción                     |
|   Consultas útiles para troubleshooting en prod   |
|   📎 3 archivos                    12/06/2026     |
|                                                   |
| ● Información de ambientes                        |
|   URLs, credenciales y config de cada ambiente    |
|   📎 1 archivo                     10/06/2026     |
|                                                   |
| ● Guía de deploy                                  |
|   Pasos para hacer deploy en cada ambiente        |
|   📎 2 archivos                     05/06/2026     |
+--------------------------------------------------+
```

### Vista: Detalle de documento
```
+--------------------------------------------------+
| Título:  [Consultas SQL de producción          ]  |
| Descripción:                                      |
| [Consultas útiles para troubleshooting en prod  ] |
|                                                   |
| Archivos adjuntos:                                |
| ☐ consultas_prod.sql         12.4 KB  [Abrir] [X] |
| ☐ indices_lentos.sql          3.1 KB  [Abrir] [X] |
| ☐ stored_procs.sql            8.7 KB  [Abrir] [X] |
|                                                   |
| [+ Agregar archivos]                              |
+--------------------------------------------------+
| [Guardar]  [Eliminar documento]                   |
+--------------------------------------------------+
```
