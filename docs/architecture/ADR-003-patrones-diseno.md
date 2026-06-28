# ADR-003: Patrones de Diseño

- **Estado:** Aceptado
- **Fecha:** 2026-06-20
- **Contexto:** Definir la arquitectura interna de cada módulo y las relaciones entre capas

---

## Decisión

Se adopta el patrón **Router → Service → Repository → Model** con **Inyección de Dependencias** mediante FastAPI `Depends`.

---

## Estructura de Capas

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   ROUTER     │────>│   SERVICE    │────>│  REPOSITORY   │────>│    MODEL     │
│  (endpoints)  │     │ (reglas de   │     │  (consultas)  │     │  (SQLModel)  │
│              │     │  negocio)    │     │               │     │              │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
       │                     │
       │                     ▼
       │           ┌──────────────────┐
       │           │  Servicios       │
       └──────────>│  externos        │
                   │  (Azure API,     │
                   │   logger, etc.)  │
                   └──────────────────┘
```

### Responsabilidades

| Capa | Responsabilidad | ¿Contiene lógica de negocio? |
|------|----------------|------------------------------|
| **Router** | Define endpoints HTTP, valida parámetros de ruta/query, llama al servicio | No |
| **Service** | Reglas de negocio, orquestación, transiciones de estado, cálculos | Sí |
| **Repository** | Acceso a datos (CRUD), queries a la BD, abstrae SQLModel | No |
| **Model** | Definición de tablas SQLModel, relaciones entre entidades | Solo esquema |

### Inyección de Dependencias

Las dependencias se inyectan desde `core/dependencies.py`:

```python
def get_db(request: Request) -> Session: ...
def get_repository(request: Request) -> ProyectoRepository: ...
def get_logger() -> Logger: ...
```

Esto permite:
- **Testear servicios con repositorios mock** sin BD real
- **Cambiar implementación** de repositorios sin modificar servicios
- **Aislar lógica de negocio** para pruebas unitarias

### Repository (Patrón)

Cada módulo define una **interfaz abstracta** y una **implementación concreta**:

```python
class ProyectoRepository(ABC):
    @abstractmethod
    def get_activos(self) -> list[Proyecto]: ...
    @abstractmethod
    def get_by_id(self, id: int) -> Proyecto | None: ...
    @abstractmethod
    def save(self, proyecto: Proyecto) -> Proyecto: ...

class SQLAlchemyProyectoRepository(ProyectoRepository):
    def __init__(self, db: Session): ...
    # implementaciones
```

---

## Opciones Consideradas

- **Router → Service (sin Repository)** — Válido para CRUD simple, pero dificulta el testing unitario del Service
- **Router → Service → Repository → Model** ✅ — Mejor separación, testable, desacoplado
- **Clean Architecture / Hexagonal** — Demasiado para un proyecto de este tamaño; el patrón elegido es suficiente

---

## Consecuencias

- Los tests unitarios pueden usar repositorios mock en lugar de BD real
- La lógica de negocio está centralizada en Services, no dispersa en los routers
- Cada módulo puede cambiar su implementación de BD sin afectar a otros módulos
- El código es más verboso inicialmente (interfaces, inyección) pero más mantenible a largo plazo
