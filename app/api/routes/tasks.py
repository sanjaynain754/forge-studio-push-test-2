from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.crud.task import create_task as create_task_record
from app.crud.task import delete_task, get_task, get_tasks, update_task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate


router = APIRouter(prefix='/tasks', tags=['tasks'])


@router.post('/', response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TaskResponse:
    return create_task_record(db, task_in=task_in, owner_id=current_user.id)


@router.get('/', response_model=list[TaskResponse])
def list_tasks(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    completed: bool | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[TaskResponse]:
    return get_tasks(
        db,
        owner_id=current_user.id,
        skip=skip,
        limit=limit,
        completed=completed,
    )


@router.get('/{task_id}', response_model=TaskResponse)
def retrieve_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TaskResponse:
    task = get_task(db, task_id=task_id, owner_id=current_user.id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task not found')
    return task


@router.patch('/{task_id}', response_model=TaskResponse)
def partial_update_task(
    task_id: int,
    task_in: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TaskResponse:
    task = get_task(db, task_id=task_id, owner_id=current_user.id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task not found')
    return update_task(db, db_task=task, task_in=task_in)


@router.delete('/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def remove_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Response:
    task = get_task(db, task_id=task_id, owner_id=current_user.id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task not found')
    delete_task(db, db_task=task)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
