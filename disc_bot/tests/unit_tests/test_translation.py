from disc_bot.cog_helpers.translator import Translator
from disc_bot.exceptions.translator import LanguageNotFoundError
from collections import namedtuple
import pytest

Expected = namedtuple("Expected", ["reg", "translated", "start", "end"])


@pytest.fixture
def translator(scope="function"):
    return Translator(auto_translate = True)

@pytest.fixture(params=[
    Expected("Mi amor", "My love", "spanish", "english"),
    Expected("Mi familia", "My family", "spanish", "english"),
    ])
def en_translations(request):
    return request.param

def test_to_en(translator, en_translations):
    expected = en_translations.translated
    start_string = en_translations.reg
    assert translator.translate(start_string) == expected

def test_to_sp(translator, en_translations):
    translator.set_language('spanish')
    expected = en_translations.reg
    start_string = en_translations.translated
    assert translator.translate(start_string) == expected

def test_same_lang(translator, en_translations):
    translator.auto_translate = False
    expected = en_translations.reg
    start_string = en_translations.reg
    assert translator.translate(start_string) == expected

