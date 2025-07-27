    `auth-service/
    ├── src/
    │   ├── auth_service/
    │   │   ├── __init__.py
    │   │   ├── main.py                 # FastAPI app entry point
    │   │   ├── config/
    │   │   │   ├── __init__.py
    │   │   │   ├── settings.py         # Environment configuration
    │   │   │   └── database.py         # Database configuration
    │   │   ├── domain/                 # Domain layer (entities, value objects)
    │   │   │   ├── __init__.py
    │   │   │   ├── entities/
    │   │   │   │   ├── __init__.py
    │   │   │   │   ├── user.py
    │   │   │   │   ├── role.py
    │   │   │   │   └── permission.py
    │   │   │   └── repositories/       # Repository interfaces
    │   │   │       ├── __init__.py
    │   │   │       ├── user_repository.py
    │   │   │       └── role_repository.py
    │   │   ├── infrastructure/         # Infrastructure layer
    │   │   │   ├── __init__.py
    │   │   │   ├── database/
    │   │   │   │   ├── __init__.py
    │   │   │   │   ├── models.py       # SQLAlchemy models
    │   │   │   │   ├── repositories/   # Repository implementations
    │   │   │   │   │   ├── __init__.py
    │   │   │   │   │   ├── user_repository.py
    │   │   │   │   │   └── role_repository.py
    │   │   │   │   └── migrations/     # Alembic migrations
    │   │   │   ├── security/
    │   │   │   │   ├── __init__.py
    │   │   │   │   ├── password.py     # Password hashing
    │   │   │   │   ├── jwt_handler.py  # JWT operations
    │   │   │   │   └── permissions.py  # Permission checks
    │   │   │   └── external/           # External service integrations
    │   │   │       ├── __init__.py
    │   │   │       └── email_service.py
    │   │   ├── application/            # Application layer (use cases)
    │   │   │   ├── __init__.py
    │   │   │   ├── services/
    │   │   │   │   ├── __init__.py
    │   │   │   │   ├── auth_service.py
    │   │   │   │   └── user_service.py
    │   │   │   └── dtos/              # Data Transfer Objects
    │   │   │       ├── __init__.py
    │   │   │       ├── auth_dto.py
    │   │   │       └── user_dto.py
    │   │   └── presentation/           # Presentation layer (API)
    │   │       ├── __init__.py
    │   │       ├── api/
    │   │       │   ├── __init__.py
    │   │       │   ├── v1/
    │   │       │   │   ├── __init__.py
    │   │       │   │   ├── auth.py     # Auth endpoints
    │   │       │   │   ├── users.py    # User endpoints
    │   │       │   │   └── admin.py    # Admin endpoints
    │   │       │   └── dependencies.py # Dependency injection
    │   │       ├── middleware/
    │   │       │   ├── __init__.py
    │   │       │   ├── auth_middleware.py
    │   │       │   └── rate_limit.py
    │   │       └── schemas/            # Pydantic models
    │   │           ├── __init__.py
    │   │           ├── auth.py
    │   │           ├── user.py
    │   │           └── common.py
    ├── tests/
    │   ├── __init__.py
    │   ├── unit/
    │   ├── integration/
    │   └── conftest.py
    ├── migrations/                     # Alembic migration files
    ├── docs/                          # Documentation
    ├── scripts/                       # Utility scripts
    ├── requirements/
    │   ├── base.txt
    │   ├── dev.txt
    │   └── prod.txt
    ├── .env.example
    ├── alembic.ini
    ├── pyproject.toml
    ├── Dockerfile
    ├── docker-compose.yml
    └── README.md`