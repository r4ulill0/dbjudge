import pytest
import type_compatible


def test_compatible_posgresql_strings():
    char = "character"
    varchar = "character varying"
    nchar = "national character"

    assert type_compatible.is_string(char)
    assert type_compatible.is_string(varchar)
    assert type_compatible.is_string(nchar)


def test_compatible_posgresql_integer():
    num = "integer"
    snum = "smallint"

    assert type_compatible.is_integer(num)
    assert type_compatible.is_integer(snum)


def test_compatible_posgresql_double():
    real = "real"
    assert type_compatible.is_float(real)


def test_compatible_posgresql_interval():
    interval = "interval"
    assert type_compatible.is_interval(interval)


def test_compatible_posgresql_boolean():
    boolean = "boolean"
    assert type_compatible.is_boolean(boolean)


def test_compatible_posgresql_date():
    date = "date"
    timestamp = "timestamp without time zone"
    timestampZ = "timestamp with time zone"

    assert type_compatible.is_date(date)
    assert type_compatible.is_date(timestamp)
    assert type_compatible.is_date(timestampZ)
