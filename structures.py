import exceptions

class Column:
    def __init__(self, name, ctype, nullable=False, unique=False):
        self.name = name
        self.ctype = ctype
        self.constraint = ""
        self.reference = []
        self.nullable = nullable
        self.unique = unique
        self.max_char_len = None
        self.fake_type = "default"

    def add_reference(self, reference):
        self.reference.append(reference)


class Table:
    def __init__(self, name, primary_key):
        self.name = name
        self.columns = {}
        self.primary_key = primary_key
        self.foreign_keys = []
        self.fake_data_size = 100
        self.row_instances = []

    def add_column(self, column:Column):
        self.columns[column.name] = column
    
    def set_fake_data_size(self, num_rows):
        self.fake_data_size = num_rows

class Context:
    def __init__(self):
        self.tables = []

    def add_table(self, table:Table):
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

class Reference:
    def __init__(self, source, target):
        self.source = source
        self.target = target

class ForeignKey:
    def __init__(self, source_table, target_table):
        self.source_table = source_table
        self.target_table = target_table
        self._references = []
    
    def add_column_reference(self, reference):
        self._references.append(reference)

    def get_column_references(self):
        return self._references