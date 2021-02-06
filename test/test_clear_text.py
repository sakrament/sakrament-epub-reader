from sakrament_epub_reader.text import *


def test_OneToIReplacementRegexProcessor():
    p = OneToIReplacementRegexProcessor()
    assert p.process("1абв") == "іабв"
    assert p.process("абв1") == "абві"
    assert p.process("а1б") == "аіб"
    assert p.process("а1б1в") == "аібів"
    assert p.process("аб 1абв аб") == "аб іабв аб"
    assert p.process("аб абв1 аб") == "аб абві аб"
    assert p.process("аб 1а1б1в1 аб") == "аб іаібіві аб"
    assert p.process("1") == "1"
    assert p.process(" 1 ") == " 1 "
    assert p.process(" 111 ") == " 111 "
    assert p.process("а11б") == "а11б"
    assert p.process("11б") == "11б"
    assert p.process("a11") == "a11"
    assert p.process("аб 1 аб") == "аб 1 аб"
    assert p.process("аб 111 аб") == "аб 111 аб"


def test_DigitsInTextRegexProcessor():
    p = DigitsInTextRegexProcessor()
    assert p.process("1а") == " адзін а"
    assert p.process("а1") == "а адзін "
    assert p.process("а123") == "а адзін два тры "
    assert p.process("123б") == " адзін два тры б"
    assert p.process("1б2") == " адзін б два "
    assert p.process("a 1б") == "a  адзін б"
    assert p.process("a1 б") == "a адзін  б"
    assert p.process("-1") == "-1"


def test_LongIntegerNumberRegexProcessor():
    p = LongIntegerNumberRegexProcessor()
    assert p.process("123456789012345").startswith("адзін два тры")
    assert p.process("12345678901234") == "12345678901234"


def test_MinusSignRegexProcessor():
    p = MinusSignRegexProcessor()
    assert p.process("-123") == "мінус 123"
    assert p.process("абв -123") == "абв мінус 123"


def test_DecimalNumberRegexProcessor():
    p = DecimalNumberRegexProcessor()
    assert p.process("1.2") == ""

#
# def test_simple():
#     # keep non numbers untouched
#     assert clear_text('') == ''
#     assert clear_text(' ') == ' '
#     assert clear_text('мама') == 'мама'
#
#
# def test_numbers():
#     # convert numbers
#     assert clear_text('123') == 'сто дваццаць тры'
#     assert clear_text('321') == 'трыста дваццаць адзін'
#
#
# def test_numbers_mixed_with_text():
#     # convert numbers, keep other text untouched
#     assert clear_text("ааааа 197654  ббббб 23344556678 ссссс 1.5  245671 год") == \
#            'ааааа сто дзевяноста сем тысяч шэсцьсот пяцьдзесят чатыры  ' \
#            'ббббб дваццаць тры мільярды трыста сорак чатыры мільёны пяцьсот пяцьдзесят шэсць тысяч шэсцьсот семдзесят восем ' \
#            'ссссс адзін.пяць  дзвесце сорак пяць тысяч шэсцьсот семдзесят адзін год'
#
#     assert clear_text(" 3.77 ааааа 1957  ссссс 1.5 ммммм 33.67") == ' тры.семдзесят сем ааааа адна тысяча ' \
#                                                                     'дзевяцьсот пяцьдзесят сем  ссссс адзін.пяць ' \
#                                                                     'ммммм трыццаць тры.шэсцьдзесят сем'
