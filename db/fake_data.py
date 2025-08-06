from models.user import UserResponse
from auth.hash import hash_password
from datetime import datetime

users_db = [
    UserResponse(
        id=1,
        username="admin",
        email="admin@example.com",
        full_name="Super Admin",
        hashed_password=hash_password("admin123"),  
        is_active=True,
        is_admin=True,
        status="online",
        avatar_url="https://example.com/avatar/admin.png",
        created_at=datetime.now(),
        last_seen=datetime.now()
    )
]
