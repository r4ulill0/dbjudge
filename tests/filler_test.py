import pytest
import conftest

from dbjudge import filler
from dbjudge.structures.context import Context
from dbjudge.structures.table import Table
from dbjudge.structures.column import Column
from dbjudge.fake_data_gen import Faker

import datetime


@pytest.fixture
def db_empty_table(database_connection):
    writer = database_connection.cursor()

    table = Table('filler_test', ('id',))
    column = Column('id', 'character varying', unique=True)
    table.add_column(column)

    query = 'CREATE TABLE filler_test(id varchar, PRIMARY KEY (id));'
    writer.execute(query)
    database_connection.commit()

    yield table

    cleaning_query = 'DROP TABLE filler_test;'
    writer.execute(cleaning_query)
    writer.close()
    database_connection.commit()


def test_generate_fake_data(database_connection, db_empty_table, database_manager):

    context = Context()
    context.add_table(db_empty_table)

    filler.generate_fake_data(context, database_connection)


def test_fill_table(db_empty_table, database_cursor, database_manager):

    db_empty_table.fake_data_size = 3

    context = Context()
    context.add_table(db_empty_table)
    faker = Faker(db_empty_table, context, pool_size=3)
    faker.column_data_pool['id'].clear()
    faker.column_data_pool['id'].add('one')
    faker.column_data_pool['id'].add('alpha')
    faker.column_data_pool['id'].add('gamma')

    db_cursor = database_cursor

    filler._fill_table(db_empty_table, faker, db_cursor)

    db_cursor.connection.commit()

    result_query = 'SELECT * FROM filler_test ORDER BY id;'
    db_cursor.execute(result_query)
    results = db_cursor.fetchall()

    expected = [('alpha',), ('gamma',), ('one',)]

    assert(results == expected)
