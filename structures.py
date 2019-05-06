import exceptions

class Column:
    def __init__(self, name, ctype, nullable=False):
        self.name = name
        self.ctype = ctype
        self.constraint = ""
        self.reference = []
        self.nullable = nullable
        self.max_char_len = None
        self.fake_type = "default"
        self.instances_pool = set()

    def add_reference(self, reference):
        self.reference.append(reference)


class Table:
    def __init__(self, name, primary_key):
        self.name = name
        self.columns = {}
        self.primary_key = primary_key
        self.fake_data_size = 100

    def add_column(self, column:Column):
        self.columns[column.name] = column
    
    def set_fake_data_size(self, num_rows):
        self.fake_data_size = num_rows

    def update_instances_pools(self, values_list):
        for key, value in zip(self.columns.keys(),values_list):
            self.columns[key].instances_pool.add(value)

class Context:
    def __init__(self):
        self.tables = []

    def add_table(self, table:Table):
        self.tables.append(table)

    def resolve_column_reference(self, reference):
        table_name, column_name = reference
        for table in self.tables:
            if (table.name == table_name):
                return table.columns[column_name]

        raise exceptions.ColumnReferenceNotFound('column {column} not found in table: {table}',
            column_name, table_name)