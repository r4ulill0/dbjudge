"""Database table representation"""
from dbjudge.structures.column import Column


class Table:
    """Database table representation"""

    def __init__(self, name, primary_key):
        self.name = name
        self.columns = {}
        self.primary_key = primary_key
        self.foreign_keys = []
        self.fake_data_size = 100
        self.row_instances = []

    def add_column(self, column: Column):
        """Adds a column to the table.

        :param column: new column
        :type column: Column
        """
        self.columns[column.name] = column
