from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import APIRouter, Depends
from ...database import get_db_session
from ...models import Task
from ...schemas.task import TaskInDB, TaskCreate
from typing import List

router = APIRouter(
    prefix="/api/tasks",
    tags=["tasks"],
    responses={404: {"description": "Not found"}},
)


# Получение всех задач
@router.get("/get", response_model=List[TaskInDB])
async def read_tasks(skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_db_session)):
    # Выполняем запрос к базе данных, выбирая задачи с учетом смещения и ограничения
    result = await session.execute(select(Task).offset(skip).limit(limit))
    tasks = result.scalars().all()  # Преобразуем результат запроса в список объектов Task
    return tasks


@router.get("/get/{task_id}", response_model=TaskInDB)
async def read_task(task_id: int, session: AsyncSession = Depends(get_db_session)):
    result = await session.execute(select(Task).where(Task.id == task_id))
    task = result.scalars().first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/create", response_model=TaskInDB, status_code=201)
async def create_task(task: TaskCreate, session: AsyncSession = Depends(get_db_session)):
    if not task.title:
        raise HTTPException(status_code=400, detail="The title cannot be empty")
    if not isinstance(task.completed, bool):
        raise HTTPException(status_code=400, detail="Completed type error")

    # Создаем новую задачу на основе полученных данных
    new_task = Task(**task.dict())
    # Добавляем новую задачу в сессию базы данных
    session.add(new_task)
    # Фиксируем изменения в базе данных
    await session.commit()
    # Обновляем данные новой задачи в сессии
    await session.refresh(new_task)
    # Возвращаем созданную задачу
    return new_task
