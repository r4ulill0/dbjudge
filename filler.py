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
    query_template = "INSERT INTO {} ({}) VALUES (%s);"

    columns_names_list = format_columns_names(table.columns)

    for _ in range(table.fake_data_size):
        values_list = faker.generate_fake(table)

        insert_query = sql.SQL(query_template).format(
            sql.Identifier(table.name),
            sql.Identifier(columns_names_list)
        )
        db_cursor.execute(insert_query, values_list)


def format_columns_names(columns):
    result = ""
    for idx, key in enumerate(columns):
        name = columns[key].name
        if (idx == 0):
            result += name
        else:
            result += ", " + name

    return result
