from fastapi import APIRouter, Depends
from auth.deps import admin_required

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users")
async def list_users(current_admin = Depends(admin_required)):
    from db.fake_data import users_db
    return users_db
