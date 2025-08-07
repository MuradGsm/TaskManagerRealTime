from fastapi import HTTPException, status, Depends
from db.fake_data import tasks_db, task_id_counter
from models.task import TaskRequest, TaskResponse
from datetime import datetime
from auth.deps import get_current_user
from models.user import UserResponse

async def get_all_tasks_service(user: UserResponse = Depends(get_current_user)):
    users_tasks = [task for task in tasks_db if task.created_by == user.id]
    return {"all_tasks": users_tasks}


async def get_task_service(task_id: int, user: UserResponse = Depends(get_current_user)):
    for task in tasks_db:
        if task.id == task_id:
            if task.created_by != user.id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized')
            return task
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")


async def create_task_service(task_data: TaskRequest, user: UserResponse = Depends(get_current_user)):
    new_task = TaskResponse(
        id=next(task_id_counter),
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        created_by=user.id,
        assigned_to=task_data.assigned_to,
        watchers=task_data.watchers,
        comments=task_data.comments,
        due_date=task_data.due_date,
        created_at=datetime.now()
    )
    tasks_db.append(new_task)
    return new_task


async def update_task_service(task_id: int, task_data: TaskRequest, user: UserResponse = Depends(get_current_user)):
    for task in tasks_db:
        if task.id == task_id:
            if task.created_by != user.id:
                raise HTTPException(status_code=403, detail="Not authorized")
            task.title = task_data.title
            task.description = task_data.description
            task.status = task_data.status
            task.assigned_to = task_data.assigned_to
            task.watchers = task_data.watchers
            task.comments = task_data.comments
            task.due_date = task_data.due_date
            return task
    raise HTTPException(status_code=404, detail="Task not found")


async def delete_task_service(task_id: int, user: UserResponse = Depends(get_current_user)):
    for task in tasks_db:
        if task.id == task_id:
            if task.created_by != user.id:
                raise HTTPException(status_code=403, detail="Not authorized")
            tasks_db.remove(task)
            return {"detail": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")


async def assign_task_to_user_service(task_id: int, user_id: int, user: UserResponse = Depends(get_current_user)):
    for task in tasks_db:
        if task.id == task_id:
            if task.created_by != user.id:
                raise HTTPException(status_code=403, detail="Not authorized")
            task.assigned_to = user_id
            return task
    raise HTTPException(status_code=404, detail="Task not found")
