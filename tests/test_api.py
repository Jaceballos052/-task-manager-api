import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

# Base de datos SQLite en memoria para tests (no necesita PostgreSQL)
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Sustituye la BD real por la de test
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    """Crea las tablas antes de cada test y las elimina después."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)


# ── Health check ──────────────────────────────────────────────────────────────

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


# ── Crear tarea ───────────────────────────────────────────────────────────────

def test_create_task():
    payload = {"title": "Aprender FastAPI", "priority": "high"}
    response = client.post("/tasks", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Aprender FastAPI"
    assert data["priority"] == "high"
    assert data["completed"] is False
    assert "id" in data


def test_create_task_empty_title():
    response = client.post("/tasks", json={"title": ""})
    assert response.status_code == 422  # Validation error


# ── Listar tareas ─────────────────────────────────────────────────────────────

def test_list_tasks_empty():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_with_data():
    client.post("/tasks", json={"title": "Tarea 1"})
    client.post("/tasks", json={"title": "Tarea 2"})

    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 2


# ── Obtener tarea por ID ──────────────────────────────────────────────────────

def test_get_task():
    created = client.post("/tasks", json={"title": "Mi tarea"}).json()
    response = client.get(f"/tasks/{created['id']}")

    assert response.status_code == 200
    assert response.json()["title"] == "Mi tarea"


def test_get_task_not_found():
    response = client.get("/tasks/999")
    assert response.status_code == 404


# ── Actualizar tarea ──────────────────────────────────────────────────────────

def test_update_task():
    created = client.post("/tasks", json={"title": "Tarea original"}).json()
    response = client.patch(f"/tasks/{created['id']}", json={"completed": True})

    assert response.status_code == 200
    assert response.json()["completed"] is True
    assert response.json()["title"] == "Tarea original"  # No cambió


def test_update_task_not_found():
    response = client.patch("/tasks/999", json={"completed": True})
    assert response.status_code == 404


# ── Eliminar tarea ────────────────────────────────────────────────────────────

def test_delete_task():
    created = client.post("/tasks", json={"title": "Borrar esto"}).json()
    response = client.delete(f"/tasks/{created['id']}")

    assert response.status_code == 204
    assert client.get(f"/tasks/{created['id']}").status_code == 404


def test_delete_task_not_found():
    response = client.delete("/tasks/999")
    assert response.status_code == 404
