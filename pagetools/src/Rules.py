from typing import List, Union
from pathlib import Path
import json
import regex as re


class Rule:
    def __init__(self, original: str, target: str, rule_type: str):
        self.original = original
        self.target = target
        self.rule_type = rule_type

    def set_original(self, original: str):
        self.original = original

    def get_original(self) -> str:
        return self.original

    def set_target(self, target: str):
        self.target = target

    def get_target(self) -> str:
        return self.target

    def get_rule_type(self) -> str:
        return self.rule_type

    def apply(self, text: str):
        if self.rule_type == "raw":
            return text.replace(self.original, self.target)
        elif self.rule_type == "regex":
            return re.sub(self.original, self.target, text)
        else:
            return "Rule type not supported."

    def __str__(self):
        return f"{self.original} -> {self.target} ({self.rule_type})"


class Ruleset:
    def __init__(self, rules: List[Rule] = None):
        self.rules: List[Rule] = rules if rules else []

    def get_rules(self) -> List[Rule]:
        return self.rules

    def from_json(self, _json: Union[list, Path]):
        data = None
        if isinstance(_json, Path):
            with _json.open("r") as json_file:
                data = json.load(json_file)
        elif isinstance(_json, list):
            data = _json
        for _rule in data:
            rule = Rule(original=_rule["rule"][0], target=_rule["rule"][1], rule_type=_rule["type"])
            self.add_rule(rule)

    def add_rule(self, rule: Rule, index: int = None):
        if index:
            self.rules.insert(index, rule)
        else:
            self.rules.append(rule)

    def apply(self, text: str) -> str:
        for rule in self.rules:
            text = rule.apply(text)
        return text

    def remove_rule(self, index: int):
        self.rules.pop(index)

    def __add__(self, other):
        if isinstance(other, Ruleset):
            self.rules.extend(other.get_rules())
            return Ruleset(rules=self.rules)
        else:
            return NotImplemented

    def __radd__(self, other):
        return self.__add__(other)

    def __eq__(self, ruleset):
        if isinstance(ruleset, Ruleset):
            return self.rules == ruleset.get_rules()
        else:
            return NotImplemented
