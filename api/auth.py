from fastapi import APIRouter, HTTPException, status, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm
from models.user import UserRequest, UserResponse
from service.auth_service import register_service, login_service
from auth.jwt import decode_refresh_token, create_access_token
from auth.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register(user_data: UserRequest):
    return await register_service(user_data)

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return await login_service(form_data.username, form_data.password)

@router.post("/refresh")
async def refresh_token(refresh_token: str = Body(...)):
    try:
        user_id = decode_refresh_token(refresh_token)
        access_token = create_access_token(data={"sub": str(user_id)})
        return {"access_token": access_token, "token_type": "bearer"}
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")


@router.get("/me")
async def get_me(current_user: UserResponse = Depends(get_current_user)):
    return {"email": current_user.email, "id": current_user.id}


