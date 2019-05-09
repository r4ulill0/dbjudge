import os
import psycopg2
from structures import Table, Column, Context
import queries


def create_context(conn):
    
    database_cursor = conn.cursor()
    context = Context()

    _load_tables(context, database_cursor)

    for table in context.tables:
        _load_table_columns(table, database_cursor)

    _load_columns_references(context, database_cursor)

    database_cursor.close()
    return context


def _load_tables(context, database_cursor):
    database_cursor.execute(queries.TABLES_QUERY)
    tables = database_cursor.fetchall()

    for i in tables:
        database_cursor.execute(queries.PRIMARY_KEY_QUERY,(i[0],))
        primary_key = _format_primary_key(database_cursor.fetchall())
        new_table = Table(i[0],primary_key)
        context.add_table(new_table)

def _format_primary_key(raw_query_response):
    pk_list = []
    for element in raw_query_response:
        pk_list.append(element[0])
    pk_formatted = tuple(pk_list)
    return pk_formatted

def _load_table_columns(table, database_cursor):
    database_cursor.execute(queries.COLUMN_TYPE_QUERY,(table.name,))
    columns_types = database_cursor.fetchall()
    uniques = _load_table_uniques(table, database_cursor)
    
    for column_and_type in columns_types:
        column_name = column_and_type[0]
        column_type = column_and_type[1]
        column_nullable = column_and_type[2] is 'yes'
        column_char_len = column_and_type[3]
        column_unique = column_name in uniques
        new_column = Column(column_name,column_type,column_nullable, column_unique)
        
        if (column_char_len != 'NULL'):
            new_column.max_char_len = column_char_len

        table.add_column(new_column)

def _load_table_uniques(table, database_cursor):
    database_cursor.execute(queries.UNIQUE_KEY_QUERY,(table.name,))
    query_result =database_cursor.fetchall() 
    uniques = set()
    for result in query_result:
        uniques.add(result[0])
    
    return uniques

def _load_columns_references(context, database_cursor):
    for table in context.tables:
        for key, column in table.columns.items():
            database_cursor.execute(queries.REFERENCE_QUERY,(table.name,column.name))
            refq = database_cursor.fetchall()
            reference = None
            if (len(refq) == 1):
                target_table = refq[0][4]
                target_column = refq[0][5]
                reference = (target_table,target_column)
            column.add_reference(reference)