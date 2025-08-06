from fastapi import Depends, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from db.fake_data import users_db
from models.user import UserResponse
from auth.jwt import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserResponse:
    try:
        user_id = int(decode_access_token(token))
        for user in users_db:
            if user.id == user_id:
                return user
        raise HTTPException(status_code=404, detail='User not found')
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
