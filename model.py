from pydantic import BaseModel, Field
from datetime import datetime

current_year = datetime.now().year

class Book(BaseModel):
    """
    Модель книги для библиотеки, содержащая основные атрибуты и их валидацию.

    Атрибуты:
        id (int): Уникальный идентификатор книги. Должен быть больше 0.
        title (str): Название книги. От 1 до 150 символов, пробелы удаляются.
        author (str): Автор книги. От 1 до 250 символов, пробелы удаляются.
        year (int): Год издания книги. Должен быть меньше или равен текущему году.
        status (bool): Статус книги, True — в наличии, False — выдана.
    """

    id: int = Field(
        ..., 
        description="ID книги", 
        gt=0
    )
    title: str = Field(
        ..., 
        description="Название книги",
        min_length=1,
        max_length=150,
        strip_whitespace=True
    )
    author: str = Field(
        ..., 
        description="Автор книги",
        min_length=1,
        max_length=250,
        strip_whitespace=True
    )
    year: int = Field(
        ..., 
        description="Год издания книги",
        le=current_year
    )
    status: bool = Field(
        default=True, 
        description="Статус: True - в наличии, False - выдана"
    )

    model_config = {
        "str_strip_whitespace": True,
        "validate_assignment": True
    }



    