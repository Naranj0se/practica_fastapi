from fastapi import Path, Query, APIRouter
from fastapi.responses import FileResponse, JSONResponse
from typing import List
from src.models.book_model import Book, BookCreate, BookUpdate

books_list: List[Book]  = []

book_router = APIRouter()

@book_router.get("/", tags=["books"], status_code=200, response_description="List of books")
def get_books() -> List[Book]:
    content = [book.model_dump() for book in books_list]
    return JSONResponse(content=content, status_code=200)

@book_router.get("/by_category" , tags=["books"])
def get_books_by_query(category: str = Query(min_length=1, max_length=100)) -> Book | dict:
    for book in books_list:
        if book.category == category:
            return JSONResponse(content=book.model_dump(), status_code=200)
    return JSONResponse(content={"error": "Book not found"}, status_code=404)

@book_router.get("/{book_id}", tags=["books"])
def get_book(book_id: int = Path(gt=0)) -> Book | dict:
    for book in books_list:
        if book.id == book_id:
            return JSONResponse(content=book.model_dump(), status_code=200)
    return JSONResponse(content={"error": "Book not found"}, status_code=404)

@book_router.post("", tags=["books"])
def create_book(book: BookCreate) -> Book:
    books_list.append(book)
    return JSONResponse(content=book.model_dump(), status_code=201)

@book_router.put("/{book_id}", tags=["books"])
def update_book(book_id: int, book: BookUpdate) -> Book | dict:
    for item in books_list:
        if item.id == book_id:
            item.title = book.title
            item.author = book.author
            item.year = book.year
            item.category = book.category
            return JSONResponse(content=item.model_dump(), status_code=200)
    return JSONResponse(content={"error": "Book not found"}, status_code=404)

@book_router.delete("/{book_id}", tags=["books"])
def delete_book(book_id: int) -> dict:
    for book in books_list:
        if book.id == book_id:
            books_list.remove(book)
            return JSONResponse(content={"message": f"Book with id {book_id} has been deleted"}, status_code=200)
    return JSONResponse(content={"error": f"Book with id {book_id} not found"}, status_code=404)