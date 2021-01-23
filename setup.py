import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sakrament_epub_reader",
    version="1.0.0",
    author="Sakrament",
    description="A tool for converting textual epub books to a set of mp3 files via Sakrament's TTS engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sakrament/sakrament-epub-reader",
    packages=setuptools.find_packages(),
    python_requires='>=3.8',
)
