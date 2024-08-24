from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
import uuid


class UserModel(BaseModel):
   uuid: uuid.UUID
   username: str
   email: str
   first_name: str
   last_name: str
   is_verified: bool
   password_hash: str = Field(exclude=True)
   created_at: datetime
   updated_at: datetime


class UserCreateModel(BaseModel):
   first_name: str = Field(max_length=30)
   last_name: str = Field(max_length=30)
   username: str = Field(max_length=20)
   email: str = Field(max_length=50)
   password: str = Field(min_length=6)


class UserLoginModel(BaseModel):
   email: str
   password: str
