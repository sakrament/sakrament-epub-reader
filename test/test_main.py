import pathlib
import sakrament_epub_reader


def get_data_path():
    return pathlib.Path(__file__).resolve().parent / 'data'


def get_books_path():
    return get_data_path() / 'books'


def run_book_test(book_name):
    book = get_books_path() / book_name
    argv = [str(book)]  # program name is not used
    sakrament_epub_reader.main(argv)


def test_kolas():
    run_book_test('Kolas_Na-rostanyah.epub')


def test_korotkevich():
    run_book_test('Korotkevich_Kalasy-pad-syarpom-tvaim.epub')
