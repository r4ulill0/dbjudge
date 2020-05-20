import pytest

from dbjudge import filler
from dbjudge.structures.context import Context
from dbjudge.structures.table import Table
from dbjudge.structures.column import Column
from dbjudge.fake_data_gen import Faker


def test_generate_fake_data(database_connection, db_empty_table, database_manager):

    context = Context()
    mock_table = db_empty_table('test_gen_fake_data')
    context.add_table(mock_table)

    filler.generate_fake_data(context, database_connection)


def test_fill_table(db_empty_table, database_cursor, database_manager):

    table = db_empty_table('filler_test')
    table.fake_data_size = 3

    context = Context()
    context.add_table(table)
    faker = Faker(table, context, pool_size=3)
    faker.column_data_pool['id'].clear()
    faker.column_data_pool['id'].add('one')
    faker.column_data_pool['id'].add('alpha')
    faker.column_data_pool['id'].add('gamma')

    db_cursor = database_cursor

    filler._fill_table(table, faker, db_cursor)

    db_cursor.connection.commit()

    result_query = 'SELECT * FROM filler_test ORDER BY id;'
    db_cursor.execute(result_query)
    results = db_cursor.fetchall()

    expected = [('alpha',), ('gamma',), ('one',)]

    assert(results == expected)
