# ADR-004: DevOps / CI-CD

- **Estado:** Aceptado
- **Fecha:** 2026-06-20
- **Contexto:** Definir herramientas y flujo de trabajo para desarrollo, integración continua y distribución

---

## Decisiones

| Aspecto | Elección |
|---------|----------|
| Gestor de dependencias | `pip` + `requirements.txt` |
| Ejecución | `python run.py` + script `.bat` |
| Linter / Formatter | Ruff |
| Repositorio | GitHub |
| Análisis de calidad | SonarCloud (cloud, sin agente local) |
| CI/CD | GitHub Actions desde el día 1 |
| Versionado | Semántico (`MAJOR.MINOR.PATCH`) |
| Commits | Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, etc.) |

---

## Pipeline CI/CD Propuesto

### Workflow: CI (por push y PR a main)

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test-and-lint:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: "pip"

      - name: Instalar dependencias
        run: pip install -r requirements.txt

      - name: Instalar herramientas de desarrollo
        run: pip install ruff pytest pytest-cov

      - name: Linter (Ruff)
        run: ruff check .

      - name: Tests con cobertura
        run: pytest --cov=. --cov-report=xml

      - name: Análisis SonarCloud
        uses: SonarSource/sonarcloud-github-action@master
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

### Workflow: Release (por tag v*)

```yaml
name: Release

on:
  push:
    tags:
      - "v*"

jobs:
  release:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - run: pip install -r requirements.txt

      - name: Generar changelog
        id: changelog
        uses: mikepenz/release-changelog-builder-action@v4

      - name: Crear Release
        uses: softprops/action-gh-release@v1
        with:
          body: ${{ steps.changelog.outputs.changelog }}
```

---

## Flujo de Trabajo Diario

```bash
git checkout -b feat/agregar-filtro-fechas
# ... desarrollar ...
ruff check .        # Linter
ruff format .       # Formatter
pytest              # Tests
git add -A
git commit -m "feat: agregar filtro por rango de fechas en tablero"
git push origin feat/agregar-filtro-fechas
# PR en GitHub → CI automático → merge a main
```

---

## Consecuencias

- Cada push ejecuta linter + tests + SonarCloud automáticamente
- SonarCloud no requiere infraestructura local (SaaS)
- Ruff mantiene el estilo consistente sin intervención manual
- Conventional commits permiten generar changelogs automáticos
- El `requirements.txt` mantenido manualmente requiere atención para no quedar desactualizado
