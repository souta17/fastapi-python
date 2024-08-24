from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.models import User
from .shcemas import UserCreateModel
from .utils import generate_hash_pass


class UserService:
   async def get_user_by_email(self, email: str, session: AsyncSession):
      statment = select(User).where(User.email == email)
      result = await session.exec(statment)
      user = result.first()
      return user

   async def user_exist(self, email: str, session: AsyncSession):
      user = await self.get_user_by_email(email, session)
      return True if user is not None else False

   async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
      user_data_dict = user_data.model_dump()
      new_user = User(
          **user_data_dict
      )
      new_user.password_hash = generate_hash_pass(user_data_dict['password'])
      session.add(new_user)
      await session.commit()
      return new_user
