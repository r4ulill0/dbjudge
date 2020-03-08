import pytest
import datetime
import decimal

from dbjudge import type_compatible
from dbjudge import exceptions
from dbjudge.fake_data_gen import Faker
from dbjudge.structures.context import Context
from dbjudge.structures.table import Table
from dbjudge.structures.column import Column
from dbjudge.structures.reference import Reference
from dbjudge.structures.foreign_key import ForeignKey
from dbjudge.structures.fake_types import Custom
from dbjudge.structures.fake_types import Regex

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

def test_wrap_with_quote_marks(faker):
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

    output_2bytes = faker._gen_integer(2, None, None)
    output_bot_2bytes = faker._gen_integer(2, limit_2bytes[0], limit_2bytes[0])
    output_top_2bytes = faker._gen_integer(2, limit_2bytes[1], limit_2bytes[1])

    output_4bytes = faker._gen_integer(4, None, None)
    output_bot_4bytes = faker._gen_integer(4, limit_4bytes[0], limit_4bytes[0])
    output_top_4bytes = faker._gen_integer(4, limit_4bytes[1], limit_4bytes[1])

    assert isinstance(output_2bytes, int)
    assert isinstance(output_4bytes, int)
    assert (output_2bytes >= limit_2bytes[0]) and (output_2bytes <= limit_2bytes[1])
    assert (output_4bytes >= limit_4bytes[0]) and (output_4bytes <= limit_4bytes[1])
    assert output_bot_2bytes == limit_2bytes[0]
    assert output_bot_4bytes == limit_4bytes[0]
    assert output_top_2bytes == limit_2bytes[1]
    assert output_top_4bytes == limit_4bytes[1]
    
def test_gen_boolean(faker):
    output = faker._gen_boolean()
    assert isinstance(output, bool)

def test_gen_decimal(faker):
    top_value = decimal.Decimal('12.345')
    bot_value = decimal.Decimal('-39.499')
    output_top = faker._gen_decimal(3, top_value, top_value)
    output_bot = faker._gen_decimal(3, bot_value, bot_value)
    assert isinstance(output_top, decimal.Decimal)
    assert isinstance(output_bot, decimal.Decimal)
    assert output_top == top_value
    assert output_bot == bot_value

def test_gen_datetime(faker):
    output = faker._gen_datetime()

    assert isinstance(output, datetime.datetime)

def test_gen_interval(faker):
    output = faker._gen_interval()
    
    assert isinstance(output, datetime.timedelta)

def test_generate_fake_with_no_uniques_avaiable(faker):
    table = Table('uniques_table', ('unique_col',))
    column = Column('unique_col','character varying',unique=True)
    table.add_column(column)
    table.row_instances.append({column.name: 'default'})
    column.fake_type = Regex('extra_unique')
    faker.column_data_pool['unique_col'] = set()
    faker.column_data_pool['unique_col'].add('default')

    values = faker.generate_fake(table)

    assert values[0]== 'extra_unique'

def test_generate_fake_with_foreign_key(faker):
    check_value = 'check value'
    target = Table('target_table', ('target_id',))
    table = Table('table', ('id',))
    target_pk = Column('target_id','character varying', unique=True)
    id_col = Column('id', 'integer', unique=True)
    ref_col = Column('ref', 'character varying')
    
    ref_source = 'ref'
    ref_target = 'target_id'
    reference = Reference(ref_source,ref_target)
    ref_col.add_reference(reference)

    fkey = ForeignKey(table, target)
    fkey.add_column_reference(reference)

    target.add_column(target_pk)
    table.add_column(id_col)
    table.add_column(ref_col)
    table.foreign_keys.append(fkey)

    target.row_instances.append({target_pk.name:check_value})

    faker.column_data_pool[id_col.name] = set((check_value,))

    values = faker.generate_fake(table)

    assert values == [check_value,check_value]

def test_generate_fake(faker):
    supported_types = (type_compatible.ACCEPTED_STRING_DB_TYPES,
        type_compatible.ACCEPTED_INTEGER_DB_TYPES,
        type_compatible.ACCEPTED_BOOLEAN_DB_TYPES,
        type_compatible.ACCEPTED_FLOAT_DB_TYPES,
        type_compatible.ACCEPTED_DATE_DB_TYPES,
        type_compatible.ACCEPTED_INTERVAL_DB_TYPES)

    for supp_type in supported_types:
        for ctype in supp_type:
            column = Column("temp", ctype)
            output = faker._generate_fake(column)
            assert isinstance(output, str)

def test_generate_custom_fake(faker, load_csv_fakes, database_manager, reset_cache):
    col_regex = Column('regex','character varying')
    col_woman = Column('woman', 'character varying')
    regex_type = Regex('a')
    woman_type = Custom('woman_names')
    
    col_regex.fake_type = regex_type
    col_woman.fake_type = woman_type

    reset_cache(woman_type.custom_type)

    regex_result = faker._generate_fake(col_regex)
    woman_result = faker._generate_fake(col_woman)

    assert regex_result == 'a'
    assert woman_result == 'ZOILA ROCIO'

def test_invalid_column_type_generate_fake(faker):
    with pytest.raises(exceptions.InvalidColumnTypeError):
        column = Column('column', 'not supported yet')
        
        faker._generate_fake(column)
    
def test_default_generate_data_pool(faker):
    column = Column('column','character varying')
    size = 1000
    pool = faker._generate_data_pool(column,size)

    assert len(pool) == size

def test_generate_nullable_data_pool(faker):
    column = Column('column', 'character varying',nullable=True)
    size = 2
    pool = faker._generate_data_pool(column, size)

    assert len(pool) == size
    assert 'NULL' in pool

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
        Faker(table, context)
    

def test_generate_fake_from_pool(faker, table):
    expected_output = ["surprise"]
    
    pool = set()
    pool.add(expected_output[0])
    column = Column("pk","character varying")
    table.add_column(column)
    faker.column_data_pool[column.name] = pool

    output = faker.generate_fake(table)

    assert output == expected_output

def test_valid_primary_key(faker, table):
    pk_column_1 = Column('first_pk', 'integer')
    pk_column_2 = Column('second_pk', 'character')
    table.columns = [pk_column_1, pk_column_2]

    table.primary_key=('first_pk', 'second_pk')

    row_insert_1 = {'first_pk':1, 'second_pk':'a'}
    row_insert_2 = {'first_pk':5, 'second_pk':'b'}
    table.row_instances.append(row_insert_1)



    assert not faker._valid_primary_key(table, row_insert_1)
    assert faker._valid_primary_key(table, row_insert_2)

def test_has_pool_uniques(faker, table):
    column_case_1 = Column('A', 'integer',unique=True)
    column_case_2 = Column('B', 'character',unique=True)
    column_case_3 = Column('C', 'integer',unique=True)
    column_case_4 = Column('D', 'character varying', unique=True)
    
    pool_case_1 = set((0,-2,9))
    pool_case_2 = set(('3','i','k'))
    pool_case_3 = set((-129,0,2))
    pool_case_4 = set()

    faker.column_data_pool[column_case_1.name] = pool_case_1
    faker.column_data_pool[column_case_2.name] = pool_case_2
    faker.column_data_pool[column_case_3.name] = pool_case_3
    faker.column_data_pool[column_case_4.name] = pool_case_4

    instance_case_1 = {'A':0, 'B':'3', 'C':9, 'D':'some'}
    instance_case_2 = {'A':-2, 'B':'i', 'C':99, 'D':'someth'}
    instance_case_3 = {'A':9, 'B':'k', 'C':999, 'D':'something'}

    table.row_instances.append(instance_case_1)
    table.row_instances.append(instance_case_2)
    table.row_instances.append(instance_case_3)

    table.add_column(column_case_1)
    table.add_column(column_case_2)
    table.add_column(column_case_3)
    table.add_column(column_case_4)


    assert not faker._has_pool_uniques(table, column_case_1)
    assert not faker._has_pool_uniques(table, column_case_2)
    assert faker._has_pool_uniques(table, column_case_3)
    assert not faker._has_pool_uniques(table, column_case_4)

def test_exists_in_instance(faker, table):
    column = Column('pk','integer')
    table.add_column(column)

    repeated_number = 5
    unrepeated_number = 0

    row_instance = {'pk': repeated_number}
    table.row_instances.append(row_instance)


    assert faker._exists_in_instance(repeated_number, table, column)
    assert not faker._exists_in_instance(unrepeated_number, table, column)

def test_list_values(faker, table):
    column_1 = Column('pk','integer')
    column_2 = Column('c2','integer')
    column_3 = Column('c3','integer')
    column_4 = Column('c4','integer')

    table.add_column(column_1)
    table.add_column(column_2)
    table.add_column(column_3)
    table.add_column(column_4)

    unordered_values ={}
    unordered_values['c4'] = 4
    unordered_values['pk'] = 1
    unordered_values['c3'] = 3
    unordered_values['c2'] = 2

    output = faker._list_values(unordered_values, table)
    
    for idx, key in enumerate(table.columns.keys()):
        assert output[idx] == unordered_values[key]