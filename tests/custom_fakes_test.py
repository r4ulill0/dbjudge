import pytest
from customFakes import custom_generator
from structures.column import Column
from structures.fake_types import Regex


def test_gen_regex():

    expression = '[ab]+'
    regex = Regex(expression)

    column = Column('CName', 'character varying')

    column.fake_type = regex
    column.max_char_len = 5

    result = custom_generator.gen_string(column)

    for char in result:
        assert (char == 'a') or (char == 'b')
    assert len(result) <= 5
