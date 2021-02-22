from sakrament_epub_reader.text import *


def test_DecimalNumberRegexProcessor():
    p = DecimalNumberProcessor()
    assert p.process("1.2") == "адна цэлая дваццаць сотых"


def test_IntegerNumberRegexProcessor():
    p = IntegerNumberProcessor()
    assert p.process("123") == "сто дваццаць тры"
    assert p.process("1234567890123450") == "1234567890123450"


def test_OneToIReplacementRegexProcessor():
    p = OneToIReplacementProcessor()
    assert p.process("1абв") == "іабв"
    assert p.process("абв1") == "абві"
    assert p.process("а1б") == "аіб"
    assert p.process("а1б1в") == "аібів"
    assert p.process("аб 1абв аб") == "аб іабв аб"
    assert p.process("аб абв1 аб") == "аб абві аб"
    assert p.process("аб 1а1б1в1 аб") == "аб іаібіві аб"
    assert p.process("а11б") == "аііб"
    assert p.process("11б") == "ііб"
    assert p.process("a11") == "aіі"

    assert p.process("аб 111 аб") == "аб ііі аб"
    assert p.process("1ра п1л1т.1р1н1й") == "іра піліт.іріній"

def test_CleanGrafSymbolProcessor():
    p = CleanGrafSymbolProcessor()
    assert p.process("Матушка ^^ Россия.Hjcc,-ура ") == "Матушка  Россия.,-ура "
    assert p.process("Мілая Беларусь.^.іріна,-123") == "Мілая Беларусь..іріна,-123"

def test_DigitsInTextRegexProcessor():
    p = DigitsInTextProcessor()
    assert p.process("1а") == " адзін а"
    assert p.process("а1") == "а адзін "
    assert p.process("а123") == "а адзін  два  тры "
    assert p.process("123б") == " адзін  два  тры б"
    assert p.process("1б2") == " адзін б два "
    assert p.process("a 1б") == "a  адзін б"
    assert p.process("a1 б") == "a адзін  б"
    assert p.process("-1") == "- адзін "


def test_simple():
    # не трогаем простые последовательности
    assert process('') == ''
    assert process(' ') == ' '
    assert process('мама') == 'мама'


def test_complex():
    # convert numbers, keep other text untouched
    assert process("ааааа 197654  ббббб 23344556678 ссссс 1.5  245671 год") == "ааааа сто дзевяноста сем тысяч шэсцьсот пяцьдзесят чатыры  ббббб дваццаць тры мільярды трыста сорак чатыры мільёны пяцьсот пяцьдзесят шэсць тысяч шэсцьсот семдзесят восем ссссс адна цэлая пяцьдзесят сотых  дзвесце сорак пяць тысяч шэсцьсот семдзесят адзін год"
    assert process(" 3.77 ааааа 1957  ссссс 1.5 ммммм 33.67") == ' тры цэлых семдзесят сем сотых ааааа адна тысяча дзевяцьсот пяцьдзесят сем  ссссс адна цэлая пяцьдзесят сотых ммммм трыццаць тры цэлых шэсцьдзесят сем сотых'
