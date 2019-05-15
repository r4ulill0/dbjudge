import pytest
import datetime
import type_compatible
from fake_data_gen import Faker
from structures import Context, Table, Column
import exceptions

@pytest.fixture
def table():
    table = Table("somename","pk")
    return table

@pytest.fixture
def faker(table):
    context = Context()
    context.add_table(table)
    faker = Faker(table, context)
    return faker

@pytest.fixture
def references_faker(faker, instances_pool):
    referenced_table = Table("target", "id")
    referenced_column = Column("id","integer")
    referenced_table.add_column(referenced_column)

    referenced_column.instances_pool = instances_pool
    
    table = Table("main","id")
    pk = Column("id","character")
    foreing_key = Column("pointer","integer")
    foreing_key.add_reference(('target','id'))
    table.add_column(pk)
    table.add_column(foreing_key)

    faker._context.add_table(referenced_table)
    faker._context.add_table(table)

    return faker

@pytest.fixture
def instances_pool():
    instances_pool = set([0,2,3,4,5,342])
    return instances_pool

def test_format_string_fake(faker):
    input = "text"
    output = faker._wrap_with_quote_marks(input)
    expected_output = "\'text\'"

    assert output == expected_output

def test_format_interval(faker):
    days = 23
    seconds = 45
    interval = datetime.timedelta(days=days, seconds=seconds)
    
    formatted_output = faker._format_interval(interval)
    expected_output = "'23 days 45.000000 seconds'::interval"

    assert formatted_output == expected_output

def test_gen_string(faker):
    output = faker._gen_string(None)
    output2 = faker._gen_string(23)

    assert isinstance(output, str)
    assert isinstance(output2, str)
    assert len(output) <= 10
    assert len(output) > 0
    assert len(output2) <= 23
    assert len(output2) > 0

def test_gen_integer(faker):
    limit_2bytes = (-32768, 32767)
    limit_4bytes = (-2147483648, 2147483647)

    output_2bytes = faker._gen_integer(2)
    output_4bytes = faker._gen_integer(4)

    assert isinstance(output_2bytes, int)
    assert isinstance(output_4bytes, int)
    assert (output_2bytes >= limit_2bytes[0]) and (output_2bytes <= limit_2bytes[1])
    assert (output_4bytes >= limit_4bytes[0]) and (output_4bytes <= limit_4bytes[1])
    
def test_gen_boolean(faker):
    output = faker._gen_boolean()
    assert isinstance(output, bool)

def test_gen_float(faker):
    output = faker._gen_float()
    assert isinstance(output, float)

def test_gen_datetime(faker):
    output = faker._gen_datetime()

    assert isinstance(output, datetime.datetime)

def test_gen_interval(faker):
    output = faker._gen_interval()
    
    assert isinstance(output, datetime.timedelta)

def test_generate_default_fake(faker):
    supported_types = (type_compatible.ACCEPTED_STRING_DB_TYPES,
        type_compatible.ACCEPTED_INTEGER_DB_TYPES,
        type_compatible.ACCEPTED_BOOLEAN_DB_TYPES,
        type_compatible.ACCEPTED_FLOAT_DB_TYPES,
        type_compatible.ACCEPTED_DATE_DB_TYPES,
        type_compatible.ACCEPTED_INTERVAL_DB_TYPES)

    for supp_type in supported_types:
        for ctype in supp_type:
            column = Column("temp", ctype)
            output = faker._generate_default_fake(column)
            assert isinstance(output, str)

def test_default_generate_data_pool(faker):
    column = Column("column",'character varying')
    size = 1000
    pool = faker._generate_data_pool(column,size)

    assert len(pool) == size

def test_is_pool_big_enough(faker):
    bool_column = Column('bool','boolean')
    int_column = Column('int', 'integer')

    full_boolean_pool = faker._is_pool_big_enough(2, 100, bool_column)
    overfilled_boolean_pool = faker._is_pool_big_enough(3, 100, bool_column)
    underfilled_boolean_pool = faker._is_pool_big_enough(1, 100, bool_column)
    empty_boolean_pool = faker._is_pool_big_enough(0, 100, bool_column)

    full_pool = faker._is_pool_big_enough(100, 100, int_column)
    overfilled_pool = faker._is_pool_big_enough(101, 100, int_column)
    underfilled_pool = faker._is_pool_big_enough(99, 100, int_column)
    empty_pool = faker._is_pool_big_enough(0, 100, int_column)

    assert full_boolean_pool == True, 'full boolean pool is not enough'
    assert overfilled_boolean_pool == True, 'overfilled boolean pool is not enough'
    assert underfilled_boolean_pool == False, 'underfilled boolean pool is enough'
    assert empty_boolean_pool == False, 'empty boolean pool is enough'
    assert full_pool == True, 'full pool is not enough'
    assert overfilled_pool == True, 'overfilled pool is not enough'
    assert underfilled_pool == False, 'underfilled pool is enough'
    assert empty_pool == False, 'empty pool is enough'


def test_fetch_foreing_key_pool(references_faker, instances_pool):
    foreing_key = references_faker._context.tables[2].columns['pointer']
    reference = foreing_key.reference[0]

    output = references_faker._fetch_foreing_key_pool(reference)

    assert output == instances_pool

def test_with_references_generate_data_pool(references_faker, instances_pool):
    foreing_key = references_faker._context.tables[2].columns['pointer']
    output = references_faker._generate_data_pool(foreing_key, 100)

    assert output == instances_pool


def test_init():
    table = Table("person","id")
    col_id = Column("id", "character varying")
    col_name = Column("name", "character varying")
    table.add_column(col_id)
    table.add_column(col_name)
    context = Context()
    context.add_table(table)

    faker = Faker(table, context)

    assert len(faker.column_data_pool) == 2
    assert len(faker.column_data_pool["id"]) == 100
    assert len(faker.column_data_pool["name"]) == 100
    assert faker._context == context
    assert table in faker._context.tables

def test_init_with_table_not_in_context():
    table = Table("person", "id")
    col_id = Column("id", "character varying")
    col_name = Column("name", "character varying")
    table.add_column(col_id)
    table.add_column(col_name)
    context = Context()
    
    with pytest.raises(exceptions.TableNotInContext):
        faker = Faker(table, context)
    

def test_generate_fake(faker, table):
    expected_output = ["surprise"]
    
    pool = set()
    pool.add(expected_output[0])
    column = Column("pk","character varying")
    table.add_column(column)
    faker.column_data_pool[column.name] = pool

    output = faker.generate_fake(table)

    assert output == expected_output

