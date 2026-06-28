---
description: >
  Estandariza los commits usando Conventional Commits y GitFlow.
  Incluye validación automática de mensajes y naming de ramas.
mode: all
temperature: 0.1
color: "#f59e0b"
---

# Commit Standards & GitFlow

Este skill define el estándar de commits y el flujo de trabajo con GitFlow para el proyecto. Cárgalo siempre que trabajes con git.

---

## 1. Conventional Commits

Toda descripción de commit DEBE seguir el formato:

```
tipo(alcance): descripción

cuerpo (opcional)

footer (opcional)
```

### Tipos permitidos

| Tipo       | Uso |
|------------|-----|
| `feat`     | Nueva funcionalidad |
| `fix`      | Corrección de bug |
| `chore`    | Mantenimiento, config, dependencias |
| `docs`     | Documentación (README, docstrings, docs/) |
| `style`    | Cambios de formato que no afectan lógica (ruff, espacios, etc.) |
| `refactor` | Cambio de código que no es fix ni feat |
| `perf`     | Mejora de rendimiento |
| `test`     | Agregar o corregir tests |
| `build`    | Cambios en el sistema de build o dependencias |
| `ci`       | Cambios en CI/CD (GitHub Actions, etc.) |
| `revert`   | Revertir un commit anterior |

### Alcance (scope)

Usar el módulo o área afectada. Ejemplos comunes del proyecto:

- `proyectos`
- `tareas`
- `tablero`
- `docs`
- `sincronizacion`
- `auth`
- `api`
- `db`
- `ui`
- `config`
- `deps`
- `ci`

Omitir el alcance si el cambio es transversal.

### Ejemplos

```
feat(proyectos): add CRUD endpoints for project management
```
```
fix(tareas): resolve date overflow on weekly view
```
```
refactor(api): extract validation logic to middleware
```
```
docs: update README with setup instructions
```
```
ci: add commit message validation workflow
```

### Reglas

1. La descripción va en **inglés**, en **imperativo** (add, fix, remove, refactor, etc.)
2. La descripción NO lleva punto final
3. El cuerpo explica **qué** y **por qué**, no el **cómo**
4. El footer puede contener `BREAKING CHANGE:` o referencias a issues `Closes #123`

---

## 2. GitFlow

### Ramas principales

| Rama       | Propósito |
|------------|-----------|
| `main`     | Código en producción. Solo recibe merges desde `release` o `hotfix` |
| `develop`  | Rama de integración. Recibe merges desde `feature/*` y `bugfix/*` |

### Ramas de soporte

| Rama                        | Origen      | Destino     | Propósito |
|-----------------------------|-------------|-------------|-----------|
| `feature/<id>-<desc>`       | `develop`   | `develop`   | Nueva funcionalidad |
| `bugfix/<id>-<desc>`        | `develop`   | `develop`   | Corrección en desarrollo |
| `hotfix/<id>-<desc>`        | `main`      | `main` + `develop` | Corrección urgente en producción |
| `release/<version>`         | `develop`   | `main` + `develop` | Preparación de release |

### Reglas de branch naming

- Usar **kebab-case** después del prefijo
- Incluir ID del issue si aplica: `feature/42-add-login`, `bugfix/87-fix-crash`
- Versiones semánticas en releases: `release/1.2.3`

### Flujo de trabajo

```
                        main
                         ↑
                 release/1.0.0 ←─── tag v1.0.0
                  ↑        ↑
         feature/* → develop  ← hotfix/*
                  ↑
              bugfix/*
```

#### Feature o Bugfix
```
git checkout develop
git pull
git checkout -b feature/42-add-login
# ... trabajar, commiteando con Conventional Commits
git push -u origin feature/42-add-login
# Crear PR a develop → squash & merge
```

#### Hotfix
```
git checkout main
git pull
git checkout -b hotfix/87-fix-critical
# ... trabajar, commiteando
git push -u origin hotfix/87-fix-critical
# Crear PR a main → merge (no squash)
# Crear PR a develop → merge
```

#### Release
```
git checkout develop
git pull
git checkout -b release/1.0.0
# Últimos ajustes (changelog, version bump, etc.)
git push -u origin release/1.0.0
# Crear PR a main → merge (no squash)
# Taggear: git tag -a v1.0.0 -m "v1.0.0"
# Merge back a develop
```

### Estrategia de merge

| Rama origen → destino | Estrategia |
|---|---|
| `feature/*` → `develop` | **Squash & merge** (1 commit por feature) |
| `bugfix/*` → `develop` | **Squash & merge** |
| `hotfix/*` → `main` | **Merge commit** (preservar historia) |
| `hotfix/*` → `develop` | **Merge commit** |
| `release/*` → `main` | **Merge commit** |
| `release/*` → `develop` | **Merge commit** |

### Versionado semántico

`MAJOR.MINOR.PATCH` basado en:

- **MAJOR**: breaking changes (`BREAKING CHANGE` en footer del commit)
- **MINOR**: nuevas funcionalidades (`feat`)
- **PATCH**: bugfixes y cambios menores (`fix`, `refactor`, `chore`, etc.)

---

## 3. Hooks de validación

El proyecto incluye hooks automáticos vía `pre-commit`:

### commit-msg

Se ejecuta al hacer `git commit`. Valida que el mensaje cumpla:

```
^(feat|fix|chore|docs|style|refactor|perf|test|build|ci|revert)(\(.+\))?: .{1,72}
```

- Rechaza el commit si el formato es inválido
- Muestra el error y un ejemplo de formato correcto

### Instalación local

```bash
pip install pre-commit
pre-commit install --hook-type commit-msg
```

---

## 4. Para agentes opencode

Cuando cargues este skill, SIGUE ESTRICTAMENTE estas reglas:

1. Antes de hacer `git commit`, asegúrate de que el mensaje sigue Conventional Commits
2. Al crear ramas, usa el prefijo adecuado según el propósito (feature, bugfix, hotfix)
3. Al cerrar un PR, indica la estrategia de merge correcta
4. Si el usuario no especifica un mensaje de commit, propón uno tú siguiendo el estándar
