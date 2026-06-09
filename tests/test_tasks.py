import pytest
from sqlmodel import Session
from app.models import Task
from tests.conftest import engine
from app.schemas import TaskAnalysis
from app.exceptions import LLMServiceError, InvalidLLMResponseError


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def fake_analyze_task_with_llm(title: str, description: str) -> TaskAnalysis:
    return TaskAnalysis(
        category="technical",
        priority="high",
        estimated_effort="medium",
        summary="Mocked AI summary.",
        reasoning="Mocked AI reasoning.",
    )

def test_create_task_with_mocked_llm(client, monkeypatch):
    monkeypatch.setattr(
        "app.services.workflow_service.analyze_task_with_llm",
        fake_analyze_task_with_llm,
    )

    response = client.post(
        "/tasks/",
        json={
            "title": "Build Docker setup",
            "description": "Create Dockerfile and docker-compose for the backend.",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Build Docker setup"
    assert data["description"] == "Create Dockerfile and docker-compose for the backend."
    assert data["category"] == "technical"
    assert data["priority"] == "high"
    assert data["estimated_effort"] == "medium"
    assert data["ai_summary"] == "Mocked AI summary."
    assert data["ai_reasoning"] == "Mocked AI reasoning."
    assert data["status"] == "pending"
    assert "created_at" in data
    assert "updated_at" in data



def test_reanalyze_task_with_mocked_llm(client, sample_task, monkeypatch):
    monkeypatch.setattr(
        "app.services.workflow_service.analyze_task_with_llm",
        fake_analyze_task_with_llm,
    )

    response = client.post(f"/tasks/{sample_task.id}/reanalyze")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == sample_task.id
    assert data["title"] == "Test Task"
    assert data["description"] == "This is a test task."
    assert data["category"] == "technical"
    assert data["priority"] == "high"
    assert data["estimated_effort"] == "medium"
    assert data["ai_summary"] == "Mocked AI summary."
    assert data["ai_reasoning"] == "Mocked AI reasoning."


def fake_llm_service_failure(title: str, description: str):
    raise LLMServiceError("Mocked Groq failure.")

def test_create_task_llm_service_failure(client, monkeypatch):
    monkeypatch.setattr(
        "app.services.workflow_service.analyze_task_with_llm",
        fake_llm_service_failure,
    )

    response = client.post(
        "/tasks/",
        json={
            "title": "Task that fails",
            "description": "This task should trigger mocked LLM failure.",
        },
    )

    assert response.status_code == 503
    assert response.json() == {
        "detail": "AI analysis service is currently unavailable. Please try again later."
    }


def fake_invalid_llm_response(title: str, description: str):
    raise InvalidLLMResponseError("Mocked invalid LLM response.")

def test_create_task_invalid_llm_response(client, monkeypatch):
    monkeypatch.setattr(
        "app.services.workflow_service.analyze_task_with_llm",
        fake_invalid_llm_response,
    )

    response = client.post(
        "/tasks/",
        json={
            "title": "Task with invalid AI response",
            "description": "This task should trigger mocked invalid AI output.",
        },
    )

    assert response.status_code == 502
    assert response.json() == {
        "detail": "AI analysis service returned an invalid response. Please try again."
    }



def test_get_empty_tasks(client):
    response = client.get("/tasks/")

    assert response.status_code == 200
    assert response.json() == []


def test_get_task_by_id(client, sample_task):
    response = client.get(f"/tasks/{sample_task.id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == sample_task.id
    assert data["title"] == "Test Task"
    assert data["description"] == "This is a test task."
    assert data["category"] == "technical"
    assert data["priority"] == "high"
    assert data["estimated_effort"] == "medium"
    assert data["status"] == "pending"


def test_get_task_not_found(client):
    response = client.get("/tasks/999999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_update_task_status(client, sample_task):
    response = client.put(
        f"/tasks/{sample_task.id}",
        json={"status": "in_progress"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == sample_task.id
    assert data["status"] == "in_progress"
    assert data["title"] == "Test Task"


def test_update_task_invalid_status(client, sample_task):
    response = client.put(
        f"/tasks/{sample_task.id}",
        json={"status": "almost_done"},
    )

    assert response.status_code == 422


def test_filter_tasks_by_status(client, sample_task):
    response = client.get("/tasks/filter/?status=pending")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["id"] == sample_task.id
    assert data[0]["status"] == "pending"


def test_filter_tasks_no_match(client, sample_task):
    response = client.get("/tasks/filter/?status=completed")

    assert response.status_code == 200
    assert response.json() == []


def test_delete_task(client, sample_task):
    response = client.delete(f"/tasks/{sample_task.id}")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Task deleted successfully",
        "deleted_task_id": sample_task.id,
    }

    get_response = client.get(f"/tasks/{sample_task.id}")

    assert get_response.status_code == 404




