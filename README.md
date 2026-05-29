# AI Workflow Platform

## Overview

AI Workflow Platform is a backend-first workflow management application built with FastAPI and SQLModel. The project demonstrates modern backend engineering principles including REST API development, data validation, database persistence, layered architecture, and version-controlled software development.

The platform serves as the foundation for a future AI-powered workflow automation system capable of task classification, prioritization, and workflow orchestration using Large Language Models (LLMs).

---

## Features

### Current Features

- FastAPI REST API
- CRUD Operations (Create, Read, Update, Delete)
- Pydantic Data Validation
- SQLite Database Persistence
- SQLModel ORM Integration
- Layered Backend Architecture
- Git & GitHub Version Control
- Swagger UI API Documentation
- Health Check Endpoint

### Planned Features

- PostgreSQL Integration
- AI-Powered Task Classification
- AI Workflow Recommendations
- Task Prioritization Engine
- OpenAI / Groq Integration
- Workflow Analytics Dashboard
- Authentication & Authorization
- Deployment to Cloud Infrastructure

---

## Tech Stack

### Backend

- Python 3.11+
- FastAPI
- SQLModel
- SQLite

### Validation

- Pydantic

### API Documentation

- Swagger UI
- OpenAPI

### Version Control

- Git
- GitHub

### Future Technologies

- PostgreSQL
- OpenAI API / Groq API
- Docker
- React

---

## Project Structure

```text
ai-workflow-platform/
│
├── app/
│   ├── main.py
│   ├── crud.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   │
│   ├── routes/
│   │   └── registration.py
│   │
│   └── services/
│       └── workflow_service.py
│
├── .gitignore
├── requirements.txt
├── README.md
└── LICENSE
```

## Architecture Overview

Client

↓

FastAPI Routes

↓

CRUD Layer

↓

Database Layer

↓

SQLite Database

### Responsibilities

**main.py**

- Application entry point
- Route registration
- FastAPI configuration

**crud.py**

- Database operations
- Create, Read, Update, Delete logic

**database.py**

- Database engine creation
- Connection management

**models.py**

- SQLModel database models
- Table definitions

**schemas.py**

- Request validation
- Response schemas

**services/**

- Business logic
- Future AI integrations

**routes/**

- API endpoint definitions

---

## Installation

### Clone Repository

git clone https://github.com/lomeeshan/ai-workflow-platform.git

cd ai-workflow-platform

### Create Virtual Environment

python -m venv venv

### Activate Virtual Environment

Mac/Linux:

source venv/bin/activate

Windows:

venv\Scripts\activate

### Install Dependencies

pip install -r requirements.txt

---

## Running The Application

Start the development server:

uvicorn app.main:app --reload

Server:

http://127.0.0.1:8000

Swagger Documentation:

http://127.0.0.1:8000/docs

---

## API Endpoints

### Health Check

GET /health

### Create Task

POST /tasks

### Get All Tasks

GET /tasks

### Get Task By ID

GET /tasks/{task_id}

### Update Task

PUT /tasks/{task_id}

### Delete Task

DELETE /tasks/{task_id}

---

## Learning Objectives

This project was built to develop practical skills in:

- Backend Engineering
- REST API Development
- Database Design
- Data Validation
- Software Architecture
- Git & GitHub Workflows
- AI Application Development
- Production Software Practices

---

## Roadmap

### Phase 1

- FastAPI Fundamentals
- CRUD Operations
- SQLite Integration
- Layered Architecture

### Phase 2

- PostgreSQL Migration
- Environment Variables
- Configuration Management

### Phase 3

- AI Integration
- LLM APIs
- Workflow Automation

### Phase 4

- Frontend Dashboard
- Authentication
- Deployment

---

## License

This project is licensed under the MIT License.
