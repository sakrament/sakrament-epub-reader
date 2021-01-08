import logging
import docopt
import pathlib
import html2text
import ebooklib
import ebooklib.epub
import shutil
import subprocess
import os


data_path = pathlib.Path(__file__).resolve().parent / 'data'
tts_engine_path = data_path / 'bin' / 'mac' / 'tts_engine'


def run_tts_eingine(text):
    """Converts text to PCM audio data"""
    # todo: lang

    input_bytes = text.encode(encoding='utf-8', errors='strict')
    original_cwd = os.getcwd()

    try:
        os.chdir(tts_engine_path.parent)
        completed_process = subprocess.run(
            [str(tts_engine_path), '--lang', 'be', '--wav'],
            input=input_bytes,
            check=True,
            stdout=subprocess.PIPE)
    finally:
        os.chdir(original_cwd)

    return completed_process.stdout


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
    output_dir = input_epub_file.parent / input_epub_file.stem

    logging.info('Program started')
    logging.info('Input epub file: %s', input_epub_file)
    logging.info('Output directory: %s', output_dir)

    if not input_epub_file.exists():
        logging.error("Can't find input EPUB file: %s", input_epub_file)
        raise Exception()

    if output_dir.exists():
        logging.warning('Output directory exists. Removing it.')
        shutil.rmtree(output_dir, ignore_errors=True)

    output_dir.mkdir()

    book = ebooklib.epub.read_epub(input_epub_file)

    logging.info("Metadata id: %s", book.get_metadata('DC', 'identifier'))
    logging.info("Metadata title: %s", book.get_metadata('DC', 'title'))
    logging.info("Metadata language: %s", book.get_metadata('DC', 'language'))

    h2t = html2text.HTML2Text()
    h2t.ignore_links = True
    h2t.ignore_images = True
    h2t.ignore_tables = True
    h2t.ignore_images = True
    h2t.images_to_alt = True
    #h2t.body_width = 0  # don't wrap

    for idx, spine in enumerate(book.spine):
        id = spine[0]
        linear = spine[1]
        formatted_idx = '{:03d}'.format(idx)

        item = book.get_item_with_id(id)
        if item.get_type() != ebooklib.ITEM_DOCUMENT:
            continue

        body = item.get_body_content().decode("utf-8")
        clean_body = h2t.handle(body)

        logging.info("Item: %s %s", formatted_idx, item.get_name())

        chapter_path = output_dir / f'{formatted_idx}_{pathlib.Path(id).stem}.txt'

        with chapter_path.open('w') as f:
            f.write(clean_body)

        text = clean_body.split()[0]
        pcm = run_tts_eingine(text)

        break

    logging.info('OK')
