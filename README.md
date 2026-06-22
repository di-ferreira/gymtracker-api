# GymTracker API

Exercise catalog API with muscle groups, movement patterns, equipment, and exercises. Role-based access control (admin/user) with JWT authentication. Built with FastAPI, SQLAlchemy, and PostgreSQL/SQLite.

## Stack

- **Framework:** FastAPI
- **ORM:** SQLAlchemy 2.0 (async)
- **Database:** PostgreSQL (prod) / SQLite (dev)
- **Migrations:** Alembic
- **Auth:** JWT (PyJWT) + bcrypt
- **Tests:** pytest + pytest-asyncio + httpx (37 tests)

## Quick Start (Dev)

```bash
# 1. Dependencies
pip install -r requirements.txt

# 2. Environment
cp .env.example .env
# Edit .env: ENVIRONMENT=development
# DATABASE_URL=sqlite+aiosqlite:///./gymtracker.db

# 3. Database
alembic upgrade head

# 4. Start
uvicorn src.main:app --reload --port 8001
```

Open `http://127.0.0.1:8001/docs`.

## Run Tests

```bash
pytest tests/ -v --asyncio-mode=auto
```

## Seed Data

```bash
PYTHONPATH=. python3 scripts/seed.py
```

## Docker (Production)

```bash
docker compose up --build
```

## Docker (Dev with hot reload)

```bash
docker compose -f docker-compose.dev.yml up --build
```

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `ENVIRONMENT` | `development` | `development` or `production` |
| `DATABASE_URL` | `sqlite+aiosqlite:///./gymtracker.db` | DB connection string |
| `SECRET_KEY` | `change-me-...` | JWT signing key |
| `CORS_ORIGINS` | `http://localhost:3000` | Comma-separated allowed origins |
| `LOG_LEVEL` | `INFO` | Logging level |
| `DB_ECHO` | `false` | SQLAlchemy echo mode |
| `DEBUG` | `false` | Debug mode |

## Access Control

| Role | Permissions |
|---|---|
| `user` (default) | Register, login, view own profile, list public catalog |
| `admin` | Full CRUD on catalog, manage users (list, promote, deactivate) |

Default admin seed: `admin@gymtracker.com` / `admin123` (created by `scripts/seed.py`).

## API Endpoints

### Auth (`/api/v1/auth`) — any role

| Method | Path | Description |
|---|---|---|
| POST | `/auth/register` | Create new user |
| POST | `/auth/login` | Get JWT token |
| GET | `/auth/me` | Current user profile |
| PATCH | `/auth/me` | Update own name or password (requires current_password) |

### Admin Users (`/api/v1/admin/users`) — admin only

| Method | Path | Description |
|---|---|---|
| GET | `/users/` | List all users (paginated: `?skip=0&limit=100`) |
| PATCH | `/users/{id}` | Update user role/name/is_active |

### Public Catalog (`/api/v1/catalog`) — any authenticated user

| Method | Path | Description |
|---|---|---|
| GET | `/catalog/exercises/` | List exercises |
| GET | `/catalog/muscle-groups/` | List muscle groups |
| GET | `/catalog/movement-groups/` | List movement groups |
| GET | `/catalog/equipment/` | List equipment |

### Admin Catalog (`/api/v1/admin/catalog`) — admin only

| Method | Path | Description |
|---|---|---|
| POST | `/catalog/muscle-groups/` | Create muscle group |
| GET | `/catalog/muscle-groups/` | List muscle groups |
| GET | `/catalog/muscle-groups/{id}` | Get muscle group |
| PATCH | `/catalog/muscle-groups/{id}` | Update muscle group |
| DELETE | `/catalog/muscle-groups/{id}` | Delete muscle group |
| POST | `/catalog/movement-groups/` | Create movement group |
| GET | `/catalog/movement-groups/` | List movement groups |
| GET | `/catalog/movement-groups/{id}` | Get movement group |
| PATCH | `/catalog/movement-groups/{id}` | Update movement group |
| DELETE | `/catalog/movement-groups/{id}` | Delete movement group |
| POST | `/catalog/equipment/` | Create equipment |
| GET | `/catalog/equipment/` | List equipment |
| GET | `/catalog/equipment/{id}` | Get equipment |
| PATCH | `/catalog/equipment/{id}` | Update equipment |
| DELETE | `/catalog/equipment/{id}` | Delete equipment |
| POST | `/catalog/exercises/` | Create exercise |
| GET | `/catalog/exercises/` | List exercises |
| GET | `/catalog/exercises/{id}` | Get exercise |
| PATCH | `/catalog/exercises/{id}` | Update exercise |
| DELETE | `/catalog/exercises/{id}` | Delete exercise |

### Health

| Method | Path | Description |
|---|---|---|
| GET | `/api/v1/admin/health` | Root health check (with DB test) |
| GET | `/api/v1/admin/catalog/health` | Catalog health check (with DB test) |

### Root

| Method | Path | Description |
|---|---|---|
| GET | `/` | API info |

## Project Structure

```
src/
├── core/           # Config, logging
├── database/       # Session, Base, migrations
├── models/         # SQLAlchemy ORM models
├── schemas/        # Pydantic request/response schemas
├── repositories/   # Data access layer
├── services/       # Business logic
├── routers/        # FastAPI route handlers
└── main.py         # App entrypoint
```
