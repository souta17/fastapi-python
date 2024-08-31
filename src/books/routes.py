from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .service import BookService
from .schemas import Book, BookCreateModel
from src.auth.dependencies import AccessTokenBearer


access_token_bearer = AccessTokenBearer()


book_router = APIRouter()
book_service = BookService()


@book_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Book)
async def create_book(
        book_data: BookCreateModel,
        session: AsyncSession = Depends(get_session),
        token_detail: dict = Depends(access_token_bearer)):

   user_uid = token_detail.get("user")["user_uid"]
   new_book = await book_service.create_book(book_data, user_uid, session)

   return new_book


@book_router.get("/")
async def get_all_books(
        session: AsyncSession = Depends(get_session)
):
   books = await book_service.get_all_books(session)

   return books
