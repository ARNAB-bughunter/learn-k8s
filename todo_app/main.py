from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
import uuid

from database import init_db, get_db, TodoModel

app = FastAPI(title="Todo API")


# ── Pydantic schemas ──────────────────────────────────────────────────────────

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = ""


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class Todo(BaseModel):
    id: str
    title: str
    description: str
    completed: bool

    model_config = {"from_attributes": True}


# ── Startup ───────────────────────────────────────────────────────────────────

@app.on_event("startup")
async def startup():
    await init_db()


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/api/todos", response_model=list[Todo])
async def get_todos(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TodoModel))
    return result.scalars().all()


@app.post("/api/todos", response_model=Todo, status_code=201)
async def create_todo(todo: TodoCreate, db: AsyncSession = Depends(get_db)):
    row = TodoModel(
        id=str(uuid.uuid4()),
        title=todo.title,
        description=todo.description or "",
        completed=False,
    )
    db.add(row)
    await db.commit()
    await db.refresh(row)
    return row


@app.patch("/api/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: str, update: TodoUpdate, db: AsyncSession = Depends(get_db)):
    row = await db.get(TodoModel, todo_id)
    if not row:
        raise HTTPException(status_code=404, detail="Todo not found")
    if update.title is not None:
        row.title = update.title
    if update.description is not None:
        row.description = update.description
    if update.completed is not None:
        row.completed = update.completed
    await db.commit()
    await db.refresh(row)
    return row


@app.delete("/api/todos/{todo_id}", status_code=204)
async def delete_todo(todo_id: str, db: AsyncSession = Depends(get_db)):
    row = await db.get(TodoModel, todo_id)
    if not row:
        raise HTTPException(status_code=404, detail="Todo not found")
    await db.delete(row)
    await db.commit()


@app.delete("/api/todos", status_code=204)
async def clear_completed(db: AsyncSession = Depends(get_db)):
    await db.execute(delete(TodoModel).where(TodoModel.completed == True))
    await db.commit()


# ── Static / frontend ─────────────────────────────────────────────────────────

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root():
    return FileResponse("static/index.html")
