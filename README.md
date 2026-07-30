# Task Management API

A production-ready FastAPI backend for a task management application with JWT authentication, task CRUD operations, input validation, and CORS support.

## Features

- User registration and login
- JWT bearer authentication
- Password hashing with bcrypt
- Task CRUD endpoints scoped to the authenticated user
- Pydantic request and response validation
- SQLAlchemy ORM persistence
- SQLite by default, configurable via environment variables
- CORS middleware for frontend integration
- Interactive API docs at `/docs`

## Tech Stack

- FastAPI
- SQLAlchemy
- Pydantic
- python-jose
- Passlib with bcrypt
- Uvicorn

## Project Structure

```text
app/
├── api/
│   ├── deps.py
│   └── routes/
│       ├── auth.py
│       ├── health.py
│       └── tasks.py
├── core/
│   ├── config.py
│   ├── database.py
│   └── security.py
├── crud/
│   ├── task.py
│   └── user.py
├── models/
│   ├── task.py
│   └── user.py
├── schemas/
│   ├── task.py
│   ├── token.py
│   └── user.py
└── main.py
```

## Requirements

- Python 3.11+

## Setup

1. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create your environment file:

```bash
cp .env.example .env
```

4. Set a strong secret key in `.env`.

Example generator:

```bash
python -c 'import secrets; print(secrets.token_urlsafe(32))'
```

5. Start the API:

```bash
uvicorn app.main:app --reload
```

6. Open the docs:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `APP_NAME` | Application name | `Task Management API` |
| `ENVIRONMENT` | Runtime environment | `development` |
| `API_V1_PREFIX` | Base API prefix | `/api/v1` |
| `SECRET_KEY` | JWT signing key | required |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token lifetime in minutes | `60` |
| `DATABASE_URL` | SQLAlchemy database URL | `sqlite:///./task_manager.db` |
| `CORS_ORIGINS` | Allowed frontend origins, comma-separated or JSON array | `http://localhost:3000,http://127.0.0.1:3000` |

## Authentication Flow

### Register

`POST /api/v1/auth/register`

Request body:

```json
{
  "email": "user@example.com",
  "password": "StrongPass123"
}
```

### Login

`POST /api/v1/auth/login`

This endpoint uses OAuth2 form data, so send:

- `username`: user email
- `password`: user password

Example:

```bash
curl -X POST 'http://127.0.0.1:8000/api/v1/auth/login' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=user@example.com&password=StrongPass123'
```

Response:

```json
{
  "access_token": "<jwt>",
  "token_type": "bearer"
}
```

### Authenticated Requests

Use the token as:

```bash
-H 'Authorization: Bearer <jwt>'
```

## API Endpoints

### Health

- `GET /health` - Service health check

### Auth

- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Obtain JWT token
- `GET /api/v1/auth/me` - Get current authenticated user

### Tasks

- `POST /api/v1/tasks/` - Create a task
- `GET /api/v1/tasks/` - List current user's tasks
- `GET /api/v1/tasks/{task_id}` - Retrieve a single task
- `PATCH /api/v1/tasks/{task_id}` - Update a task
- `DELETE /api/v1/tasks/{task_id}` - Delete a task

## Example Task Payload

```json
{
  "title": "Finish FastAPI backend",
  "description": "Implement authentication and task CRUD",
  "due_date": "2026-01-15T12:00:00Z"
}
```

## Architecture Overview

- `app/main.py` initializes FastAPI, middleware, routers, and startup lifecycle.
- `app/core/` contains configuration, database setup, and security utilities.
- `app/models/` defines SQLAlchemy ORM models.
- `app/schemas/` defines Pydantic request and response models.
- `app/crud/` holds database access logic.
- `app/api/routes/` exposes HTTP endpoints.
- `app/api/deps.py` contains reusable dependencies like JWT user resolution.

## Production Notes

- Replace SQLite with PostgreSQL by updating `DATABASE_URL`.
- Use a strong `SECRET_KEY` and never commit `.env`.
- Restrict `CORS_ORIGINS` to trusted frontend domains.
- Run behind a reverse proxy such as Nginx or a cloud load balancer.
- Use a process manager or container platform for deployment.

## License

This project is provided as-is for your use and extension.
