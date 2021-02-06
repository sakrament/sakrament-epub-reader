import pathlib
import sakrament_epub_reader


def get_data_path():
    return pathlib.Path(__file__).resolve().parent / 'data'


def get_books_path():
    return get_data_path() / 'books'


def run_book_test(book_name):
    book_path = get_books_path() / book_name
    sakrament_epub_reader.process_book(book_path, False, False)


def test_kolas():
    run_book_test('Kolas_Na-rostanyah.epub')


def test_korotkevich():
    run_book_test('Korotkevich_Kalasy-pad-syarpom-tvaim.epub')


def test_newspaper():
    run_book_test('newspaper.epub')
