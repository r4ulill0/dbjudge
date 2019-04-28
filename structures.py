class Column:
    def __init__(self, name, ctype):
        self.name = name
        self.ctype = ctype
        self.constraint = ""
        self.table_reference = []
        self.fake_type = "default"

    def add_reference(self, reference):
        self.table_reference.append(reference)

class Table:
    def __init__(self, name, primary_key):
        self.name = name
        self.columns = []
        self.primary_key = primary_key
        self.fake_data_size = 100

    def add_column(self, column:Column):
        self.columns.append(column)
    
    def set_fake_data_size(self, num_rows):
        self.fake_data_size = num_rows

class Context:
    def __init__(self):
        self.tables = []

    def add_table(self, table:Table):
        self.tables.append(table)