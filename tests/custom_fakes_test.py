import pytest
import logging
from dbjudge.custom_fakes import custom_generator
from dbjudge.custom_fakes import custom_loader
from dbjudge.structures.column import Column
from dbjudge.structures.fake_types import Regex, Custom
from dbjudge.exceptions import InvalidColumnFakeType


@pytest.fixture
def expected_types(database_manager):
    expected_types = ('Header', 'for', 'test')
    yield expected_types

    writer = database_manager.main_connection.cursor()
    for e_type in expected_types:
        try:
            query = "DELETE FROM dbjudge_fake_data WHERE fake_type='{}';"
            writer.execute(query, (e_type,))
        except Exception as exception:
            logging.warning(
                "Failed to execute teardown query: %s\n%s".format((query, str(exception))))
            writer.rollback()
    database_manager.main_connection.commit()


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


def test_save_to_database_custom_names(database_manager, expected_types):
    csv_file_path = 'tests/csv_files/save_to_database_test.csv'

    loaded_data = custom_loader.load_csv_fakes(csv_file_path)
    custom_loader.save_to_database(loaded_data, selected_names=expected_types)

    reader = database_manager.main_connection.cursor()

    assertion_query = ''' SELECT data, fake_type
                        FROM dbjudge_fake_data
                        WHERE fake_type like '{}'
                            or fake_type like '{}'
                            or fake_type like '{}';
    '''.format(*expected_types)
    reader.execute(assertion_query)

    results = reader.fetchall()

    assert len(results) == 5*len(expected_types)
    for row in results:
        assert row[1] in expected_types


def test_save_to_database_default(database_manager):
    csv_file_path = 'tests/csv_files/save_to_database_test.csv'

    loaded_data = custom_loader.load_csv_fakes(csv_file_path)
    custom_loader.save_to_database(loaded_data)
    expected_titles = ('Titles', 'of', 'default')
    reader = database_manager.main_connection.cursor()

    assertion_query = ''' SELECT data, fake_type
                        FROM dbjudge_fake_data
                        WHERE fake_type like '{}'
                            or fake_type like '{}'
                            or fake_type like '{}';
    '''.format(*expected_titles)
    reader.execute(assertion_query)

    results = reader.fetchall()

    assert len(results) == 5*len(expected_titles)
    for row in results:
        assert row[1] in expected_titles
