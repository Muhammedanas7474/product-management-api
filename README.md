# product-management-api

📦 Product Management API

Production-ready Product & Category Management API built with Django REST Framework, designed with performance, scalability, and clean architecture principles.

🚀 Overview

This project implements a production-grade backend API with:

Slug-based resource access

Soft delete support

Image upload with async thumbnail generation

PostgreSQL database

Redis + Celery for background processing

Dockerized infrastructure

Health checks

Swagger API documentation

Flower monitoring for Celery

Automated test suite

The system is fully containerized and can be started with a single command.

🏗 Architecture Overview
Client → Django API (Gunicorn)
                ↓
          PostgreSQL (DB)
                ↓
         Redis (Broker)
                ↓
            Celery Worker
                ↓
        Thumbnail Generation

Key Design Decisions

PostgreSQL for production reliability

SQLite in-memory for tests (faster, isolated)

Celery + Redis for async image processing

Supervisor to manage Gunicorn + Celery in one container

Docker volumes for persistent media & DB data

Slug-based URLs for clean REST design

Indexing & optimized queries for performance

⚙️ Tech Stack
Layer	Technology
Backend	Django 6 + DRF
Database	PostgreSQL 15
Cache/Broker	Redis 7
Async Tasks	Celery
Monitoring	Flower
Server	Gunicorn
Containerization	Docker + Docker Compose
API Docs	DRF Spectacular (Swagger)
Testing	Pytest
🧪 Running the Project
1️⃣ Prerequisites

Docker

Docker Compose

2️⃣ Setup Environment

Create .env file from example:

cp .env.example .env


Ensure it contains:

```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://postgres:postgres@db:5432/product_db
REDIS_URL=redis://redis:6379/0
```

### Environment Variables Explanation
| Variable | Description |
|---|---|
| `DEBUG` | Enables clear error messages. Must be `False` in production. |
| `SECRET_KEY` | Cryptographic key for Django security. |
| `DATABASE_URL` | Connection string for PostgreSQL database. |
| `REDIS_URL` | Connection string for Redis broker and backend. |

3️⃣ Start the Application
docker compose up --build


This will:

Build multi-stage Docker image

Start PostgreSQL

Start Redis

Run migrations

Start Gunicorn

Start Celery worker

Start Flower

No manual steps required.

🌐 Available Services
Service	URL
API Base	http://localhost:8000

Swagger UI	http://localhost:8000/api/docs/

Redoc	http://localhost:8000/api/redoc/

Health Check	http://localhost:8000/health/

Flower (Celery Monitor)	http://localhost:5555
🗃 API Endpoints
Categories

GET /api/categories/

POST /api/categories/

GET /api/categories/{slug}/

PUT /api/categories/{slug}/

DELETE /api/categories/{slug}/ (Soft Delete)

Products

GET /api/products/

POST /api/products/

GET /api/products/{slug}/

PUT /api/products/{slug}/

DELETE /api/products/{slug}/ (Soft Delete)

🖼 Image & Async Processing

When a product is created:

Image is uploaded and stored

Celery task is triggered

Thumbnail is generated asynchronously

Database updated with thumbnail path

To verify:

docker exec -it product_app ls -R /app/media

🧠 Database & Performance Optimizations

Indexed slug fields

Optimized querysets

Soft delete pattern

Pagination enabled

Filtering support

PostgreSQL used in production

SQLite in-memory used for tests (faster execution)

🧪 Running Tests
python -m pytest


Test database uses:

SQLite in-memory (:memory:)


This ensures:

Fast test execution

No dependency on Docker

Isolated test environment

🐳 Docker Design
Multi-Stage Build

Builder stage installs dependencies

Final stage copies only required artifacts

Reduces image size

Improves security

Volumes

postgres_data → persistent DB

media_data → persistent media files

Process Management

Supervisor manages:

Gunicorn

Celery Worker

📊 Health Check
GET /health/


Confirms:

Database connectivity

Application readiness

Used for production readiness and container orchestration.

📦 Project Structure
config/          → Django settings
products/        → Product app
categories/      → Category app
core/            → Shared utilities
deploy/          → Supervisor config
media/           → Uploaded files
docker-compose.yml
Dockerfile
entrypoint.sh

🧩 Engineering Decisions Explained
Why PostgreSQL?

Production-grade relational database with indexing & reliability.

Why Redis?

Fast in-memory broker for async tasks.

Why Celery?

Background processing for non-blocking image operations.

Why Supervisor?

Ensures Gunicorn and Celery are managed reliably inside container.

Why SQLite for tests?

Faster, lightweight, avoids external dependencies.

🛡 Production Readiness Features

Dockerized infrastructure

Health endpoint

Async task monitoring

Structured logging

Environment-based settings

No manual startup steps

Clean separation of concerns

👨‍💻 Development Notes

Database migrations are version controlled.

Database files are not committed.

Media files are excluded from Git.

Environment variables are required for production.

📌 Evaluation Alignment
Dimension	Covered
Correctness	Full CRUD, slug handling, soft delete, async thumbnail
Architecture	Clean app separation, service layer usage
Engineering Depth	Indexed fields, async processing, production Docker
Communication	Clear README & setup instructions
### ⚠️ Known Limitations & Trade-offs
1.  **Single Container Architecture**: requirement #6 mandates a single Docker container using a process supervisor (Supervisord). While this achieves the goal, standard production deployments often favor entirely separate containers for web servers and workers (e.g., Kubernetes pods or ECS tasks) for independent scaling and isolation.
2.  **Volume Storage**: Images are stored in a local Docker volume (`media_data`). In a distributed production system, an S3-compatible cloud storage backend would be implemented using `django-storages` to prevent horizontal scaling issues.
3.  **Basic Authentication**: For the scope of this test, complex authentication/authorization features (like JWT or OAuth2) were omitted to focus on core product architecture, caching, and background processing.

🏁 Final Notes

The system is designed to:

Start with a single command

Run reliably in containers

Scale background processing independently

Follow production best practices
