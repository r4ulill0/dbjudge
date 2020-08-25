"""Database foreign key representation"""


class ForeignKey:
    """Database foreign key representation"""

    def __init__(self, source_table, target_table):
        self.source_table = source_table
        self.target_table = target_table
        self._references = []

    @property
    def references(self):
        """References attribute
        """
        return self._references

    @references.getter
    def get_references(self):
        """References attribute getter

        :return: References between tables
        :rtype: list
        """
        return self._references

    def add_column_reference(self, reference):
        """Add a column reference to the foreign key.

        :param reference: column reference
        :type reference: Reference
        """
        self._references.append(reference)
