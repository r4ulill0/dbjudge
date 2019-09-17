
class ForeignKey:
    def __init__(self, source_table, target_table):
        self.source_table = source_table
        self.target_table = target_table
        self._references = []

    def add_column_reference(self, reference):
        self._references.append(reference)

    def get_column_references(self):
        return self._references
