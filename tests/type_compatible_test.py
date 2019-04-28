import pytest
import type_compatible

def test_compatible_posgresql_strings():
    char = "character"
    varchar = "character varying"
    nchar = "national character"

    assert type_compatible.is_string(char)
    assert type_compatible.is_string(varchar)
    assert type_compatible.is_string(nchar)