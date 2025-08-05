from fastapi import FastAPI, status, HTTPException
from db.fake_data import users_db
from models.user import UserRequest, UserResponse
from auth.hash import hash_password
from datetime import datetime

app = FastAPI()


@app.get("/user/username/{username}")
async def get_user_by_username(username: str):
    for user in users_db:
        if user.username == username:
            return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')



@app.get("/user/id/{user_id}")
async def get_user_by_id(user_id: int):
    for user in users_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')



@app.post("/user/create", response_model=UserResponse)
async def create_user(user: UserRequest):
    new_id = len(users_db) + 1

    new_user = UserResponse(
        id=new_id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hash_password(user.password),
        is_active=user.is_active,
        is_admin=user.is_admin,
        status=user.status,
        avatar_url=user.avatar_url,
        created_at=datetime.now(),
        last_seen=datetime.now()
    )

    users_db.append(new_user)
    return new_user



@app.put("/user/status/{user_id}")
async def update_status(user_id: int, status: str):
    for user in users_db:
        if user.id == user_id:
            user.status = status
            user.last_seen = datetime.now()
            return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
