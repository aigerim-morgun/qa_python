import pytest
from main import BooksCollector


class TestBooksCollector:

    def test_add_new_book_add_two_books(self):
        collector = BooksCollector()

        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        assert len(collector.get_books_genre()) == 2

    @pytest.mark.parametrize(
        'book_name, expected_count',
        [
            ['', 0],                    # 0
            ['Я', 1],                   # 1
            ['Мастер и Маргарита', 1],  # 16
            ['Я' * 40, 1],              # 40
            ['Я' * 41, 0]               # 41
        ]
    )
    def test_add_new_book_name_length(self, book_name, expected_count):
        collector = BooksCollector()

        collector.add_new_book(book_name)

        assert len(collector.get_books_genre()) == expected_count

    def test_add_new_book_not_add_duplicate(self):
        collector = BooksCollector()

        collector.add_new_book('Дюна')
        collector.add_new_book('Дюна')

        assert len(collector.get_books_genre()) == 1

    def test_add_new_book_without_genre(self):
        collector = BooksCollector()

        collector.add_new_book('Дюна')

        assert collector.get_book_genre('Дюна') == ''

    def test_set_book_genre_successfully_sets_valid_genre(self):
        collector = BooksCollector()

        collector.add_new_book('Дюна')
        collector.set_book_genre('Дюна', 'Фантастика')

        assert collector.get_book_genre('Дюна') == 'Фантастика'

    def test_set_book_genre_not_set_if_genre_not_in_list(self):
        collector = BooksCollector()

        collector.add_new_book('Дюна')
        collector.set_book_genre('Дюна', 'Роман')

        assert collector.get_book_genre('Дюна') == ''

    def test_set_book_genre_not_set_if_book_not_exists(self):
        collector = BooksCollector()

        collector.set_book_genre('Дюна', 'Фантастика')

        assert collector.get_book_genre('Дюна') is None

    @pytest.mark.parametrize(
        'genre, book_name',
        [
            ['Фантастика', 'Дюна'],
            ['Ужасы', 'Дракула'],
            ['Детективы', 'Один из нас лжет'],
            ['Мультфильмы', 'Король Лев'],
            ['Комедии', 'Сон в летнюю ночь']
        ]
    )
    def test_get_books_with_specific_genre(self, genre, book_name):
        collector = BooksCollector()

        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)

        result = collector.get_books_with_specific_genre(genre)

        assert book_name in result

    def test_get_books_with_specific_genre_invalid_genre(self):
        collector = BooksCollector()

        collector.add_new_book('Дневник памяти')
        collector.set_book_genre('Дневник памяти', 'Роман')

        result = collector.get_books_with_specific_genre('Роман')

        assert result == []

    def test_get_books_with_specific_genre_empty_dict(self):
        collector = BooksCollector()

        result = collector.get_books_with_specific_genre('Фантастика')

        assert result == []

    def test_get_books_genre(self):
        collector = BooksCollector()

        collector.add_new_book('Дюна')
        collector.set_book_genre('Дюна', 'Фантастика')

        result = collector.get_books_genre()

        assert result == {'Дюна': 'Фантастика'}

    @pytest.mark.parametrize(
        'genre, expected_result',
        [
            ['Фантастика', True],
            ['Мультфильмы', True],
            ['Комедии', True],
            ['Ужасы', False],
            ['Детективы', False]
        ]
    )
    def test_get_books_for_children(self, genre, expected_result):
        collector = BooksCollector()

        collector.add_new_book('Книга')
        collector.set_book_genre('Книга', genre)

        result = collector.get_books_for_children()

        if expected_result:
            assert 'Книга' in result
        else:
            assert 'Книга' not in result

    def test_add_book_in_favorites(self):
        collector = BooksCollector()

        collector.add_new_book('Дневник памяти')
        collector.add_book_in_favorites('Дневник памяти')

        assert 'Дневник памяти' in collector.get_list_of_favorites_books()

    def test_delete_book_from_favorites(self):
        collector = BooksCollector()

        collector.add_new_book('Дневник памяти')
        collector.add_book_in_favorites('Дневник памяти')
        collector.delete_book_from_favorites('Дневник памяти')

        assert 'Дневник памяти' not in collector.get_list_of_favorites_books()

    def test_get_list_of_favorites_books_empty(self):
        collector = BooksCollector()

        assert collector.get_list_of_favorites_books() == []