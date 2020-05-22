"""Avaiable data types for data generation."""

from enum import Enum


class Fake_type(Enum):
    """Fake type category.
    """
    default = 0
    regex = 1
    custom = 2


class Default:
    """Default data type.
    """

    def __init__(self):
        self.category = Fake_type.default


class Regex:
    """Regular expression based data type.
    """

    def __init__(self, expression):
        self.category = Fake_type.regex
        self.expression = expression


class Custom:
    """Custom preloaded data type.
    """

    def __init__(self, fake_type):
        self.category = Fake_type.custom
        self.custom_type = fake_type
