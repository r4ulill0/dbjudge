import pytest
from custom_fakes import custom_generator
from custom_fakes import custom_loader
from structures.column import Column
from structures.fake_types import Regex, Custom


@pytest.fixture(scope='module')
def load_csv_fakes(database_manager):
    file_path = 'tests/csv_files/names.csv'
    results = custom_loader.load_csv_fakes(file_path)
    custom_loader.save_to_database(results, (0,), ('woman_names',))


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
