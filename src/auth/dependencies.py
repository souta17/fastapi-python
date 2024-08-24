from fastapi import Request, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException
from .utils import decode_token


class TokenBaerer(HTTPBearer):
   def __init__(self, auto_error=True):
      super().__init__(auto_error)

   async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
      creds = await super().__call__(request)
      token_data = creds.credentials
      if not self.token_valid:
         raise HTTPException(
             status_code=status.HTTP_403_FORBIDDEN,
             detail='Invalid or expired tokrn')

      if token_data['refresh']:
         raise HTTPException(
             status_code=status.HTTP_403_FORBIDDEN,
             detail='Please provide an access token')
      self.verify_token_data(token_data)

      return token_data

   def token_valid(self, token: str) -> bool:
      token_data = decode_token(token)
      return True if token_data is not None else False

   def verify_token_data(self, token_data):
      raise NotImplementedError("Please override this method in child classes")


class AccessTokenBearer(TokenBaerer):
   def verify_token_data(self, token_data: dict) -> None:
      if token_data and token_data['refresh']:
         raise HTTPException(
             status_code=status.HTTP_403_FORBIDDEN,
             detail='Please provide an access token')


class RefreshTokenBearer(TokenBaerer):
   def verify_token_data(self, token_data: dict) -> None:
      if token_data and token_data['refresh']:
         raise HTTPException(
             status_code=status.HTTP_403_FORBIDDEN,
             detail='Please provide an refresh token')
