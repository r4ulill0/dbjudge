import os
import time
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

    pending_inserts = table.fake_data_size
    while pending_inserts > 0:
        time.sleep(0.01)  # Avoid hogging the CPU
        values_list = faker.generate_fake(table)
        insert_success = Manager.singleton_instance.custom_insert(
            table.name, table.columns.keys(), values_list, db_cursor)
        if insert_success:
            pending_inserts -= 1
        else:
            table.row_instances.pop()
