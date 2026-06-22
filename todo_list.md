# GymTracker API - Todo List

> Status: **✅ Rodando** — `uvicorn src.main:app --reload --port 8001` funciona com SQLite em dev.
> 22 endpoints ativos em `/api/v1/admin/catalog/`, `/api/v1/admin/health`, `/`.

---

## ✅ Concluído

### 1. Config: Suporte a SQLite (dev) / PostgreSQL (prod)
- `aiosqlite` adicionado nas dependências
- `src/core/config.py` lê `ENVIRONMENT` do `.env`, `database_url` property, `is_sqlite` property
- `src/database/session.py`: engine correto por tipo de banco, `get_db()` única
- `.env` (dev) criado: `ENVIRONMENT=development`, `DATABASE_URL=sqlite+aiosqlite:///./gymtracker.db`

### 2. Modelos: Compatibilidade com SQLite
- `PG_UUID` substituído por `Uuid` genérico do SQLAlchemy
- `server_default="gen_random_uuid()"` substituído por `default=uuid.uuid4`
- Enums PostgreSQL (`DifficultyLevel`, `MediaUrlType`) convertidos para Python `enum.Enum` com `sqlalchemy.Enum`
- Forward reference em `Exercise.instructions` corrigido
- `SoftDeleteMixin` adicionado ao modelo `Equipment`

### 3. Schemas corrigidos
- `BaseExerciseBase` → `ExerciseBase` em todos os schemas do `exercise.py`
- `CatalogVersionResponse` não necessário (router `catalog.py` não importa schema)

### 4. Repositories
- `src/repositories/exercise_repository.py` reescrito com imports corretos, paginação, filtros, search, equipment management

### 5. Services
- Todos os services corrigidos: imports de schemas corretos, métodos `list`/`list_all` padronizados

### 6. Routers
- Todos os routers com imports corretos de `src.schemas.catalog` e `src.schemas.exercise`
- `src/routers/admin.py` removido (exception handlers em router não funcionam)
- `src/routers/catalog.py` simplificado (sem imports quebrados)

### 7. Rotas registradas em `main.py`
- Todos os routers registrados sob `/api/v1/admin/catalog/` + health em `/api/v1/admin/health`
- `src/api/` removido (estrutura consolidada em `src/routers/`)

### 8. Alembic
- `alembic.ini` configurado apontando para `src/database/migrations/env.py`
- Migration inicial criada e aplicada (9 tabelas)

### 9. Dependências
- `aiosqlite`, `bcrypt`, `pydantic-settings` instalados

### 10. Schemas duplicados
- `src/schemas/muscle_group.py` removido (todos usam `src/schemas/catalog.py`)

### 11. `src/api/` vs `src/routers/`
- `src/api/` removido — estrutura consolidada em `src/routers/`

### 14. Infraestrutura
- `.gitignore`: `*.db`, `__pycache__`, `.env` adicionados

---

## 🟡 Próximas tarefas

### 12. Testes
- [ ] Completar `tests/test_exercises.py` (atualmente vazio)
- [ ] Corrigir fixtures assíncronas em `conftest.py`
- [ ] Adicionar `TestClient` fixture para testes de integração
- [ ] Criar database test session com SQLite in-memory

### 13. Autenticação
- [x] Implementar JWT com PyJWT + bcrypt
- [x] Endpoints: `POST /auth/register`, `POST /auth/login`, `GET /auth/me`
- [x] Migration `add_users_table` aplicada
- [ ] ~~Adicionar `python-jose` ou `pyjwt`~~ (PyJWT já estava nas dependências)

---

## 🟢 Melhorias - Nice-to-have

### 14. Infraestrutura (restante)
- [ ] Healthcheck real que testa conexão com banco
- [ ] Script de seed para popular dados de teste
- [ ] Dockerfile: copiar `requirements.txt` e ajustar instalação
- [ ] docker-compose: adicionar volume para código em dev (hot reload)

### 15. Código
- [ ] Logging configurado (atualmente usa `app.logger` sem config)
- [ ] Error handlers globais (app-level) para 404, 422, 500
- [ ] Middleware CORS com origens dinâmicas via config
- [ ] Rate limiting (placeholder removido junto com `admin.py`)

### 16. Documentação
- [ ] README.md com instruções de setup (dev/prod)
- [ ] Endpoints listados no README

---

## Fluxo de Setup (Dev)

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Criar .env
cp .env.example .env
# Editar .env: ENVIRONMENT=development
# DATABASE_URL=sqlite+aiosqlite:///./gymtracker.db

# 3. Rodar migrations
alembic upgrade head

# 4. Iniciar servidor
uvicorn src.main:app --reload --port 8001
```
