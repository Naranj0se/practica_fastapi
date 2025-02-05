from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import PlainTextResponse, RedirectResponse, FileResponse

from pydantic import BaseModel, Field

from typing import Optional, List

app = FastAPI(title="Mi primera API", description="Api de prueba para aprender FastAPI", version="1.0")


# Definir el modelo de datos
class Book(BaseModel):
    id: int # El id es opcional al crear un libro
    title: str
    author: str
    year: int
    category: str

class BookCreate(BaseModel):
    id: int = Field(..., gt=0, description="The id of the book")
    title: str = Field(..., min_length=1, max_length=100, description="The title of the book")
    author: str = Field(..., min_length=1, max_length=100, description="The author of the book")
    year: int = Field(..., gt=0, description="The year of the book")
    category: str = Field(..., min_length=1, max_length=100, description="The category of the book")

    model_config = {
        'json_schema_extra': {
            "example": {
                "id": 11,
                "title": "The Midnight Library",
                "author": "Matt Haig",
                "year": 2020,
                "category": "Fiction"
            }
        }
    }

class BookUpdate(BaseModel):
    title: str
    author: str
    year: int
    category: str

books_list: List[Book]  = []

@app.get("/", tags=["home"])
def home():
    return PlainTextResponse(content="Welcome to my API")

@app.get("/books", tags=["books"])
def get_books() -> List[Book]: # El tipo de retorno es una lista de tipo Book
    return [book.model_dump() for book in books_list]

@app.get("/books/" , tags=["books"])
def get_books_by_query(category: str = Query(min_length=1, max_length=100)) -> Book | dict:
    for book in books_list:
        if book.category == category:
            return book.model_dump()

@app.get("/books/{book_id}", tags=["books"])
def get_book(book_id: int = Path(gt=0)) -> Book | dict: # El tipo de retorno es un objeto de tipo Book
    for book in books_list:
        if book.id == book_id:
            return book.model_dump()
    return {}

@app.post("/books", tags=["books"])
def create_book(book: BookCreate) -> Book:
    # new_book = book.model_dump() # Convertir el objeto Pydantic a un diccionario
    books_list.append(book)
    return book.model_dump()
    # return RedirectResponse(url="/books", status_code=303) # Redireccionar a la lista de libros

@app.put("/books/{book_id}", tags=["books"])
def update_book(book_id: int, book: BookUpdate) -> Book | dict:
    for item in books_list:
        if item.id == book_id:
            item.title = book.title
            item.author = book.author
            item.year = book.year
            item.category = book.category
            return item
    return {}

@app.delete("/books/{book_id}", tags=["books"])
def delete_book(book_id: int) -> dict:
    for book in books_list:
        if book.id == book_id:
            books_list.remove(book)
            return {"message": "Book with id {} has been deleted".format(book_id)}
    return {"message": "Book with id {} not found".format(book_id)}

@app.get("/download", tags=["download"])
def download_file():
    return FileResponse("textoPrueba.txt")