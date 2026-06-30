# Backend – JWT Authentication API

A lightweight **FastAPI** web service that demonstrates JWT-based authentication.  
Dependencies are managed with [Poetry](https://python-poetry.org/).

---

## Features

| Endpoint | Method | Description |
|---|---|---|
| `/token` | `POST` | Authenticate and receive a JWT (expires in 300 s) |
| `/token/refresh` | `POST` | Exchange a valid token for a new one |
| `/health` | `GET` | Liveness probe |
| `/docs` | `GET` | Interactive Swagger UI |
| `/redoc` | `GET` | ReDoc documentation |

---

## Requirements

- Python ≥ 3.11
- [Poetry](https://python-poetry.org/) ≥ 1.8
- Docker & Docker Compose (optional, for containerised deployment)

---

## Local setup (without Docker)

```bash
# 1. Enter the backend directory
cd backend

# 2. Install dependencies
poetry install

# 3. Run the development server
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at <http://localhost:8000>.  
Interactive docs: <http://localhost:8000/docs>

---

## Docker deployment

```bash
# From the backend/ directory
docker compose up --build
```

Or set a custom secret key:

```bash
SECRET_KEY=my-super-secret-key docker compose up --build
```

The service will be available at <http://localhost:8000>.

---

## Usage

### 1. Obtain a token

```bash
curl -X POST http://localhost:8000/token \
  -d "username=admin&password=admin123" \
  -H "Content-Type: application/x-www-form-urlencoded"
```

**Response**

```json
{
  "access_token": "<jwt>",
  "token_type": "bearer",
  "expires_in": 300
}
```

### 2. Refresh a token

```bash
curl -X POST http://localhost:8000/token/refresh \
  -H "Authorization: Bearer <your_access_token>"
```

**Response**

```json
{
  "access_token": "<new_jwt>",
  "token_type": "bearer",
  "expires_in": 300
}
```

### 3. Health check

```bash
curl http://localhost:8000/health
# {"status":"ok"}
```

---

## Configuration

| Environment variable | Default | Description |
|---|---|---|
| `SECRET_KEY` | `change-me-in-production-use-a-long-random-string` | HMAC signing key for JWTs. **Always override in production.** |

---

## Project structure

```
backend/
├── app/
│   ├── __init__.py
│   └── main.py          # FastAPI application & JWT logic
├── pyproject.toml       # Poetry project manifest
├── poetry.lock          # Locked dependency tree
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## Security notes

- Passwords are hashed with **bcrypt** via `passlib[bcrypt]`.  
- The `bcrypt` package is pinned to `>=3.2,<4.0` for compatibility with passlib 1.7.x.  
- JWT tokens are signed with **HS256**.  
- The default `SECRET_KEY` is only suitable for local development.  Always set a strong secret in production via the `SECRET_KEY` environment variable.
