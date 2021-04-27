from pagetools.src.Page import Page
from pagetools.src.regularization.Rules import Ruleset

import unicodedata as ud
from pathlib import Path
from typing import Union


class Regularizer:
    def __init__(self, xml: Path, rules: Ruleset, normalize_unicode: Union[None, str]):
        self.page = Page(xml)
        self.ruleset = rules
        self.normalize_unicode = normalize_unicode

    def regularize(self):
        for elem in self.page.get_texts():
            if self.normalize_unicode:
                text = ud.normalize(self.normalize_unicode, "".join(elem.itertext()))
            else:
                text = "".join(elem.itertext())

            elem.text = self.ruleset.apply(text)

    def export(self, output: Path):
        self.page.export(output)
