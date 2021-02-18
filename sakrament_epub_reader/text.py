import re
import decimal

import sakrament_epub_reader.num2t4be as num2t4be
import sakrament_epub_reader.num2t4ru as num2t4ru


class Processor:
    """Базовый класс для всех текстовых процессоров"""
    def __init__(self, pattern, repl):
        self.name = self.__class__.__name__
        self.pattern = re.compile(pattern)
        self.repl = repl

    def process(self, text):
        return self.pattern.sub(self.repl, text)


class DecimalNumberProcessor(Processor):
    """Чтение дробных чисел (последовательность цифр
    окруженная пробелами и разделённых на две группы одной точкой)"""
    def __init__(self):
        def repl(m):
            int_units = ((u'цэлая', u'цэлых', u'цэлых'), 'f')
            exp_units = ((u'дзесятая', u'дзесятых', u'сотых'), 'f')

            number_as_decimal = decimal.Decimal(m.group())
            number_as_text = num2t4be.decimal2text(
                number_as_decimal,
                int_units=int_units,
                exp_units=exp_units)

            return number_as_text

        super().__init__(
            pattern=r"\b\d{1,15}\.\d{1,2}\b",
            repl=repl
        )


class IntegerNumberProcessor(Processor):
    """Чтение целых чисел (последовательность цифр окруженная пробелами)"""
    def __init__(self):
        def repl(m):
            number_as_digits = m.group()
            number_as_int = int(number_as_digits)
            number_as_text = num2t4be.num2text(number_as_int)
            return number_as_text

        super().__init__(
            pattern=r"\b\d{1,15}\b",
            repl=repl
        )


class OneToIReplacementProcessor(Processor):
    """Чтение одиночной цифры '1' как буквы 'i', если цифра идёт среди других букв. Попытка коррекции
    ошибок системы оптического распознавания текста применяемой у пользователей"""
    def __init__(self):
        super().__init__(
            pattern=r"1",
            repl="і"
        )


class CleanGrafSymbolProcessor(Processor):
    """ Убрать все символы кроме букв русских и белорусских, цифр и знаков препинания и пробела"""
    def __init__(self):
        super().__init__(
            pattern=r"[^А-ЯЁа-яёА-ЯІЎа-яіў0-9-.,\s]",
            repl=""
        )
class DigitsInTextProcessor(Processor):
    """Чтение цифр по одной, если не сработал ни один из предыдущих вариантов."""
    def __init__(self):
        def repl(m):
            digit_as_int = int(m.group())
            digit_as_text = num2t4be.num2text(digit_as_int)
            return ' ' + digit_as_text + ' '

        super().__init__(
            pattern=r"\d",
            repl=repl
        )


processors = [
    DecimalNumberProcessor(),
    IntegerNumberProcessor(),
    DigitsInTextProcessor(),
    OneToIReplacementProcessor(),
    CleanGrafSymbolProcessor()
]


def process(text):
    """Обработать текст всеми процессорами"""
    for p in processors:
        text = p.process(text)
    return text
