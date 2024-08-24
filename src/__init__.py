from fastapi import FastAPI
from src.auth.routes import auth_router


app = FastAPI(title='My API', description='Belajar Membuat API dengan Fastapi')
app.include_router(auth_router, prefix='/api/v1/auth', tags=['auth'])
