
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
