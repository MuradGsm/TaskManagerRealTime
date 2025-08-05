from fastapi import APIRouter, HTTPException, status, Body
from models.user import UserRequest
from service.auth_service import register_service, login_service
from auth.jwt import decode_refresh_token, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register(user_data: UserRequest):
    return await register_service(user_data)

@router.post("/login")
async def login(username: str, password: str):
    return await login_service(username, password)

@router.post("/refresh")
async def refresh_token(refresh_token: str = Body(...)):
    try:
        user_id = decode_refresh_token(refresh_token)
        access_token = create_access_token(data={"sub": str(user_id)})
        return {"access_token": access_token, "token_type": "bearer"}
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
