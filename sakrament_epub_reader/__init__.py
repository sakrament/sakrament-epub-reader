import logging
import docopt
import pathlib
import ebooklib
import ebooklib.epub

help = \
    """
    Sakrament EPUB reader
    
    Usage:
        sakrament-epub-reader <input_epub_file>
        sakrament-epub-reader (-h | --help) 
    """

def main(argv):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s ' + logging.BASIC_FORMAT,
        datefmt='[%H:%M:%S]')

    args = docopt.docopt(help, argv=argv)

    input_epub_file = pathlib.Path(args['<input_epub_file>']).resolve()

    logging.info('Program started')
    logging.info('Input epub file: %s', input_epub_file)

    if not input_epub_file.exists():
        logging.error("Can't find input EPUB file: %s", input_epub_file)
        raise Exception()

    book = ebooklib.epub.read_epub(input_epub_file)

    for i in book.get_items():
        if i.get_type() != ebooklib.ITEM_DOCUMENT:
            continue
        logging.info("Item: %s", i.get_name())

    logging.info('OK')
