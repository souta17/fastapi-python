from fastapi import FastAPI
from src.auth.routes import auth_router

VERSION = 1
frepix_api = '/api/v1'

app = FastAPI(
    title='My API',
    version=VERSION,
    description='Belajar Membuat API dengan Fastapi'
)
app.include_router(auth_router, prefix=f'{frepix_api}/auth', tags=['auth'])
