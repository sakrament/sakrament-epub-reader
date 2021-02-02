# Sakrament EPUB reader

A tool for converting textual epub books to a set of mp3 files via Sakrament's TTS engine.

The project was made for ["Belarusian society of the visually impaired"](https://beltiz.by/) to help visually impaired people read (listen to) Belarusian texts.

For number to text conversion we use an excellent [ru_number_to_text](https://github.com/seriyps/ru_number_to_text) module. 
We also wrote the Belarusian version of the module.

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

## Other

For mp3 encoding we use [LAME](https://lame.sourceforge.io/) encoder. 
Binaries for Windwos are taken [here](https://www.rarewares.org/mp3-lame-bundle.php#lame-current-sbd).
Version is `LAME 3.100.1` (win32 bundle).

## TODO

* `num2t4be` and `num2t4ru` modules have repeated code, get rid of it. Write Unit-tests for these conversions.
* russian language support
