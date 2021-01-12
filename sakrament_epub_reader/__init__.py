import logging
import docopt
import pathlib
import html2text
import ebooklib
import ebooklib.epub
import shutil
import subprocess
import time
import os


data_path = pathlib.Path(__file__).resolve().parent / 'data'
tts_engine_path = data_path / 'bin' / 'win32' / 'tts_engine' / 'tts_engine.exe'
ffmpeg_path = data_path / 'bin' / 'win32' / 'ffmpeg' / 'bin' / 'ffmpeg.exe'


def run_tts_engine(text, output_wav_file):
    """Converts text to PCM audio data via calling tts_engine"""
    # todo: lang

    input_bytes = text.encode(encoding='utf-8', errors='strict')
    original_cwd = os.getcwd()

    try:
            os.chdir(tts_engine_path.parent)
            completed_process = subprocess.run(
                [str(tts_engine_path), '--lang', 'be', '--wav', str(output_wav_file)],
                input=input_bytes,
                check=True,
                text=False)
    finally:
        os.chdir(original_cwd)


def convert_pcm_to_mp3(pcm_file, mp3_file):
    """Convert PCM data into MP3 data format by passing it through ffmpeg"""

    command = [
        str(ffmpeg_path),
        '-hide_banner',
        '-loglevel', 'warning',
        '-vn',
        #'-f', 's16le',
        #'-ar', '48000',
        #'-ac', '1',
        '-i', str(pcm_file),
        str(mp3_file)
    ]

    subprocess.run(command, check=True)


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

        logging.info("Processing book item: %s %s", formatted_idx, item.get_name())

        body = item.get_body_content().decode("utf-8")
        clean_body = h2t.handle(body)

        chapter_path = output_dir / f'{formatted_idx}_{pathlib.Path(id).stem}'
        chapter_path_txt = chapter_path.with_suffix('.txt')
        chapter_path_wav = chapter_path.with_suffix('.wav')
        chapter_path_mp3 = chapter_path.with_suffix('.mp3')

        # only for debugging epub parsing
        with chapter_path_txt.open('w', encoding='utf-8') as f:
            f.write(clean_body)

        text = clean_body[0:1024]

        logging.info("  TTS start")
        tts_start_time = time.time()
        run_tts_engine(text, chapter_path_wav)
        logging.info("  TTS complete (%s)", time.time() - tts_start_time)


        #logging.info("  MP3 conversion start")
        #mp3_start_time = time.time()
        #convert_pcm_to_mp3(chapter_path_wav, chapter_path_mp3)
        #logging.info("  MP3 conversion complete (%s)", time.time() - mp3_start_time)

        #chapter_path_txt.unlink()
        #chapter_path_pcm.unlink()

        #break

    logging.info('OK')
