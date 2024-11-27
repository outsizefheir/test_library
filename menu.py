from rich.console import Console
from rich.table import Table
from controller import Library

class Menu:
    def __init__(self):
        self.console = Console()
        self.library = Library("books.txt")

    def display_menu(self):
        self.console.print("\n[bold yellow]Доступные команды:[/bold yellow]")
        self.console.print(
            "[blue]1. Добавить книгу\n"
            "2. Удалить книгу\n"
            "3. Найти книгу\n"
            "4. Показать все книги\n"
            "5. Изменить статус книги\n"
            "6. Выйти[/blue]"
        )
    
    def run(self):
        while True:
            self.display_menu()
            choice = input("Выберите действие: ").strip()

            match choice:
                case "1":
                    self.add_view()
                case "2":
                    self.remove_view()
                case "3":
                    self.search_view()
                case "4":
                    self.display_view()
                case "5":
                    self.status_view()
                case "6":
                    self.console.print("[green]Выход из программы.[/green]")
                    break
                case _:
                    self.console.print("[red]Неверный выбор, попробуйте снова![/red]")
                    
    def add_view(self):
        try:
            self.console.print("[blue]Пример: 'Война и мир'[/blue]")
            title = input("Введите название книги: ").strip()
            
            self.console.print("[blue]Пример: 'Лев Толстой'[/blue]")
            author = input("Введите автора книги: ").strip()
            
            self.console.print("[blue]Пример: '1869'[/blue]")
            year_input = input("Введите год издания: ").strip()
            
            self.library.add_book(title, author, year_input)
            self.console.print("[green]Книга успешно добавлена![/green]")
        except ValueError as e:
            self.console.print(f"[red]{str(e)}[/red]")
        
    def remove_view(self):
        try:
            book_id = int(input("Введите ID книги для удаления: "))
            self.library.remove_book(book_id)
            self.console.print("[green]Книга успешно удалена![/green]")
        except ValueError:
            self.console.print("[red]Книга с таким ID не найдена.[/red]")        
    
    def search_view(self):
        self.console.print("[blue]Введите поле поиска (название, автор, год): [/blue]")
        field_ru = input().strip().lower()
        field_en = {
            "название": "title",
            "автор": "author",
            "год": "year"
        }.get(field_ru)
        if field_en is None:
            self.console.print("[red]Некорректный ввод поля поиска![/red]")
            return

        self.console.print("[blue]Введите запрос для поиска: [/blue]")
        query = input().strip()

        results = self.library.search_books(query, field_en)
        if results:
            for book in results:
                self.console.print(f"[green]{book}[/green]")
        else:
            self.console.print("[yellow]Книги не найдены.[/yellow]") 
            
    def display_view(self):
        """Отображает все книги в библиотеке в виде таблицы."""
        table = Table(title="Список книг")

        # Добавляем заголовки столбцов
        table.add_column("ID", justify="center", style="cyan", no_wrap=True)
        table.add_column("Название", style="magenta")
        table.add_column("Автор", style="green")
        table.add_column("Год", justify="center", style="yellow")
        table.add_column("Статус", justify="center", style="blue")

        has_books = False
        try:
            for book in self.library.reader.iterate_objects():
                has_books = True
                # Добавляем строки в таблицу
                table.add_row(
                    str(book.id),
                    book.title,
                    book.author,
                    str(book.year),
                    "в наличии" if book.status else "выдана"
                )
            if has_books:
                self.console.print(table)
            else:
                self.console.print("Библиотека пуста.", style="bold red")
        except Exception as e:
            self.console.print(f"Ошибка при чтении данных: {str(e)}", style="bold red")
            
    def status_view(self):       
        try:
            book_id = int(input("Введите ID книги: "))
            new_status = input("Введите статус: 0 - если выдана, 1 - если в наличии): ").strip()
            if new_status not in ("0", "1"):
                raise ValueError("Статус должен быть 0 или 1.")
            self.library.change_status(book_id, bool(int(new_status)))
            self.console.print("[green]Статус книги успешно изменен![/green]")
        except ValueError as e:
            self.console.print(f"[red]{str(e)}[/red]")