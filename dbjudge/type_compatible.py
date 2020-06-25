# MIT License

# Copyright (c) 2020 Raúl Medina González <raulmgcontact@gmail.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Supported database types."""

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
    """Return True if the database type is a string supported type supported, False otherwise.
    """
    return db_type in ACCEPTED_STRING_DB_TYPES


def is_integer(db_type):
    """Return True if the database type is an integer supported type, False otherwise.
    """
    return db_type in ACCEPTED_INTEGER_DB_TYPES


def is_float(db_type):
    """Return True if the database type is a float supported type, False otherwise.
    """
    return db_type in ACCEPTED_FLOAT_DB_TYPES


def is_interval(db_type):
    """Return True if the database type is a interval supported type, False otherwise.
    """
    return db_type in ACCEPTED_INTERVAL_DB_TYPES


def is_boolean(db_type):
    """Return True if the database type is a boolean supported type, False otherwise.
    """
    return db_type in ACCEPTED_BOOLEAN_DB_TYPES


def is_date(db_type):
    """Return True if the database type is a date supported type, False otherwise.
    """
    return db_type in ACCEPTED_DATE_DB_TYPES


def bytes_limit(db_type):
    """Returns the bytes limit of a specific database type. Only integer types are supported.
    """
    return BYTES_OF[db_type]


def is_valid(db_type):
    """Return True if the database type is supported, False otherwise.
    """
    valid = is_string(db_type)\
        or is_integer(db_type)\
        or is_float(db_type)\
        or is_interval(db_type)\
        or is_boolean(db_type)\
        or is_date(db_type)

    return valid
