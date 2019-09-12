import pytest
from custom_fakes import custom_generator
from custom_fakes import custom_loader
from structures.column import Column
from structures.fake_types import Regex, Custom
from exceptions import InvalidColumnFakeType


def test_invalid_column_type():
    with pytest.raises(InvalidColumnFakeType):
        dumb_col = Column('dumb', 'dumb')
        modified_regex = Regex('a?b')
        modified_regex.category = 'modified'
        dumb_col.fake_type = modified_regex

        custom_generator.gen_string(dumb_col)


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


def test_custom_fake_cache(load_csv_fakes):
    cache = custom_generator.Custom_cache('woman_names')

    initial_size = len(cache.cached_data)
    cache.cached_data.clear()
    cleared_size = len(cache.cached_data)
    cache.check_cache('man_names')
    updated_size = len(cache.cached_data)

    assert initial_size == 24494
    assert cleared_size == 0
    assert updated_size == 25442


def test_get_custom_fake(database_manager, load_csv_fakes):

    custom_fake_type = 'woman_names'
    fake_type = Custom(custom_fake_type)

    column = Column('Wnames', 'character varying')

    column.fake_type = fake_type

    result = set()
    file_rows_without_header = 24494

    for _ in range(file_rows_without_header+100):
        addition = custom_generator.gen_string(column)
        result.add(addition)

    assert(len(result) == file_rows_without_header)


def test_custom_fake_loader(database_manager, load_csv_fakes):

    reader = database_manager.main_connection.cursor()
    reader.execute(
        "SELECT * FROM dbjudge_fake_data WHERE fake_type = 'woman_names'")
    results = reader.fetchall()
    reader.close()

    file_rows_without_header = 24494
    assert(len(results) == file_rows_without_header)
