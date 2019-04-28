ACCEPTED_STRING_DB_TYPES = (
    'character',
    'character varying',
    'national character',
)
ACCEPTED_INTEGER_DB_TYPES = ('integer','smallint')
ACCEPTED_DOUBLE_DB_TYPES = ('real',)
ACCEPTED_INTERVAL_DB_TYPES = ('interval')
ACCEPTED_BOOLEAN_DB_TYPES = ('boolean')
ACCEPTED_DATE_DB_TYPES = (
    'date',
    'timestamp with time zone',
    'timestamp without time zone'
)
def is_string(db_type):
    return (db_type in ACCEPTED_STRING_DB_TYPES)

def is_integer(db_type):
    return (db_type in ACCEPTED_INTEGER_DB_TYPES)

def is_double(db_type):
    return (db_type in ACCEPTED_DOUBLE_DB_TYPES)

def is_interval(db_type):
    return (db_type in ACCEPTED_INTERVAL_DB_TYPES)

def is_boolean(db_type):
    return (db_type in ACCEPTED_BOOLEAN_DB_TYPES)

def is_date(db_type):
    return (db_type in ACCEPTED_DATE_DB_TYPES)