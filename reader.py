from collections.abc import Generator
import json
from model import Book

class Reader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def iterate_objects(self) -> Generator[Book, None, None]:
        """
        Генератор для итерации по объектам Book, сохраненным в файле.

        :return: Генератор объектов Book.
        :raises IOError: Если файл не удается открыть для чтения.
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    book = self.read_object(line)
                    yield book
        except IOError as e:
            raise IOError(f'Ошибка итерации: {e}')

    def read_object(self, json_str: str) -> Book:
        """
        Преобразует строку JSON в объект Book.

        :param json_str: Строка в формате JSON.
        :return: Объект Book.
        :raises ValueError: Если строка не соответствует формату JSON 
        """
        try:
            data = json.loads(json_str)
            return Book(**data)
        except json.JSONDecodeError:
            raise ValueError("Неверный формат JSON")





