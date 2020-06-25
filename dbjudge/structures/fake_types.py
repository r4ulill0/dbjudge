# MIT License

# Copyright (c) 2020 Raúl Medina González <raulmgcontact@gmail.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""available data types for data generation."""

from enum import Enum


class FakeType(Enum):  # pylint: disable=too-few-public-methods
    """Fake type category.
    """
    default = 0
    regex = 1
    custom = 2


class Default:  # pylint: disable=too-few-public-methods
    """Default data type.
    """

    def __init__(self):
        self.category = FakeType.default


class Regex:  # pylint: disable=too-few-public-methods
    """Regular expression based data type.
    """

    def __init__(self, expression):
        self.category = FakeType.regex
        self.expression = expression


class Custom:  # pylint: disable=too-few-public-methods
    """Custom preloaded data type.
    """

    def __init__(self, fake_type):
        self.category = FakeType.custom
        self.custom_type = fake_type
