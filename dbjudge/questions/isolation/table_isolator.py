from dbjudge.connection_manager.manager import Manager
from dbjudge.utils import queries
from psycopg2 import sql


def isolate(database, table_name):
    # TODO Try to reserve the table name
    isolation_name = "dbjudge_isolation"

    Manager.singleton_instance.select_database(database)

    data_definition = sql.SQL(queries.COPY_TABLE).format(
        sql.Identifier(isolation_name),
        sql.Identifier(isolation_name),
        sql.Identifier(table_name)
    )
    writer = Manager.singleton_instance.selected_db_connection.cursor()
    writer.execute(data_definition)

    writer.close()
