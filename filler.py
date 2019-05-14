import os
import psycopg2
from structures import Table, Column, Context
import fake_data_gen

def generate_fake_data(context, db_connection):
    db_cursor = db_connection.cursor()

    for table in context.tables:
        faker = fake_data_gen.Faker(table, context)
        _fill_table(table, faker, db_cursor)

    db_cursor.close()


def _fill_table(table, faker, db_cursor):
    query_template = "INSERT INTO {0} ({1}) VALUES ({2});"

    columns_names_list = format_columns_names(table.columns)

    for _ in range(table.fake_data_size):
        values_list = faker.generate_fake(table)
        formatted_values_list = format_fake_values(values_list)
        
        insert_query = query_template.format(table.name,columns_names_list, formatted_values_list)
        print(insert_query)
        db_cursor.execute(insert_query)

def format_columns_names(columns):
    result = ""
    for idx, key in enumerate(columns):
        name = columns[key].name
        if (idx == 0):
            result += name
        else:
            result += ", " + name
    
    return result

def format_fake_values(values):
    formatted_values = []
    for value in values:
        formatted_values.append(str(value))

    formatted_result = ','.join(formatted_values)

    return formatted_result