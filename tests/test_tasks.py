from sqlmodel import Session

from app.models import Task
from tests.conftest import engine


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


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
