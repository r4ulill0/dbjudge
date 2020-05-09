ACCEPTED_STRING_DB_TYPES = (
    'character',
    'character varying',
    'national character',
)
ACCEPTED_INTEGER_DB_TYPES = ('integer', 'smallint')
ACCEPTED_FLOAT_DB_TYPES = ('real',)
ACCEPTED_BOOLEAN_DB_TYPES = ('boolean')
ACCEPTED_INTERVAL_DB_TYPES = ('interval')
ACCEPTED_DATE_DB_TYPES = (
    'date',
    'time without time zone',
    'timestamp with time zone',
    'timestamp without time zone'
)
BYTES_OF = {
    'integer': 4,
    'smallint': 2,
}


def is_string(db_type):
    return db_type in ACCEPTED_STRING_DB_TYPES


def is_integer(db_type):
    return db_type in ACCEPTED_INTEGER_DB_TYPES


def is_float(db_type):
    return db_type in ACCEPTED_FLOAT_DB_TYPES


def is_interval(db_type):
    return db_type in ACCEPTED_INTERVAL_DB_TYPES


def is_boolean(db_type):
    return db_type in ACCEPTED_BOOLEAN_DB_TYPES


def is_date(db_type):
    return db_type in ACCEPTED_DATE_DB_TYPES


def bytes_limit(db_type):
    return BYTES_OF[db_type]


def is_valid(db_type):
    valid = is_string(db_type)\
        or is_integer(db_type)\
        or is_float(db_type)\
        or is_interval(db_type)\
        or is_boolean(db_type)\
        or is_date(db_type)

    return valid
