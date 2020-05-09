import pytest

from dbjudge.structures.column import Column
from dbjudge import exceptions


def test_unsupported_ctype():
    with pytest.raises(exceptions.InvalidColumnTypeError) as expected_exception:
        Column('randomname', 'nosupptype')

    assert 'Unsupported column type: nosupptype' in str(
        expected_exception.value)
