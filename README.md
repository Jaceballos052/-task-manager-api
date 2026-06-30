# Task Manager API

REST API for task management built with **FastAPI**, **PostgreSQL**, **Docker** and **Pytest**.

## Tech Stack

- **FastAPI** — Modern, high-performance web framework
- **SQLAlchemy** — ORM for database interaction
- **PostgreSQL** — Production database (SQLite for local dev/testing)
- **Docker & Docker Compose** — Containerized deployment
- **Pytest + httpx** — Integration testing

## Project Structure

```
task-manager-api/
├── app/
│   ├── main.py        # FastAPI app and endpoints
│   ├── models.py      # SQLAlchemy database models
│   ├── schemas.py     # Pydantic request/response schemas
│   ├── crud.py        # Database logic (Create, Read, Update, Delete)
│   └── database.py    # Database connection and session management
├── tests/
│   └── test_api.py    # Integration tests (11 tests, 100% passing)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt       # Production dependencies
└── requirements-dev.txt   # Local development dependencies
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/tasks` | List all tasks |
| POST | `/tasks` | Create a new task |
| GET | `/tasks/{id}` | Get task by ID |
| PATCH | `/tasks/{id}` | Partially update a task |
| DELETE | `/tasks/{id}` | Delete a task |

## Getting Started

### Option 1 — Docker (recommended)

```bash
docker-compose up --build
```

API available at `http://localhost:8000`

### Option 2 — Local development

**Requirements:** Python 3.13+

```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/Mac

# Install dependencies
pip install -r requirements-dev.txt

# Run the server
uvicorn app.main:app --reload
```

API available at `http://localhost:8000`

## Interactive Documentation

FastAPI generates automatic interactive docs:

- **Swagger UI** → `http://localhost:8000/docs`
- **ReDoc** → `http://localhost:8000/redoc`

## Running Tests

```bash
pytest tests/ -v
```

Expected output:

```
tests/test_api.py::test_health_check              PASSED
tests/test_api.py::test_create_task               PASSED
tests/test_api.py::test_create_task_empty_title   PASSED
tests/test_api.py::test_list_tasks_empty          PASSED
tests/test_api.py::test_list_tasks_with_data      PASSED
tests/test_api.py::test_get_task                  PASSED
tests/test_api.py::test_get_task_not_found        PASSED
tests/test_api.py::test_update_task               PASSED
tests/test_api.py::test_update_task_not_found     PASSED
tests/test_api.py::test_delete_task               PASSED
tests/test_api.py::test_delete_task_not_found     PASSED

11 passed in 1.54s
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite:///./taskdb.db` | Database connection string |

For PostgreSQL:
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/taskdb
```

## Author

**José Ángel Ceballos Rodríguez**
- GitHub: [@Jaceballos052](https://github.com/Jaceballos052)
- LinkedIn: [José Ángel Ceballos](https://www.linkedin.com/in/josé-ángel-ceballos-rodríguez-a44996346/)
