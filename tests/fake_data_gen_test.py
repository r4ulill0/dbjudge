import pytest

import type_compatible
from fake_data_gen import Faker
from structures import Table, Column

@pytest.fixture
def faker():
    table = Table("somename","pk")
    faker = Faker(table)
    return faker

def test_format_string_fake(faker):
    input = "text"
    output = faker._format_string_fake(input)
    expected_output = "\'text\'"

    assert output == expected_output

def test_gen_string(faker):
    output = faker._gen_string()

    assert isinstance(output, str)
    assert len(output) == 10

def test_string_generate_default_fake(faker):
    for ctype in type_compatible.ACCEPTED_STRING_DB_TYPES:
        output = faker._generate_default_fake(ctype)
        assert isinstance(output, str)

def test_generate_data_pool(faker):
    column = Column("column",'character varying')
    size = 1000
    pool = faker._generate_data_pool(column,size)

    assert len(pool) == size

def test_init():
    table = Table("person","id")
    col_id = Column("id", "character varying")
    col_name = Column("name", "character varying")
    table.add_column(col_id)
    table.add_column(col_name)

    faker = Faker(table)

    assert len(faker.column_data_pool) == 2
    assert len(faker.column_data_pool["id"]) == 100
    assert len(faker.column_data_pool["name"]) == 100

def test_generate_fake(faker):
    expected_output = "surprise"
    
    pool = set()
    pool.add(expected_output)
    column = Column("somename","character varying")
    faker.column_data_pool[column.name] = pool

    output = faker.generate_fake(column)

    assert output == expected_output
