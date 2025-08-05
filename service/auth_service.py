from fastapi import status, HTTPException
from db.fake_data import users_db
from models.user import UserRequest, UserResponse
from auth.hash import hash_password,verify_password
from datetime import datetime
from auth.jwt import create_access_token, create_refresh_token




async def register_service(user_data: UserRequest):
  for user in users_db:
      if user.username == user_data.username or user.email == user_data.email:
          raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already exists')

  new_id = len(users_db) + 1

  new_user = UserResponse(
      id=new_id,
      username=user_data.username,
      email=user_data.email,
      full_name=user_data.full_name,
      hashed_password=hash_password(user_data.password),
      is_active=user_data.is_active,
      is_admin=user_data.is_admin,
      status=user_data.status,
      avatar_url=user_data.avatar_url,
      created_at=datetime.now(),
      last_seen=datetime.now()
  )

  users_db.append(new_user)
  return new_user

async def login_service(username: str, password: str):
    for user in users_db:
        if user.username == username:
            if verify_password(password, user.hashed_password):
                access_token = create_access_token(data={"sub": str(user.id)})
                refresh_token = create_refresh_token(data={"sub": str(user.id)})

                return {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "token_type": "bearer"
                }
            else:
                raise       HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid password")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

