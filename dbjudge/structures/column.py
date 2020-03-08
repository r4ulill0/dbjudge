from .fake_types import Default


class Column:
    def __init__(self, name, ctype, nullable=False, unique=False):
        self.name = name
        self.ctype = ctype
        self.constraint = ""
        self.reference = []
        self.nullable = nullable
        self.unique = unique
        self.max_char_len = None
        self.max_value = None
        self.min_value = None
        self.fake_type = Default()

    def add_reference(self, reference):
        self.reference.append(reference)

    # TODO modify setters to verify types (ctype with type compatible)
