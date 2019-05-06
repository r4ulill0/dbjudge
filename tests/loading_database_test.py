import pytest
import psycopg2
import conftest
import squemaGetter
from structures import Table, Column, Context

def test_load_tables(database_cursor):
    context = Context()
    
    squemaGetter._load_tables(context, database_cursor)
    table = context.tables

    assert len(context.tables) == 3
    assert 'persona' in table[0].name
    assert ('userid',) == table[0].primary_key
    assert 'libro' in table[1].name
    assert ('titulo', 'autor') == table[1].primary_key
    assert 'prestamo' in table[2].name
    assert ('titulo', 'autor', 'persona') == table[2].primary_key

def test_load_table_columns(database_cursor):
    table = Table('persona', ('userid',))

    squemaGetter._load_table_columns(table, database_cursor)

    column = table.columns
    assert column['userid'].name == 'userid'
    assert column['userid'].ctype == 'integer'
    assert column['nombre'].name == 'nombre'
    assert column['nombre'].ctype == 'character varying'
    assert column['dni'].name == 'dni'
    assert column['dni'].ctype == 'character varying'
    assert column['nacimiento'].name == 'nacimiento'
    assert column['nacimiento'].ctype == 'date'
    assert column['suspension'].name == 'suspension'
    assert column['suspension'].ctype == 'boolean'
    assert column['genero'].name == 'genero'
    assert column['genero'].ctype == 'character varying'

def test_load_columns_references(database_cursor):
    context = Context()
    squemaGetter._load_tables(context,database_cursor)
    for table in context.tables:
        squemaGetter._load_table_columns(table, database_cursor)

    squemaGetter._load_columns_references(context, database_cursor)

    referencing_table = context.tables[2]
    referencing_column_1 = referencing_table.columns['titulo']
    referencing_column_2 = referencing_table.columns['autor']
    referencing_column_3 = referencing_table.columns['persona']

    assert referencing_column_1.reference[0] == ('libro','titulo')
    assert referencing_column_2.reference[0] == ('libro','autor')
    assert referencing_column_3.reference[0] == ('persona','userid')

def test_format_primary_key():
    simulated_query_response = [('data_1',),('data_2',)]

    formated_data = squemaGetter._format_primary_key(simulated_query_response)

    assert formated_data == ('data_1', 'data_2')