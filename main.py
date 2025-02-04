from fastapi import FastAPI, Body

from pydantic import BaseModel, Field

from typing import Optional, List

app = FastAPI(title="Mi primera API", description="Api de prueba para aprender FastAPI", version="1.0")

books_list = [
    {"id": 1, "title": "The Midnight Library", "author": "Matt Haig", "year": 2020, "category": "Fiction"},
    {"id": 2, "title": "The Vanishing Half", "author": "Brit Bennett", "year": 2020, "category": "Fiction"},
    {"id": 3, "title": "Where the Crawdads Sing", "author": "Delia Owens", "year": 2018, "category": "Mystery"},
    {"id": 4, "title": "The Invisible Life of Addie LaRue", "author": "V.E. Schwab", "year": 2020, "category": "Fantasy"},
    {"id": 5, "title": "The Four Winds", "author": "Kristin Hannah", "year": 2021, "category": "Historical Fiction"},
    {"id": 6, "title": "The Silent Patient", "author": "Alex Michaelides", "year": 2019, "category": "Thriller"},
    {"id": 7, "title": "The Guest List", "author": "Lucy Foley", "year": 2020, "category": "Mystery"},
    {"id": 8, "title": "The Last Thing He Told Me", "author": "Laura Dave", "year": 2021, "category": "Thriller"},
    {"id": 9, "title": "The Night Watchman", "author": "Louise Erdrich", "year": 2020, "category": "Historical Fiction"},
    {"id": 10, "title": "Anxious People", "author": "Fredrik Backman", "year": 2020, "category": "Fiction"}
]

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

class BookUpdate(BaseModel):
    title: str
    author: str
    year: int
    category: str

@app.get("/", tags=["home"])
def home():
    return {"Hello": "World"}

@app.get("/books", tags=["books"])
def get_books() -> List[Book]: # El tipo de retorno es una lista de tipo Book
    return books_list

@app.get("/books/" , tags=["books"])
def get_books_by_query(category: str):
    for book in books_list:
        if book["category"] == category:
            return book

@app.get("/books/{book_id}", tags=["books"])
def get_book(book_id: int) -> Book: # El tipo de retorno es un objeto de tipo Book
    for book in books_list:
        if book["id"] == book_id:
            return book

@app.post("/books", tags=["books"])
def create_book(book: BookCreate) -> Book:
    new_book = book.model_dump() # Convertir el objeto Pydantic a un diccionario
    books_list.append(new_book)
    return new_book

@app.put("/books/{book_id}", tags=["books"])
def update_book(book_id: int, book: BookUpdate) -> Book:
    for item in books_list:
        if item["id"] == book_id:
            item["title"] = book.title
            item["author"] = book.author
            item["year"] = book.year
            item["category"] = book.category
            return item

@app.delete("/books/{book_id}", tags=["books"])
def delete_book(book_id: int):
    for book in books_list:
        if book["id"] == book_id:
            books_list.remove(book)
            return {"message": "Book with id {} has been deleted".format(book_id)}