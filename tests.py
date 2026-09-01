import pytest
from main import BooksCollector


class TestBooksCollector:

    # ==================== ТЕСТЫ ДЛЯ МЕТОДА add_new_book ====================
    
    @pytest.mark.parametrize("book_name", [
        "Война и мир",
        "Мастер и Маргарита",
        "Гарри Поттер и философский камень"
    ])
    def test_add_new_book_valid_name(self, book_name):
        """Тест: добавление книг с корректными названиями (до 40 символов)"""
        collector = BooksCollector()
        collector.add_new_book(book_name)
        assert book_name in collector.books_genre
        assert collector.books_genre[book_name] == ""

    def test_add_new_book_duplicate(self):
        """Тест: попытка добавить книгу с уже существующим названием"""
        collector = BooksCollector()
        collector.add_new_book("Дюна")
        collector.add_new_book("Дюна")
        # Проверяем, что книга добавлена только один раз
        assert len(collector.books_genre) == 1

    @pytest.mark.parametrize("invalid_name", [
        "",  # пустая строка
        "a" * 41,  # 41 символ
        "a" * 100  # много символов
    ])
    def test_add_new_book_invalid_name(self, invalid_name):
        """Тест: добавление книг с некорректными названиями"""
        collector = BooksCollector()
        collector.add_new_book(invalid_name)
        assert invalid_name not in collector.books_genre

    # ==================== ТЕСТЫ ДЛЯ МЕТОДА set_book_genre ====================

    @pytest.mark.parametrize("book_name, genre", [
        ("1984", "Фантастика"),
        ("Оно", "Ужасы"),
        ("Убийство в Восточном экспрессе", "Детективы"),
        ("Шрек", "Мультфильмы"),
        ("Бриллиантовая рука", "Комедии")
    ])
    def test_set_book_genre_valid(self, book_name, genre):
        """Тест: установка жанра для существующей книги"""
        collector = BooksCollector()
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        assert collector.get_book_genre(book_name) == genre

    def test_set_book_genre_for_nonexistent_book(self):
        """Тест: попытка установить жанр для несуществующей книги"""
        collector = BooksCollector()
        collector.set_book_genre("Несуществующая книга", "Фантастика")
        assert "Несуществующая книга" not in collector.books_genre

    @pytest.mark.parametrize("invalid_genre", [
        "Роман",
        "Поэзия", 
        "Приключения",
        "Сказки"
    ])
    def test_set_book_genre_invalid_genre(self, invalid_genre):
        """Тест: установка невалидного жанра"""
        collector = BooksCollector()
        collector.add_new_book("Тестовая книга")
        collector.set_book_genre("Тестовая книга", invalid_genre)
        assert collector.get_book_genre("Тестовая книга") == ""

    # ==================== ТЕСТЫ ДЛЯ МЕТОДА get_book_genre ====================

    def test_get_book_genre_existing_book(self):
        """Тест: получение жанра существующей книги"""
        collector = BooksCollector()
        collector.add_new_book("Гарри Поттер")
        collector.set_book_genre("Гарри Поттер", "Фантастика")
        assert collector.get_book_genre("Гарри Поттер") == "Фантастика"

    def test_get_book_genre_nonexistent_book(self):
        """Тест: получение жанра несуществующей книги"""
        collector = BooksCollector()
        assert collector.get_book_genre("Несуществующая книга") is None

    def test_get_book_genre_book_without_genre(self):
        """Тест: получение жанра книги без установленного жанра"""
        collector = BooksCollector()
        collector.add_new_book("Книга без жанра")
        assert collector.get_book_genre("Книга без жанра") == ""

    # ==================== ТЕСТЫ ДЛЯ МЕТОДА get_books_with_specific_genre ====================

    @pytest.mark.parametrize("genre, expected_books", [
        ("Фантастика", ["Дюна", "1984"]),
        ("Ужасы", ["Оно"]),
        ("Детективы", []),
        ("Мультфильмы", ["Шрек"])
    ])
    def test_get_books_with_specific_genre(self, genre, expected_books):
        """Тест: получение списка книг по конкретному жанру"""
        collector = BooksCollector()
        # Добавляем книги
        collector.add_new_book("Дюна")
        collector.set_book_genre("Дюна", "Фантастика")
        collector.add_new_book("1984")
        collector.set_book_genre("1984", "Фантастика")
        collector.add_new_book("Оно")
        collector.set_book_genre("Оно", "Ужасы")
        collector.add_new_book("Шрек")
        collector.set_book_genre("Шрек", "Мультфильмы")
        
        assert collector.get_books_with_specific_genre(genre) == expected_books

    def test_get_books_with_specific_genre_empty_dict(self):
        """Тест: получение книг по жанру из пустого словаря"""
        collector = BooksCollector()
        assert collector.get_books_with_specific_genre("Фантастика") == []

    # ==================== ТЕСТЫ ДЛЯ МЕТОДА get_books_genre ====================

    def test_get_books_genre_empty(self):
        """Тест: получение пустого словаря книг"""
        collector = BooksCollector()
        assert collector.get_books_genre() == {}

    def test_get_books_genre_with_books(self):
        """Тест: получение словаря с книгами и жанрами"""
        collector = BooksCollector()
        collector.add_new_book("Книга 1")
        collector.set_book_genre("Книга 1", "Фантастика")
        collector.add_new_book("Книга 2")
        collector.set_book_genre("Книга 2", "Комедии")
        
        expected = {"Книга 1": "Фантастика", "Книга 2": "Комедии"}
        assert collector.get_books_genre() == expected

    # ==================== ТЕСТЫ ДЛЯ МЕТОДА get_books_for_children ====================

    @pytest.mark.parametrize("books_data", [
        {
            "books": [
                ("Книга 1", "Фантастика"),
                ("Книга 2", "Мультфильмы"),
                ("Книга 3", "Комедии")
            ],
            "expected": ["Книга 1", "Книга 2", "Книга 3"]
        },
        {
            "books": [
                ("Книга 1", "Ужасы"),
                ("Книга 2", "Детективы")
            ],
            "expected": []
        },
        {
            "books": [
                ("Книга 1", "Фантастика"),
                ("Книга 2", "Ужасы"),
                ("Книга 3", "Мультфильмы"),
                ("Книга 4", "Детективы"),
                ("Книга 5", "Комедии")
            ],
            "expected": ["Книга 1", "Книга 3", "Книга 5"]
        }
    ])
    def test_get_books_for_children(self, books_data):
        """Тест: получение списка книг для детей (без возрастного рейтинга)"""
        collector = BooksCollector()
        for book_name, genre in books_data["books"]:
            collector.add_new_book(book_name)
            collector.set_book_genre(book_name, genre)
        
        assert collector.get_books_for_children() == books_data["expected"]

    def test_get_books_for_children_book_without_genre(self):
        """Тест: книга без жанра не попадает в список для детей"""
        collector = BooksCollector()
        collector.add_new_book("Книга без жанра")
        # Книга без жанра не должна попадать в список для детей
        assert collector.get_books_for_children() == []

    # ==================== ТЕСТЫ ДЛЯ МЕТОДА add_book_in_favorites ====================

    @pytest.mark.parametrize("book_name", [
        "Гарри Поттер",
        "Властелин колец",
        "Хоббит"
    ])
    def test_add_book_in_favorites_valid(self, book_name):
        """Тест: добавление существующей книги в избранное"""
        collector = BooksCollector()
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, "Фантастика")
        collector.add_book_in_favorites(book_name)
        assert book_name in collector.favorites
        assert len(collector.favorites) == 1

    def test_add_book_in_favorites_duplicate(self):
        """Тест: повторное добавление книги в избранное"""
        collector = BooksCollector()
        collector.add_new_book("Дюна")
        collector.set_book_genre("Дюна", "Фантастика")
        collector.add_book_in_favorites("Дюна")
        collector.add_book_in_favorites("Дюна")
        # Проверяем, что книга добавлена только один раз
        assert collector.favorites.count("Дюна") == 1

    def test_add_book_in_favorites_nonexistent_book(self):
        """Тест: добавление несуществующей книги в избранное"""
        collector = BooksCollector()
        collector.add_book_in_favorites("Несуществующая книга")
        assert "Несуществующая книга" not in collector.favorites

    def test_add_book_in_favorites_book_not_in_books_genre(self):
        """Тест: добавление книги в избранное, если её нет в словаре books_genre"""
        collector = BooksCollector()
        # Не добавляем книгу через add_new_book
        collector.add_book_in_favorites("Книга из ниоткуда")
        assert "Книга из ниоткуда" not in collector.favorites

    # ==================== ТЕСТЫ ДЛЯ МЕТОДА delete_book_from_favorites ====================

    def test_delete_book_from_favorites_valid(self):
        """Тест: удаление книги из избранного"""
        collector = BooksCollector()
        collector.add_new_book("Книга для удаления")
        collector.set_book_genre("Книга для удаления", "Комедии")
        collector.add_book_in_favorites("Книга для удаления")
        assert "Книга для удаления" in collector.favorites
        
        collector.delete_book_from_favorites("Книга для удаления")
        assert "Книга для удаления" not in collector.favorites

    def test_delete_book_from_favorites_not_in_favorites(self):
        """Тест: удаление книги, которой нет в избранном"""
        collector = BooksCollector()
        collector.add_new_book("Книга")
        collector.set_book_genre("Книга", "Фантастика")
        # Не добавляем в избранное
        collector.delete_book_from_favorites("Книга")
        assert "Книга" not in collector.favorites

    def test_delete_book_from_favorites_nonexistent_book(self):
        """Тест: удаление несуществующей книги из избранного"""
        collector = BooksCollector()
        collector.delete_book_from_favorites("Несуществующая книга")
        # Ошибки быть не должно, избранное остаётся пустым
        assert collector.favorites == []

    # ==================== ТЕСТЫ ДЛЯ МЕТОДА get_list_of_favorites_books ====================

    def test_get_list_of_favorites_books_empty(self):
        """Тест: получение списка избранных книг, когда избранное пустое"""
        collector = BooksCollector()
        assert collector.get_list_of_favorites_books() == []

    def test_get_list_of_favorites_books_with_books(self):
        """Тест: получение списка избранных книг с книгами"""
        collector = BooksCollector()
        books = ["Книга 1", "Книга 2", "Книга 3"]
        
        for book in books:
            collector.add_new_book(book)
            collector.set_book_genre(book, "Фантастика")
            collector.add_book_in_favorites(book)
        
        assert collector.get_list_of_favorites_books() == books

    # ==================== КОМБИНИРОВАННЫЕ ТЕСТЫ ====================

    def test_full_workflow(self):
        """Тест: полный сценарий работы с коллекцией книг"""
        collector = BooksCollector()
        
        # Шаг 1: Добавляем книги
        collector.add_new_book("Война и мир")
        collector.add_new_book("Мертвые души")
        collector.add_new_book("Преступление и наказание")
        
        # Шаг 2: Устанавливаем жанры
        collector.set_book_genre("Война и мир", "Комедии")
        collector.set_book_genre("Мертвые души", "Комедии")
        collector.set_book_genre("Преступление и наказание", "Детективы")
        
        # Шаг 3: Проверяем книги для детей (Детективы не подходят)
        children_books = collector.get_books_for_children()
        assert "Война и мир" in children_books
        assert "Мертвые души" in children_books
        assert "Преступление и наказание" not in children_books
        
        # Шаг 4: Добавляем в избранное
        collector.add_book_in_favorites("Война и мир")
        collector.add_book_in_favorites("Мертвые души")
        
        # Шаг 5: Проверяем избранное
        favorites = collector.get_list_of_favorites_books()
        assert len(favorites) == 2
        assert "Война и мир" in favorites
        assert "Мертвые души" in favorites
        assert "Преступление и наказание" not in favorites
        
        # Шаг 6: Удаляем из избранного
        collector.delete_book_from_favorites("Война и мир")
        favorites_after_delete = collector.get_list_of_favorites_books()
        assert len(favorites_after_delete) == 1
        assert "Война и мир" not in favorites_after_delete
        assert "Мертвые души" in favorites_after_delete

    def test_get_books_with_specific_genre_and_favorites_interaction(self):
        """Тест: взаимодействие методов get_books_with_specific_genre и favorites"""
        collector = BooksCollector()
        
        # Добавляем книги разных жанров
        collector.add_new_book("Звездные войны")
        collector.set_book_genre("Звездные войны", "Фантастика")
        
        collector.add_new_book("Мстители")
        collector.set_book_genre("Мстители", "Фантастика")
        
        collector.add_new_book("Титаник")
        collector.set_book_genre("Титаник", "Детективы")
        
        # Получаем книги жанра "Фантастика"
        fantasy_books = collector.get_books_with_specific_genre("Фантастика")
        assert len(fantasy_books) == 2
        
        # Добавляем одну из них в избранное
        collector.add_book_in_favorites("Звездные войны")
        
        # Проверяем, что избранное не влияет на основной словарь
        assert collector.get_books_with_specific_genre("Фантастика") == ["Звездные войны", "Мстители"]
        assert "Звездные войны" in collector.favorites