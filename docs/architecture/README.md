# TaskRegistry — Arquitectura Técnica

> Documentación de decisiones arquitectónicas del proyecto TaskRegistry.

---

## 📋 Índice de documentos

| # | Documento | Descripción |
|---|-----------|-------------|
| — | [Contexto del sistema](./diagrama-contexto.md) | Diagrama C4 nivel 1: actores y sistemas externos |
| — | [Contenedores del sistema](./diagrama-contenedores.md) | Diagrama C4 nivel 2: componentes internos |
| — | [Estructura del proyecto](./estructura-propuesta.md) | Árbol de directorios completo |
| 1 | [ADR-001: Stack tecnológico](./ADR-001-stack-tecnologico.md) | FastAPI, Jinja2+HTMX+Alpine.js, SQLite, SQLModel, Ruff |
| 2 | [ADR-002: Estructura del proyecto](./ADR-002-estructura-proyecto.md) | Organización modular por dominio |
| 3 | [ADR-003: Patrones de diseño](./ADR-003-patrones-diseno.md) | Router → Service → Repository → Model + DI |
| 4 | [ADR-004: DevOps / CI-CD](./ADR-004-devops.md) | GitHub, GitHub Actions, SonarCloud, Ruff, Conventional Commits |

---

## 📐 Resumen del stack

```
┌──────────────────────────────────────────────────┐
│                   NAVEGADOR                        │
│  HTML + HTMX + Alpine.js + Tailwind CSS (CDN)     │
└──────────────────────┬───────────────────────────┘
                       │ HTTP (localhost:8080)
┌──────────────────────▼───────────────────────────┐
│                FASTAPI (Python 3.12)               │
│  ┌──────────┐  ┌──────────┐  ┌────────────────┐   │
│  │  Router   │─>│  Service  │─>│  Repository    │   │
│  │ (endpoint)│  │ (reglas)  │  │  (consultas BD)│   │
│  └──────────┘  └──────────┘  └───────┬──────────┘   │
│                                       │               │
│  ┌────────────────────────────────────▼────────────┐ │
│  │              SQLModel + SQLite                   │ │
│  │  data/taskregistry.db                           │ │
│  └─────────────────────────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────┐ │
│  │  Sistema de Archivos Local                       │ │
│  │  data/docs/{proyecto}/{documento}/               │ │
│  └─────────────────────────────────────────────────┘ │
└──────────────────────┬───────────────────────────┘
                       │ HTTPS + PAT
┌──────────────────────▼───────────────────────────┐
│           Azure DevOps REST API                    │
│  POST /_apis/wit/workitems/$Task                  │
└──────────────────────────────────────────────────┘
```

---

## 📦 Cómo empezar

```bash
# 1. Clonar el repositorio
git clone https://github.com/tuusuario/taskregistry.git
cd taskregistry

# 2. Crear y activar entorno virtual
python -m venv .venv
.venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
copy .env.example .env
# Editar .env con PAT de Azure DevOps (opcional para inicio)

# 5. Ejecutar en desarrollo
python run.py
# Abrir http://localhost:8080
```
