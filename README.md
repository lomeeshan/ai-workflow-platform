# AI Workflow Platform

A backend API for an AI-powered workflow platform that helps users create, organize, analyze, and re-analyze tasks using a large language model.

This project was built to practice production-style backend development with FastAPI, PostgreSQL, Alembic migrations, structured LLM integration, automated testing, and Dockerized local development.

---

## Features

* Create, read, update, delete, and filter tasks
* AI-powered task analysis using Groq LLMs
* Automatic task classification by category
* Automatic priority estimation
* Automatic effort estimation
* AI-generated task summaries and reasoning
* Re-analyze existing tasks with updated AI output
* Task lifecycle tracking with status values
* PostgreSQL database persistence
* Alembic database migrations
* Pydantic request and response validation
* Custom error handling for LLM failures
* Automated API tests with Pytest
* Mocked LLM tests to avoid real API calls during testing
* Docker Compose setup for running FastAPI and PostgreSQL together

---

## Tech Stack

### Backend

* Python
* FastAPI
* SQLModel
* Pydantic
* Uvicorn

### Database

* PostgreSQL
* Alembic

### AI Integration

* Groq API
* LLM-based task analysis
* Structured JSON validation with Pydantic

### Testing

* Pytest
* FastAPI TestClient
* Mocked LLM workflows

### DevOps

* Docker
* Docker Compose
* Environment variable configuration
* Git/GitHub

---

## Quick Start

The easiest way to run this project is with Docker Compose.

### 1. Clone the repository

```bash
git clone https://github.com/lomeeshan/ai-workflow-platform.git
cd ai-workflow-platform
```

### 2. Create a `.env` file

Create a `.env` file in the project root.

For Docker, the minimum required value is:

```env
GROQ_API_KEY=your_groq_api_key_here
```

The PostgreSQL database connection for Docker is already configured inside `docker-compose.yml`.

### 3. Start the project

```bash
docker compose up --build
```

This starts both services:

```text
api  -> FastAPI backend
db   -> PostgreSQL database
```

The API will be available at:

```text
http://localhost:8000
```

### 4. Run database migrations

Open a second terminal in the project folder and run:

```bash
docker compose exec api alembic upgrade head
```

This creates or updates the database tables inside the Docker PostgreSQL database.

### 5. Open the API docs

Go to:

```text
http://localhost:8000/docs
```

From there, you can test the API endpoints in Swagger UI.

### 6. Stop the project

```bash
docker compose down
```

This stops the containers but keeps the PostgreSQL Docker volume.

To stop the project and delete the Docker PostgreSQL database volume:

```bash
docker compose down -v
```

Warning: `docker compose down -v` deletes the Docker database data.

---

## Project Structure

```text
ai-workflow-platform/
├── app/
│   ├── main.py
│   ├── crud.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── exceptions.py
│   ├── routes/
│   │   └── tasks.py
│   └── services/
│       ├── llm_service.py
│       └── workflow_service.py
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_tasks.py
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .env.example
├── .gitignore
├── alembic.ini
├── requirements.txt
├── README.md
└── LICENSE
```

---

## Architecture Overview

The project follows a layered backend architecture:

```text
Client / Swagger UI
        ↓
FastAPI Application
        ↓
Routes Layer
        ↓
Workflow Service Layer
        ↓
LLM Service / CRUD Layer
        ↓
SQLModel ORM
        ↓
PostgreSQL Database
```

### Layer Responsibilities

| Layer                 | Responsibility                                                     |
| --------------------- | ------------------------------------------------------------------ |
| `main.py`             | Creates the FastAPI app and includes routers                       |
| `routes/tasks.py`     | Defines HTTP endpoints and handles request/response behavior       |
| `workflow_service.py` | Coordinates business workflows such as AI analysis and re-analysis |
| `llm_service.py`      | Handles Groq API calls and validates LLM responses                 |
| `crud.py`             | Handles database operations                                        |
| `models.py`           | Defines database table models                                      |
| `schemas.py`          | Defines request, response, and AI validation schemas               |
| `database.py`         | Creates database engine and session dependency                     |
| `exceptions.py`       | Defines custom application exceptions                              |

---

## API Endpoints

### Health

| Method | Endpoint  | Description      |
| ------ | --------- | ---------------- |
| GET    | `/health` | Check API health |

### Tasks

| Method | Endpoint                     | Description                            |
| ------ | ---------------------------- | -------------------------------------- |
| POST   | `/tasks/`                    | Create a task with AI analysis         |
| GET    | `/tasks/`                    | Get all tasks                          |
| GET    | `/tasks/{task_id}`           | Get a task by ID                       |
| PUT    | `/tasks/{task_id}`           | Update a task                          |
| DELETE | `/tasks/{task_id}`           | Delete a task                          |
| GET    | `/tasks/filter/`             | Filter tasks                           |
| POST   | `/tasks/{task_id}/reanalyze` | Re-run AI analysis on an existing task |

---

## Example Task Creation Request

```json
{
  "title": "Prepare for database systems exam",
  "description": "Review SQL joins, normalization, indexing, transactions, and ER diagrams."
}
```

Example response:

```json
{
  "id": 1,
  "title": "Prepare for database systems exam",
  "description": "Review SQL joins, normalization, indexing, transactions, and ER diagrams.",
  "category": "school",
  "priority": "high",
  "estimated_effort": "medium",
  "ai_summary": "Study core database systems concepts before the exam.",
  "ai_reasoning": "The task is academic and involves multiple technical topics that require focused preparation.",
  "status": "pending",
  "created_at": "2026-06-11T10:00:00Z",
  "updated_at": "2026-06-11T10:00:00Z"
}
```

---

## Environment Variables

Create a `.env` file in the project root.

Use `.env.example` as a template:

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/ai_workflow_db
GROQ_API_KEY=your_groq_api_key_here
```

Important:

* Do not commit your real `.env` file.
* Do not expose your real Groq API key.
* `.env.example` should contain placeholders only.
* For Docker, `docker-compose.yml` provides the database URL inside the API container.

---

## Running Locally Without Docker

Use this option if you want to run the FastAPI app directly on your machine instead of using Docker.

### 1. Clone the repository

```bash
git clone https://github.com/lomeeshan/ai-workflow-platform.git
cd ai-workflow-platform
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create your `.env` file

```bash
cp .env.example .env
```

Then update `.env` with your real PostgreSQL database URL and Groq API key.

### 5. Run Alembic migrations

```bash
alembic upgrade head
```

### 6. Start the FastAPI server

```bash
uvicorn app.main:app --reload
```

### 7. Open Swagger UI

Go to:

```text
http://localhost:8000/docs
```

---

## Running with Docker

Docker Compose starts two services:

```text
api  -> FastAPI backend
db   -> PostgreSQL database
```

### 1. Start the containers

```bash
docker compose up --build
```

### 2. Run database migrations

In a second terminal, run:

```bash
docker compose exec api alembic upgrade head
```

### 3. Open Swagger UI

Go to:

```text
http://localhost:8000/docs
```

### 4. Stop the containers

```bash
docker compose down
```

To stop the containers and delete the PostgreSQL Docker volume:

```bash
docker compose down -v
```

Warning: `docker compose down -v` deletes the Docker database data.

---

## Docker Notes

Inside Docker Compose, the API connects to PostgreSQL using:

```text
db:5432
```

This is because `db` is the Compose service name for the PostgreSQL container.

From inside the API container, `localhost` refers to the API container itself, not the PostgreSQL container.

So the Docker database URL uses:

```text
postgresql://postgres:postgres@db:5432/ai_workflow_db
```

The PostgreSQL service also uses a Docker volume:

```yaml
volumes:
  - postgres_data:/var/lib/postgresql/data
```

This allows database data to persist across normal container restarts.

---

## Running Tests

Run the test suite with:

```bash
pytest
```

The tests use a separate SQLite test database and FastAPI dependency overrides, so they do not modify the real PostgreSQL database.

The test suite covers:

* health check endpoint
* reading tasks
* reading a task by ID
* 404 behavior for missing tasks
* updating task status
* validation errors for invalid status values
* filtering tasks
* deleting tasks
* creating tasks with a mocked LLM response
* re-analyzing tasks with a mocked LLM response
* LLM service failure handling
* invalid LLM response handling

---

## Why Mock the LLM in Tests?

The project uses mocked LLM responses in tests because real LLM API calls are:

* slower
* non-deterministic
* dependent on internet access
* dependent on API keys
* potentially limited by rate limits or quota

Mocking allows the backend workflow to be tested reliably without calling Groq during automated tests.

---

## Database Migrations

This project uses Alembic for database migrations.

To create a new migration after changing `models.py`:

```bash
alembic revision --autogenerate -m "describe migration"
```

To apply migrations:

```bash
alembic upgrade head
```

Alembic is used instead of relying only on `SQLModel.metadata.create_all()` because migrations track schema changes over time and make database changes reproducible.

---

## Example Workflow

A typical workflow looks like this:

1. User creates a task through the API.
2. FastAPI receives and validates the request.
3. The workflow service sends the task title and description to the LLM service.
4. The LLM returns structured JSON.
5. Pydantic validates the AI output.
6. The task and AI analysis are saved in PostgreSQL.
7. The API returns the saved task to the user.
8. The user can later update, filter, delete, or re-analyze the task.

---

## Error Handling

The project uses custom exceptions for LLM-related failures:

```text
LLMServiceError
InvalidLLMResponseError
DatabaseOperationError
```

Examples:

| Error Type           | API Response             |
| -------------------- | ------------------------ |
| Groq API unavailable | 503 Service Unavailable  |
| Invalid LLM JSON     | 502 Bad Gateway          |
| Task not found       | 404 Not Found            |
| Invalid request data | 422 Unprocessable Entity |

This separates low-level service failures from HTTP response handling.

---

## Key Learning Goals

This project was built to practice:

* backend API design
* layered architecture
* database modeling
* PostgreSQL integration
* Alembic migrations
* LLM integration
* structured AI output validation
* custom error handling
* automated API testing
* mocking external services
* Dockerized local development
* project documentation

---

## Future Improvements

Possible future improvements:

* Add user authentication
* Add user accounts and task ownership
* Add frontend dashboard
* Add deployment to a cloud platform
* Add CI/CD with GitHub Actions
* Add pagination for task lists
* Add more advanced filtering and search
* Add background task processing
* Add observability and structured logging

---

## Project Status

Current status:

```text
Backend API: Complete
PostgreSQL integration: Complete
Alembic migrations: Complete
LLM integration: Complete
Testing: Complete
Docker Compose setup: Complete
README documentation: Complete
Deployment: Future improvement
```

---

## License

This project is licensed under the MIT License.

