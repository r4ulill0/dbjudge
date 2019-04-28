import os
import psycopg2
from structures import Table, Column, Context
import fake_data_gen

def generate_fake_data(context, db_connection):
    db_cursor = db_connection.cursor()

    for table in context.tables:
        _fill_table(table, db_cursor)

    db_cursor.close()


def _fill_table(table, db_cursor):
    insert_query = "INSERT INTO {0} ({1}) VALUES ({2});"

    columns_names_list = format_columns_names(table.columns)
    faker = fake_data_gen.Faker(table)

    for _ in range(table.fake_data_size):
        values_list = generate_formatted_fake_values(table.columns, faker)

        print(insert_query.format(table.name,columns_names_list, values_list))
        #db_cursor.execute(insert_query,(table.name,columns_names_list, values_list))

def format_columns_names(columns):
    result = ""
    for idx, column in enumerate(columns):
        if (idx == 0):
            result += column.name
        else:
            result += ", "+column.name
    
    return result

def generate_formatted_fake_values(columns, faker):
    values = ""
    for idx, column in enumerate(columns):
        value = str(faker.generate_fake(column))
        if (idx == 0):
            values += value
        else:
            values += ","+value
    
    return values