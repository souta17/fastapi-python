from passlib.context import CryptContext
from datetime import datetime, timedelta
from src.config import Config
import jwt
import uuid
import logging

pass_ctx = CryptContext(schemes=['bcrypt'])
ACCESS_TOKEN_EXPIRY = 3600


def generate_hash_pass(password: str) -> str:
   hash = pass_ctx.hash(password)
   return hash


def verify_pass(password: str, hash: str) -> bool:
   return pass_ctx.verify(password, hash)


def generate_token(
    user_data: dict,
    expiry: timedelta = None,
    refresh: bool = False
):
   payload = {}
   payload['user'] = user_data
   payload['exp'] = datetime.now(
   ) + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))

   payload['jti'] = str(uuid.uuid4())
   payload['refresh'] = refresh

   token = jwt.encode(
       payload=payload,
       key=Config.SECRET_KEY,
       algorithm=Config.JWT_ALGORITHM)
   return token


def decode_token(token: str):
   try:
      token_data = jwt.decode(
          jwt=token,
          key=Config.SECRET_KEY,
          algorithms=[Config.JWT_ALGORITHM]
      )
      return token_data

   except jwt.PyJWTError as e:
      logging.exception(e)
      return None
