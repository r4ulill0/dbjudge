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
"""Database column representation"""
from dbjudge import type_compatible
from dbjudge import exceptions
from .fake_types import Default


class Column:  # pylint: disable=too-many-instance-attributes
    """Database column representation
    """

    def __init__(self, name, ctype, nullable=False, unique=False):
        self.name = name
        self.ctype = ctype
        self.constraint = ""
        self.column_instances = []
        self.reference = []
        self.nullable = nullable
        self.unique = unique
        self.max_char_len = None
        self.max_value = None
        self.min_value = None
        self.fake_type = Default()

    def add_reference(self, reference):
        """Adds a reference to another column

        :param reference: Reference to a table
        :type reference: Reference
        """
        self.reference.append(reference)

    @property
    def ctype(self):
        """ctype attribute.

        :raises: InvalidColumnTypeError if ctype is not a supported column type.
        """
        return self._ctype

    @ctype.setter
    def ctype(self, value):
        if type_compatible.is_valid(value):
            # pylint: disable=attribute-defined-outside-init
            self._ctype = value
        else:
            raise exceptions.InvalidColumnTypeError(
                "Unsupported column type: "+str(value))
