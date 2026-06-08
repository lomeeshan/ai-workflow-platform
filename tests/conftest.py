import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine

from app.main import app
from app.database import get_session
from app.models import Task


TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)


def override_get_session():
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture():
    SQLModel.metadata.create_all(engine)

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="sample_task")
def sample_task_fixture():
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        task = Task(
            title="Test Task",
            description="This is a test task.",
            category="technical",
            priority="high",
            estimated_effort="medium",
            ai_summary="Test summary",
            ai_reasoning="Test reasoning",
            status="pending",
        )

        session.add(task)
        session.commit()
        session.refresh(task)

        return task
