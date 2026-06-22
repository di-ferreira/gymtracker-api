# GymTracker API

Exercise catalog API with muscle groups, movement patterns, equipment, and exercises. Role-based access control (admin/user) with JWT authentication. Built with FastAPI, SQLAlchemy, and PostgreSQL/SQLite.

## Stack

- **Framework:** FastAPI
- **ORM:** SQLAlchemy 2.0 (async, `Mapped` + `mapped_column`)
- **Database:** PostgreSQL (prod) / SQLite (dev)
- **Migrations:** Alembic
- **Auth:** JWT (PyJWT) + bcrypt
- **Storage:** Local (dev, `aiofiles`) / S3-compatible (prod, `boto3`)
- **Tests:** pytest + pytest-asyncio + httpx (57 tests)

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

Creates admin user `admin@gymtracker.com` / `admin123` + 40 exercises.

## Docker (Production)

```bash
docker compose up --build
```

Includes PostgreSQL + MinIO (S3-compatible storage) + API.

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
| `STORAGE_BACKEND` | `local` | `local` or `s3` |
| `MEDIA_DIR` | `media` | Directory for local file storage |
| `MEDIA_BASE_URL` | `http://localhost:8001/media` | Public base URL for media files |
| `MAX_UPLOAD_SIZE_MB` | `10` | Max upload file size |
| `S3_BUCKET` | `gymtracker-media` | S3/MinIO bucket name |
| `S3_ENDPOINT` | — | S3 endpoint URL (e.g. `http://minio:9000`) |
| `S3_ACCESS_KEY` | — | S3 access key |
| `S3_SECRET_KEY` | — | S3 secret key |

## Access Control

| Role | Permissions |
|---|---|
| `user` (default) | Register, login, view own profile, list public catalog |
| `admin` | Full CRUD on catalog, manage users (list, promote, deactivate), upload media |

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

### Media (`/api/v1/admin/media`) — admin only

| Method | Path | Description |
|---|---|---|
| POST | `/media/upload?folder=exercises` | Upload file (jpg, png, gif, mp4, webm; max 10MB) |
| DELETE | `/media/{folder}/{filename}` | Delete uploaded file |

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
| `Muscle Groups` | | |
| POST | `/catalog/muscle-groups/` | Create |
| GET | `/catalog/muscle-groups/` | List |
| GET | `/catalog/muscle-groups/{id}` | Get by ID |
| PATCH | `/catalog/muscle-groups/{id}` | Update |
| DELETE | `/catalog/muscle-groups/{id}` | Delete |
| `Movement Groups` | | |
| POST | `/catalog/movement-groups/` | Create |
| GET | `/catalog/movement-groups/` | List |
| GET | `/catalog/movement-groups/{id}` | Get by ID |
| PATCH | `/catalog/movement-groups/{id}` | Update |
| DELETE | `/catalog/movement-groups/{id}` | Delete |
| `Equipment` | | |
| POST | `/catalog/equipment/` | Create |
| GET | `/catalog/equipment/` | List |
| GET | `/catalog/equipment/{id}` | Get by ID |
| PATCH | `/catalog/equipment/{id}` | Update |
| DELETE | `/catalog/equipment/{id}` | Delete |
| `Exercises` | | |
| POST | `/catalog/exercises/` | Create |
| GET | `/catalog/exercises/` | List (supports pagination, search, filters) |
| GET | `/catalog/exercises/{id}` | Get by ID |
| PATCH | `/catalog/exercises/{id}` | Update |
| DELETE | `/catalog/exercises/{id}` | Soft delete |
| `Exercise Instructions` | | |
| GET | `/catalog/exercises/{id}/instructions/` | List instructions |
| POST | `/catalog/exercises/{id}/instructions/` | Add instruction |
| PATCH | `/catalog/exercises/{id}/instructions/{instr_id}` | Update instruction |
| DELETE | `/catalog/exercises/{id}/instructions/{instr_id}` | Remove instruction |
| `Exercise Alternatives` | | |
| GET | `/catalog/exercises/{id}/alternatives/` | List alternatives |
| POST | `/catalog/exercises/{id}/alternatives/` | Add alternative |
| DELETE | `/catalog/exercises/{id}/alternatives/{alt_id}` | Remove alternative |

### Health

| Method | Path | Description |
|---|---|---|
| GET | `/api/v1/admin/health` | Root health check (with DB test) |
| GET | `/api/v1/admin/catalog/health` | Catalog health check (with DB test) |

### Root

| Method | Path | Description |
|---|---|---|
| GET | `/` | API info |

## Error Format

All errors return a consistent structure:

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Exercise not found"
  }
}
```

Possible codes: `NOT_FOUND`, `CONFLICT`, `UNAUTHORIZED`, `FORBIDDEN`, `BAD_REQUEST`, `VALIDATION_ERROR`, `FILE_TOO_LARGE`, `INTERNAL_ERROR`.

## Project Structure

```
src/
├── core/           # Config, logging, error helpers, auth dependencies
├── database/       # Session, Base, Alembic migrations
├── models/         # SQLAlchemy ORM models (Mapped + mapped_column)
├── schemas/        # Pydantic request/response schemas
├── repositories/   # Data access layer
├── services/       # Business logic
├── routers/        # FastAPI route handlers
├── storage/        # Storage abstraction (local + S3 backends)
└── main.py         # App entrypoint
```

## TypeScript Types

See `types.md` for TypeScript interfaces matching all API responses.
