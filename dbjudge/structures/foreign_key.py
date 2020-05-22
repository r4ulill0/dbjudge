"""Database foreign key representation"""


class ForeignKey:
    """Database foreign key representation"""

    def __init__(self, source_table, target_table):
        self.source_table = source_table
        self.target_table = target_table
        self._references = []

    def add_column_reference(self, reference):
        """Add a column reference to the foreign key.

        :param reference: column reference
        :type reference: Reference
        """
        self._references.append(reference)

# TODO modify with @property as in column ctype following python standard use
    def get_column_references(self):
        return self._references
