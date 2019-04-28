
ACCEPTED_STRING_DB_TYPES = (
    'character',
    'character varying',
    'national character',
)

def is_string(db_type):
    return (db_type in ACCEPTED_STRING_DB_TYPES)