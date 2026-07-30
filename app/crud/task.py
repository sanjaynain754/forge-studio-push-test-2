from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


def create_task(db: Session, *, task_in: TaskCreate, owner_id: int) -> Task:
    task = Task(**task_in.model_dump(), owner_id=owner_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_task(db: Session, *, task_id: int, owner_id: int) -> Task | None:
    return db.query(Task).filter(Task.id == task_id, Task.owner_id == owner_id).first()


def get_tasks(
    db: Session,
    *,
    owner_id: int,
    skip: int = 0,
    limit: int = 20,
    completed: bool | None = None,
) -> list[Task]:
    query = db.query(Task).filter(Task.owner_id == owner_id)
    if completed is not None:
        query = query.filter(Task.completed == completed)
    return query.order_by(Task.created_at.desc()).offset(skip).limit(limit).all()


def update_task(db: Session, *, db_task: Task, task_in: TaskUpdate) -> Task:
    update_data = task_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, *, db_task: Task) -> None:
    db.delete(db_task)
    db.commit()
