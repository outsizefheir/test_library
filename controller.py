import json
import os
from pydantic import ValidationError
from model import Book
from reader import Reader

class Library:
    def __init__(self, storage_path: str):
        self.storage_path = storage_path
        self.reader = Reader(storage_path)
        self._check_storage()

    def _check_storage(self) -> None:
        """
        Проверяет наличие файла хранилища и создает его, если он отсутствует.
        
        :param: Экземпляр класса, в котором находится путь к файлу хранилища.
        :return: Функция не возвращает значения, а просто проверяет и при необходимости создает файл хранилища.
        """
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                pass

    def _get_last_id(self) -> int:
        """
        Возвращает последний ID книги в библиотеке.
        
        :param: Экземпляр класса, для обращения к интерфейсу reader и его методу iterate_objects.
        :return: Возвращает последний ID книги (int). Если книг в хранилище нет, возвращает 0.
        """
        last_id = 0
        for book in self.reader.iterate_objects():
            if book.id > last_id:
                last_id = book.id
        return last_id

    def _validate_book(self, id: int, title: str, author: str, year: str) -> Book:
        """Валидация книги. Возвращает объект Book, если валидация успешна.
                
        :param id: ID книги для валидации.
        :param title: Название книги для валидации.
        :param author: Автор книги для валидации.
        :param year: Год издания книги для валидации.
        :return: Возвращает объект Book, если данные прошли валидацию.
        :raises ValueError: Если данные книги не соответствуют правилам валидации.
        """
        try:
            return Book(
                id=id,
                title=title,
                author=author,
                year=year
            )
        except ValidationError as e:
            errors = [err['msg'] for err in e.errors()]
            raise ValueError("\n".join(errors))

    def write_to_file(self, book: Book, file_path: str) -> None:
        """Записывает книгу в файл в формате JSON.
        
        :param book: Объект книги, который необходимо записать.
        :param file_path: Путь к файлу, в который будет записана книга.
        :return: Функция записывает данные в файл.
        :raises IOError: Если возникла ошибка записи в файл.
        """
        try:
            with open(file_path, 'a', encoding='utf-8') as file:
                json_str = json.dumps(book.model_dump(), ensure_ascii=False)
                file.write(json_str + '\n')
        except OSError as e:
            raise IOError(f'Ошибка записи в файл: {e}')
            
    

    def add_book(self, title: str, author: str, year: str) -> None:
        """Добавляет новую книгу в библиотеку.
        
        :param title: Название книги.
        :param author: Автор книги.
        :param year: Год издания книги.
        :raises ValueError: Если данные книги не прошли валидацию.
        :raises IOError: Если произошла ошибка записи книги в хранилище.
        """
        next_id = self._get_last_id() + 1
        try:
            book = self._validate_book(next_id, title, author, year)
        except ValueError as e:
            raise ValueError(f"Ошибка валидации данных книги: {e}")

        try:
            with open(self.storage_path, 'a', encoding='utf-8') as file:
                self.write_to_file(book, self.storage_path)
        except IOError as e:
            raise IOError(f"Не удалось добавить книгу в хранилище: {e}")

    def remove_book(self, book_id: int) -> None:
        """Удаляет книгу из библиотеки по ID.
        
        :param book_id: ID книги, которую нужно удалить.
        :return: Книга удаляется из хранилища.
        :raises ValueError: Если книга с указанным ID не найдена.
        :raises IOError: Если произошла ошибка записи.
        """
        found = False
        temp_storage = self.storage_path + '.tmp'
        current_id = 1

        try:
            with open(temp_storage, 'w', encoding='utf-8') as temp_file:
                for book in self.reader.iterate_objects():
                    if book.id == book_id:
                        found = True
                        continue
                    
                    book.id = current_id
                    self.write_to_file(book, temp_storage)
                    current_id += 1

            if not found:
                os.remove(temp_storage)
                raise ValueError
            
            os.replace(temp_storage, self.storage_path)
        
        except IOError as e:  
            if os.path.exists(temp_storage):
                os.remove(temp_storage)
            raise IOError(f"Ошибка записи: {e}")


    def search_books(self, query: str, field: str) -> list[Book]:
        """Ищет книги по заданному полю и запросу.

        :param query: Строка, содержащая запрос для поиска. я.
        :param field: Поле, по которому производится поиск. 
        :return: List объектов Book, соответствующих критериям поиска.
        :raises ValueError: Если указано недопустимое поле для поиска.
        """
        query = query.lower()
        field = field.lower()

        search_functions = {
            "title": lambda book: query in book.title.lower(),
            "author": lambda book: query in book.author.lower(),
            "year": lambda book: query == str(book.year)
        }

        results = [book for book in self.reader.iterate_objects() if search_functions[field](book)]
        return results

    def change_status(self, book_id: int, new_status: bool) -> None:
        """Изменяет статус книги по ID.
        
        :param book_id: ID книги, для которой нужно изменить статус.
        :param new_status: Новый статус книги (True - в наличии, False - выдана).
        :return: Функция изменяет статус книги.
        :raises ValueError: Если книга с таким ID не найдена в хранилище.
        :raises ValidationError: Если данные книги не прошли валидацию при изменении статуса.
        :raises OSError: Если произошла ошибка при работе с файлами.
        """
        found = False
        temp_storage = self.storage_path + '.tmp'

        with open(temp_storage, 'w', encoding='utf-8') as temp_file:
            for book in self.reader.iterate_objects():
                if book.id == book_id:
                    try:
                        self._validate_book(book.id, book.title, book.author, str(book.year ))
                        book.status = new_status
                        found = True
                    except ValueError as e:
                        raise ValueError(f"Ошибка валидации книги: {str(e)}")
                
                self.write_to_file(book, temp_storage)

        if not found:
            os.remove(temp_storage)
            raise ValueError("Книга с таким ID не найдена.")

        os.replace(temp_storage, self.storage_path)
        
        
        