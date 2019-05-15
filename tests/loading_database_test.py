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

    persona_reference = referencing_table.foreign_keys[0].get_column_references()[0]
    titulo_reference = referencing_table.foreign_keys[1].get_column_references()[0]
    autor_reference = referencing_table.foreign_keys[1].get_column_references()[1]
    
    assert referencing_table.foreign_keys[0].source_table.name == 'prestamo'
    assert referencing_table.foreign_keys[0].target_table.name == 'persona'
    assert persona_reference.source == 'persona'
    assert persona_reference.target == 'userid'

    assert referencing_table.foreign_keys[1].source_table.name == 'prestamo'
    assert referencing_table.foreign_keys[1].target_table.name == 'libro'
    assert titulo_reference.source == 'titulo'
    assert titulo_reference.target == 'titulo'
    assert autor_reference.source == 'autor'
    assert autor_reference.target == 'autor'

def test_format_primary_key():
    simulated_query_response = [('data_1',),('data_2',)]

    formated_data = squemaGetter._format_primary_key(simulated_query_response)

    assert formated_data == ('data_1', 'data_2')