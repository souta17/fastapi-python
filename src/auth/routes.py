from fastapi import APIRouter, Depends, status
from .shcemas import UserCreateModel, UserModel, UserLoginModel
from fastapi.responses import JSONResponse
from .service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from .utils import generate_token, decode_token, verify_pass
from datetime import timedelta


REFRES_TOKEN = 2

auth_router = APIRouter()
user_service = UserService()


@auth_router.post('/signup',
                  response_model=UserModel,
                  status_code=status.HTTP_201_CREATED)
async def create_user(
        user_data: UserCreateModel,
        session: AsyncSession = Depends(get_session)):
    email = user_data.email
    user_exist = await user_service.user_exist(email, session)

    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='User already exist')
    new_user = await user_service.create_user(user_data, session)

    return new_user


@auth_router.post('/login')
async def login(
        login_request: UserLoginModel,
        session: AsyncSession = Depends(get_session)):
   email = login_request.email
   password = login_request.password

   user = await user_service.get_user_by_email(email, session)

   if user is not None:
      password_valid = verify_pass(password, user.password_hash)

      if password_valid:
         access_token = generate_token(
             user_data={
                 'email': user.email,
                 'user_uid': str(user.uid)
             }
         )

         refresh_token = generate_token(
             user_data={
                 'email': user.email,
                 'user_uid': str(user.uid)
             },
             refresh=True,
             expiry=timedelta(days=REFRES_TOKEN)
         )

         return JSONResponse(
             content={
                 'message': 'Login successfuly',
                 'access_toke': access_token,
                 'refresh_toke': refresh_token,
                 'user': {
                     'email': user.email,
                     'uid': str(user.uid)
                 }
             }
         )
   raise HTTPException(
       status_code=status.HTTP_403_FORBIDDEN,
       detail='Invalid email or password'
   )
