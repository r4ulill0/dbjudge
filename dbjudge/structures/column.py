"""Database column representation"""
from dbjudge import type_compatible
from dbjudge import exceptions
from .fake_types import Default


class Column:
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
            self._ctype = value
        else:
            raise exceptions.InvalidColumnTypeError(
                "Unsupported column type: "+str(value))
