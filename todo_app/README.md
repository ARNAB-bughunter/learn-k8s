# Todo App

A full-stack Todo application built with **FastAPI**, **PostgreSQL**, and a vanilla JS frontend. Supports creating, updating, completing, and deleting todos via a REST API.

---

## Tech Stack

| Layer     | Technology                        |
|-----------|-----------------------------------|
| Backend   | FastAPI + Uvicorn                 |
| Database  | PostgreSQL (async via SQLAlchemy) |
| Frontend  | Static HTML/JS (`static/`)        |
| Container | Docker + Docker Compose           |

---

## Project Structure

```
todo_app/
├── main.py            # FastAPI app & API routes
├── database.py        # SQLAlchemy models & DB setup
├── static/
│   └── index.html     # Frontend UI
├── requirements.txt   # Python dependencies
├── Dockerfile
├── docker-compose.yml
├── .env.example       # Environment variable template
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.12+
- PostgreSQL running locally **or** Docker + Docker Compose

---

### Option 1 — Run Locally (without Docker)

**Step 1 — Clone the repo**

```bash
git clone <repo-url>
cd todo_app
```

**Step 2 — Create and activate a virtual environment**

```bash
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
.venv\Scripts\activate           # Windows
```

**Step 3 — Install dependencies**

```bash
pip install -r requirements.txt
```

**Step 4 — Configure environment variables**

```bash
cp .env.example .env
```

Edit `.env` and set your database credentials:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=todos
```

The app reads `DATABASE_URL` from `.env`. If not set, it defaults to:

```
postgresql+asyncpg://postgres:postgres@localhost:5432/todos
```

**Step 5 — Make sure PostgreSQL is running and the database exists**

```bash
psql -U postgres -c "CREATE DATABASE todos;"
```

**Step 6 — Start the server**

```bash
uvicorn main:app --reload
```

**Step 7 — Open the app**

Visit [http://localhost:8000](http://localhost:8000) in your browser.

---

### Option 2 — Run with Docker Compose

**Step 1 — Clone the repo**

```bash
git clone <repo-url>
cd todo_app
```

**Step 2 — Configure environment variables**

```bash
cp .env.example .env
```

Edit `.env` as needed.

**Step 3 — Create the shared Docker network**

```bash
docker network create todo_net
```

**Step 4 — Start a PostgreSQL container on that network**

```bash
docker run --network todo_net --name postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=todos \
  -p 5432:5432 -d postgres
```

**Step 5 — Build and start the app**

```bash
docker compose up -d
```

**Step 6 — Open the app**

Visit [http://localhost:8000](http://localhost:8000) in your browser.

**Step 7 — Stop the containers**

```bash
docker compose down
```

---

## API Endpoints

| Method   | Endpoint              | Description                  |
|----------|-----------------------|------------------------------|
| `GET`    | `/api/todos`          | List all todos               |
| `POST`   | `/api/todos`          | Create a new todo            |
| `PATCH`  | `/api/todos/{id}`     | Update a todo (partial)      |
| `DELETE` | `/api/todos/{id}`     | Delete a specific todo       |
| `DELETE` | `/api/todos`          | Delete all completed todos   |

Interactive API docs are available at [http://localhost:8000/docs](http://localhost:8000/docs).

---

## Environment Variables

| Variable           | Default     | Description                  |
|--------------------|-------------|------------------------------|
| `POSTGRES_USER`    | `postgres`  | PostgreSQL username           |
| `POSTGRES_PASSWORD`| `postgres`  | PostgreSQL password           |
| `POSTGRES_DB`      | `todos`     | PostgreSQL database name      |
| `DATABASE_URL`     | *(derived)* | Full async DB connection URL  |
