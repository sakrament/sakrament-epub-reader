import re
import decimal

import sakrament_epub_reader.num2t4be as num2t4be
import sakrament_epub_reader.num2t4ru as num2t4ru


class Processor:
    """Базовый класс для всех текстовых процессоров"""
    def __init__(self):
        self.name = self.__class__.__name__

    def process(self):
        pass


class RegexProcessor:
    """Базовый класс для всех текстовых процессоров основаных на регулярных выражениях"""
    def __init__(self, pattern, repl):
        self.pattern = re.compile(pattern)
        self.repl = repl

    def process(self, text):
        return self.pattern.sub(self.repl, text)


class OneToIReplacementRegexProcessor(RegexProcessor):
    """Чтение одиночной цифры '1' как буквы 'i', если цифра идёт среди других букв. Это коррекция
    ошибок системы оптического распознавания текста применяемой у пользователей"""
    def __init__(self):
        super().__init__(
            pattern=r"(?<=\w)(?<!1)1(?!1)|(?<!1)1(?=\w)(?!1)",
            repl="і"
        )


class DigitsInTextRegexProcessor(RegexProcessor):
    """Чтение цифр по одной, если они окруженны другими буквами. Очень вероятно, что такие
    цифры лучше не читать как целые числа в большинстве случаев."""
    def __init__(self):
        def repl(m):
            digits_as_test = [num2t4be.num2text(int(d)) for d in m.group()]
            return ' ' + ' '.join(digits_as_test) + ' '

        super().__init__(
            pattern=r"(?<=\w)\d+|\d+(?=\w)",
            repl=repl
        )


class LongIntegerNumberRegexProcessor(RegexProcessor):
    """Чтение длинных последовательностей цифр по одной, если они являются слишком длинными,
    чтобы читать их как целые числа."""
    def __init__(self):
        def repl(m):
            digits_as_test = [num2t4be.num2text(int(d)) for d in m.group()]
            return ' '.join(digits_as_test)

        super().__init__(
            pattern=r"(\d){15,}",
            repl=repl
        )


class MinusSignRegexProcessor(RegexProcessor):
    """Чтение знака '-' как 'минус', если он предшествует целому или дробному числу"""
    def __init__(self):
        super().__init__(
            pattern=r"(?<!\S)-(?=\d+)",
            repl="мінус "
        )


class DecimalNumberRegexProcessor(RegexProcessor):
    """Чтение дробных чисел (последовательность цифр окруженная пробелами
    и разделённых на две группы одной точкой)"""
    def __init__(self):
        def repl(m):
            int_units = ((u'рубль', u'рубля', u'рублей'), 'm')
            exp_units = ((u'копейка', u'копейки', u'копеек'), 'f')

            number_as_decimal = decimal.Decimal(m.group())
            number_as_text = num2t4be.decimal2text(number_as_decimal)
            return number_as_text

        super().__init__(
            pattern=r"\d+\.\d+{1,2}",
            repl=repl
        )


class IntegerNumberRegexProcessor(RegexProcessor):
    """Чтение целых чисел (последовательность цифр окруженная пробелами)"""
    def __init__(self):
        super().__init__(
            pattern=r"(\D*)(1)(\D*)",
            repl=""
        )


processors = [
    OneToIReplacementRegexProcessor(),
    DigitsInTextRegexProcessor(),
    LongIntegerNumberRegexProcessor(),
    MinusSignRegexProcessor(),
    DecimalNumberRegexProcessor(),
    IntegerNumberRegexProcessor(),
]


def process(text):
    """Обработать текст всеми процессорами"""
    for p in processors:
        text = p.process(text)
    return text
