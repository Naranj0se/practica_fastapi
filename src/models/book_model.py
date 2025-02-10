from pydantic import BaseModel, Field, validator

class Book(BaseModel):
    id: int # El id es opcional al crear un libro
    title: str
    author: str
    year: int
    category: str

class BookCreate(BaseModel):
    id: int = Field(..., gt=0, description="The id of the book")
    title: str
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

    # Validacion personalizada

    @validator("title")
    def validate_title(cls, value):
        if len(value) < 5:
            raise ValueError("Title must be at least 5 characters, Idiot!")

        if len(value) > 50:
            raise ValueError("Title must be less than 15 characters, Idiot!")

        return value

class BookUpdate(BaseModel):
    title: str
    author: str
    year: int
    category: str