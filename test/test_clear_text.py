from sakrament_epub_reader import clear_text


clear_text('123')

def test_simple():
    # keep non numbers untouched
    assert clear_text('') == ''
    assert clear_text(' ') == ' '
    assert clear_text('мама') == 'мама'


def test_numbers():
    # convert numbers
    assert clear_text('123') == 'сто дваццаць тры'
    assert clear_text('321') == 'трыста дваццаць адзін'


def test_numbers_mixed_with_text():
    # convert numbers, keep other text untouched
    assert clear_text("ааааа 197654  ббббб 23344556678 ссссс 1.5  245671 год") == \
           'ааааа сто дзевяноста сем тысяч шэсцьсот пяцьдзесят чатыры  ' \
           'ббббб дваццаць тры мільярды трыста сорак чатыры мільёны пяцьсот пяцьдзесят шэсць тысяч шэсцьсот семдзесят восем ' \
           'ссссс адзін.пяць  дзвесце сорак пяць тысяч шэсцьсот семдзесят адзін год'

    assert clear_text(" 3.77 ааааа 1957  ссссс 1.5 ммммм 33.67") == ' тры.семдзесят сем ааааа адна тысяча ' \
                                                                    'дзевяцьсот пяцьдзесят сем  ссссс адзін.пяць ' \
                                                                    'ммммм трыццаць тры.шэсцьдзесят сем'
