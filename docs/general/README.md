# TaskRegistry — Documentación del Proyecto

> Aplicación de escritorio personal para el registro diario de tareas laborales, con sincronización semanal a Azure DevOps y tablero de control de tiempo invertido por proyecto.

---

## 📋 Índice de documentación por módulos

| # | Módulo | Descripción |
|---|--------|-------------|
| 1 | [Proyectos](./01-Modulo-Proyectos.md) | Gestión de proyectos: creación, edición, archivado |
| 2 | [Tareas](./02-Modulo-Tareas.md) | Registro diario de tareas con fechas, tiempos y estados |
| 3 | [Documentación del Proyecto](./03-Modulo-Documentacion.md) | Documentos y archivos adjuntos asociados a proyectos |
| 4 | [Sincronización con Azure DevOps](./04-Modulo-Sincronizacion-Azure.md) | Sincronización batch de tareas a Azure DevOps |
| 5 | [Tablero de Control](./05-Modulo-Tablero-Control.md) | Métricas y visualización de tareas y tiempos |
| 6 | [Reglas de Negocio](./06-Reglas-Negocio.md) | Reglas generales que aplican a todo el sistema |

---

## 🎯 Propósito del proyecto

### Problema a resolver

En el día a día laboral existen múltiples fuentes de trabajo (Remedy, HU propias, etc.) que no están centralizadas. Semanalmente se asigna una HU en Azure DevOps donde se debe reflejar todo el trabajo realizado, sin importar su origen. Las HU en Azure son mensuales, lo que hace que se pierda la trazabilidad fina de tareas realizadas en semanas anteriores.

### Solución

**TaskRegistry** es una bitácora personal de escritorio que permite:

1. **Registrar tareas diarias** con proyecto asociado, fechas y tiempo invertido
2. **Sincronizar semanalmente** las tareas seleccionadas a Azure DevOps, colgándolas de la HU correspondiente
3. **Visualizar métricas** de productividad por proyecto y rango de tiempo
4. **Gestionar proyectos** como contenedores de tareas y documentación técnica

---

## 👤 Actor

**Único:** Tú (usuario profesional). No hay autenticación, roles ni multiusuario.

---

## 🧱 Stack asumido

| Componente | Tecnología |
|------------|-----------|
| Tipo de app | Escritorio |
| Persistencia | SQLite (local) |
| Almacenamiento de archivos | Sistema de archivos local (`docs/`) |
| Integración externa | Azure DevOps REST API (vía PAT) |

> *Nota: La definición de tecnologías específicas queda a cargo del desarrollador. Esto es una guía funcional.*

---

## 🚀 Resumen del MVP

| Módulo | ¿Qué hace? | Prioritario |
|--------|-----------|-------------|
| Proyectos | CRUD simple: nombre + descripción | ✅ MVP |
| Documentación | Adjuntar documentos con archivos a proyectos | ✅ MVP |
| Tareas | Registro diario con fechas, tiempo y estados | ✅ MVP |
| Sincronización Azure | Envio batch de tareas seleccionadas a Azure DevOps | ✅ MVP |
| Tablero de control | Métricas por proyecto en rango de tiempo configurable | ✅ MVP |

---

## 🔮 Features futuras (fuera de MVP)

- Automatizaciones de tareas (scripts bash, tests, etc.)
- Sincronización bidireccional (Azure → App)
- Edición masiva de tareas
- Backup / exportación de datos
- Notificaciones / recordatorios
- Temas / personalización de UI
