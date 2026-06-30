# Backend FastAPI con JWT

Aplicación Web API construida con **Python + FastAPI** que implementa autenticación con JWT.

## Requisitos

- Python 3.12+
- [Poetry](https://python-poetry.org/)
- Docker y Docker Compose (opcional)

## Configuración del proyecto

La gestión de dependencias se realiza con Poetry y en `pyproject.toml` se define:

- `package-mode = false` (es una aplicación, no un paquete distribuible)
- `passlib[bcrypt]`
- `bcrypt >=3.2,<4.0` para compatibilidad con passlib 1.7.x

Variables opcionales de entorno:

- `SECRET_KEY`: clave para firmar JWT.
- `ADMIN_PASSWORD_HASH`: hash bcrypt de la contraseña del usuario `admin`.

## Instalación y ejecución local

Desde la carpeta `backend`:

```bash
poetry install
poetry run uvicorn app.main:app --reload
```

La API quedará disponible en `http://localhost:8000`.

## Endpoints

### 1) Obtener token

- **POST** `/token`
- Body JSON:

```json
{
  "username": "admin",
  "password": "admin123"
}
```

Respuesta exitosa:

```json
{
  "access_token": "<jwt>",
  "token_type": "bearer",
  "expires_in": 300
}
```

### 2) Refrescar token

- **POST** `/token/refresh`
- Requiere header:

Enviar el header `Authorization` usando esquema bearer con el `access_token` obtenido en `/token`.

Respuesta exitosa:

```json
{
  "access_token": "<nuevo_jwt>",
  "token_type": "bearer",
  "expires_in": 300
}
```

## Ejecución con Docker

Desde la carpeta `backend`:

```bash
docker compose up --build
```

Esto expone la API en `http://localhost:8000`.
