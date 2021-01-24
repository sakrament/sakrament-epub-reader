# Sakrament EPUB reader

A tool for converting textual epub books to a set of mp3 files via Sakrament's TTS engine.

## Make Windows distribution

* Use Windows 7 SP 1 (32 bit)
* Use official Python 3.8 distribution (the latest Python which works on 32 bit)
* Install pipenv into the main Python in the system (using `pip`)
* Using `cmd.exe` configure python virtual environment via `pipenv` 
```shell
pipenv install
```
* Open `cmd.exe` and activate the virtual environment and freeze the executable for distribution
```shell
pipenv shell
run_pyinstaller.bat
```

Then you could find the `sakrament_epub_reader.exe` file in `dist` directory.
