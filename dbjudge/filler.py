import os
import psycopg2
from psycopg2 import sql
from structures.context import Context
from structures.table import Table
from structures.column import Column
import fake_data_gen


def generate_fake_data(context, db_connection):
    db_cursor = db_connection.cursor()

    for table in context.tables:
        faker = fake_data_gen.Faker(table, context)
        _fill_table(table, faker, db_cursor)

    db_cursor.close()


def _fill_table(table, faker, db_cursor):
    query_template = "INSERT INTO {} ({}) VALUES ({});"

    for _ in range(table.fake_data_size):
        values_list = faker.generate_fake(table)

        insert_query = sql.SQL(query_template).format(
            sql.Identifier(table.name),
            sql.SQL(',').join(map(sql.Identifier, table.columns.keys())),
            sql.SQL(',').join(sql.Placeholder() * len(values_list))
        )
        db_cursor.execute(insert_query, values_list)
