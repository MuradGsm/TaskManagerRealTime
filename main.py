from fastapi import FastAPI
from api.admin import router as admin
from api.auth import router as auth

app = FastAPI()

app.include_router(auth)
app.include_router(admin)


