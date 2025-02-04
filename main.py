from fastapi import FastAPI, Body

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

@app.get("/", tags=["home"])
def home():
    return {"Hello": "World"}

@app.get("/books", tags=["books"])
def get_books():
    return books_list

@app.get("/books/" , tags=["books"])
def get_books_by_query(category: str):
    for book in books_list:
        if book["category"] == category:
            return book

@app.get("/books/{book_id}", tags=["books"])
def get_book(book_id: int):
    for book in books_list:
        if book["id"] == book_id:
            return book

@app.post("/books", tags=["books"])
def create_book(
    id: int = Body(),
    title: str = Body(), 
    author: str = Body(), 
    year: int = Body(), 
    category: str = Body()
    ):
    new_book = {"id": id, "title": title, "author": author, "year": year, "category": category}
    books_list.append(new_book)
    return new_book

@app.put("/books/{book_id}", tags=["books"])
def update_book(
    book_id: int,
    title: str = Body(), 
    author: str = Body(), 
    year: int = Body(), 
    category: str = Body()
    ):
    for book in books_list:
        if book["id"] == book_id:
            book["title"] = title
            book["author"] = author
            book["year"] = year
            book["category"] = category
            return book

@app.delete("/books/{book_id}", tags=["books"])
def delete_book(book_id: int):
    for book in books_list:
        if book["id"] == book_id:
            books_list.remove(book)
            return {"message": "Book with id {} has been deleted".format(book_id)}