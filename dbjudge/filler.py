import os
import psycopg2
from psycopg2 import sql

from dbjudge.structures.context import Context
from dbjudge.structures.table import Table
from dbjudge.structures.column import Column
from dbjudge import fake_data_gen
from dbjudge.connection_manager.manager import Manager


def generate_fake_data(context, db_connection):
    db_cursor = db_connection.cursor()

    for table in context.tables:
        faker = fake_data_gen.Faker(table, context)
        _fill_table(table, faker, db_cursor)

    db_connection.commit()
    db_cursor.close()


def _fill_table(table, faker, db_cursor):

    for _ in range(table.fake_data_size):
        values_list = faker.generate_fake(table)
        Manager.singleton_instance.custom_insert(
            table.name, table.columns.keys(), values_list, db_cursor)
