from enum import Enum


class Fake_type(Enum):
    default = 0
    regex = 1


class Default:
    def __init__(self):
        self.category = Fake_type.default


class Regex:
    def __init__(self, expression):
        self.category = Fake_type.regex
        self.expression = expression
