from datetime import datetime, timedelta
from jose import jwt, JWTError
from core import config


def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})

    encoded_jwt = jwt.encode(
        to_encode,
        setting.JWT_SECRET_KEY,
        algorithm=setting.JWT_ALGORITHM
    )
    return encoded_jwt

def decode_access_token(token: str) -> int:
    try:
        payload = jwt.decode(token, setting.JWT_SECRET_KEY, algorithms=[setting.JWT_ALGORITHM])
        user_id: int = payload.get('sub')
        if user_id is None:
            raise ValueError('Token payload missing user_id')
        return user_id
    except JWTError:
        raise


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(days=7) 
    to_encode.update({'exp': expire})

    encoded_jwt = jwt.encode(
        to_encode,
        setting.JWT_SECRET_KEY,
        algorithm=setting.JWT_ALGORITHM
    )
    return encoded_jwt


def decode_refresh_token(token: str) -> int:
    try:
        payload = jwt.decode(token, setting.JWT_SECRET_KEY, algorithms=[setting.JWT_ALGORITHM])
        user_id: int = payload.get('sub')
        if user_id is None:
            raise ValueError('Token payload missing user_id')
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
