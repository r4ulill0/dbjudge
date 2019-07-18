import exceptions
from structures.table import Table


class Context:
    def __init__(self):
        self.tables = []

    def add_table(self, table: Table):
        self.tables.append(table)

    def get_table_by_name(self, table_name):
        for table in self.tables:
            if(table.name == table_name):
                return table

    def resolve_column_reference(self, reference):
        table_name, column_name = reference
        for table in self.tables:
            if (table.name == table_name):
                return table.columns[column_name]

        raise exceptions.ColumnReferenceNotFound('column {column} not found in table: {table}',
                                                 column_name, table_name)
