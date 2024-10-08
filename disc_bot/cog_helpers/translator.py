import logging
from typing import ClassVar

from deep_translator import GoogleTranslator

from ..exceptions.translator import LanguageNotFoundError

logger = logging.getLogger("translator")

_languages = GoogleTranslator().get_supported_languages()
_languages_dict = GoogleTranslator().get_supported_languages(as_dict=True)
_translator = GoogleTranslator(source="auto", target="en")


class Translator:
    default_language = "en"
    curr_lang = "en"
    lang_list: ClassVar = _languages
    lang_dict: ClassVar = _languages_dict
    rev_lang_list: ClassVar = [abb for lang, abb in _languages_dict.items()]

    def __init__(self, auto_translate=False):
        self.auto_translate = auto_translate

    def _translate(self, message) -> str:
        source = "auto" if self.auto_translate else self.curr_lang
        return GoogleTranslator(source=source, target=self.curr_lang).translate(message)

    def translate(self, message) -> str:
        return self._translate(message)

    def set_language(self, language: str) -> None:
        if _translator.is_language_supported(language):
            self.curr_lang = language
        else:
            raise LanguageNotFoundError(f"Was unable to find {language} in {self.lang_list} or {self.rev_lang_list}")

    def format_possible_languages(self) -> str:
        _str = "Languages to choose from:\n{0}\n{1}"
        return _str.format(", ".join(self.lang_list), ", ".join(self.rev_lang_list))
