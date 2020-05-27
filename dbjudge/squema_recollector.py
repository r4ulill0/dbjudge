"""Tools to create a Context from a created database.

This module analyze the tables and columns from a database
and stores a basic structure of the database model in a Context object.
"""
from psycopg2 import sql

from dbjudge.connection_manager.manager import Manager
from dbjudge.structures.context import Context
from dbjudge.structures.table import Table
from dbjudge.structures.column import Column
from dbjudge.structures.foreign_key import ForeignKey
from dbjudge.structures.reference import Reference
from dbjudge.utils import queries

COLUMN_NULLABLE_POSITIVE_RESPONSE = 'yes'


def create_context(conn):
    """Creates a context with the basic information about a database relational model.

    :param conn: Target database connection.
    :return: Database context.
    """
    database_cursor = conn.cursor()
    context = Context()
    _load_tables(context, database_cursor)

    for table in context.tables:
        _load_table_columns(table, database_cursor)

    _load_columns_references(context, database_cursor)

    update_context_instances(context, cursor=database_cursor)

    database_cursor.close()
    return context


def _load_tables(context, database_cursor):
    database_cursor.execute(queries.TABLES_QUERY)
    tables = database_cursor.fetchall()

    for i in tables:
        database_cursor.execute(queries.PRIMARY_KEY_QUERY, (i[0],))
        primary_key = _format_primary_key(database_cursor.fetchall())
        new_table = Table(i[0], primary_key)
        context.add_table(new_table)


def _format_primary_key(raw_query_response):
    pk_list = []
    for element in raw_query_response:
        pk_list.append(element[0])
    pk_formatted = tuple(pk_list)
    return pk_formatted


def _load_table_columns(table, database_cursor):
    database_cursor.execute(queries.COLUMN_TYPE_QUERY, (table.name,))
    columns_types = database_cursor.fetchall()
    uniques = _load_table_uniques(table, database_cursor)

    for column_and_type in columns_types:
        column_name = column_and_type[0]
        column_type = column_and_type[1]
        column_nullable = column_and_type[2] is COLUMN_NULLABLE_POSITIVE_RESPONSE
        column_char_len = column_and_type[3]
        column_unique = column_name in uniques
        new_column = Column(column_name, column_type,
                            column_nullable, column_unique)

        if column_char_len:
            new_column.max_char_len = column_char_len

        table.add_column(new_column)


def _load_table_uniques(table, database_cursor):
    database_cursor.execute(queries.UNIQUE_KEY_QUERY, (table.name,))
    query_result = database_cursor.fetchall()
    uniques = set()
    for result in query_result:
        uniques.add(result[0])

    return uniques


def _load_columns_references(context, database_cursor):

    for table in context.tables:
        database_cursor.execute(queries.REFERENCE_QUERY, (table.name,))
        references = database_cursor.fetchall()
        if not references:
            continue

        last_key = ''
        for reference in references:
            key = reference[0]
            source_table_name = reference[1]
            source_column_name = reference[2]
            target_table_name = reference[4]
            target_column_name = reference[5]

            source_table = context.get_table_by_name(source_table_name)
            target_table = context.get_table_by_name(target_table_name)

            if key != last_key:
                foreign_key = ForeignKey(source_table, target_table)
                table.foreign_keys.append(foreign_key)

            reference = Reference(source_column_name, target_column_name)
            foreign_key.add_column_reference(reference)

            last_key = key


def update_context_instances(context, cursor=None):
    """Updates a context with the most recent rows found.

    :param context: Target database context.
    :param cursor: Database connection cursor,
        defaults to the selected database on the connection manager.
    """
    if not cursor:
        cursor = Manager.singleton_instance.selected_db_connection.cursor()
    for table in context.tables:
        for col_name, column in table.columns.items():
            transaction = sql.SQL(queries.COLUMN_INSTANCES).format(
                sql.Identifier(col_name),
                sql.Identifier(table.name)
            )
            cursor.execute(transaction)
            instances = cursor.fetchall()
            cursor.connection.commit()
            for instance in instances:
                column.column_instances.append(instance)
