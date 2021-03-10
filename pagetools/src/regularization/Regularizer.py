from pagetools.src.Page import Page
from pagetools.src.regularization.Rules import Ruleset

from pathlib import Path


class Regularizer:
    def __init__(self, xml: Path, rules: Ruleset):
        self.page = Page(xml)
        self.ruleset = rules

    def regularize(self):
        for elem in self.page.get_texts():
            elem.text = self.ruleset.apply("".join(elem.itertext()))

    def export(self, output: Path):
        self.page.export(output)
