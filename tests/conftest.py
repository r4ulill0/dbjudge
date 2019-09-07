import psycopg2
import pytest
from connection_manager.manager import Manager


@pytest.fixture(scope="session")
def database_connection():
    conn = psycopg2.connect(host="127.0.0.1",
                            dbname="tfg_test", user="conexion", password="plsL3tM3in")
    writer = conn.cursor()
    writer.execute(open('tests/sql_files/exampleDatabase.sql').read())
    writer.close()
    conn.commit()
    yield conn

    conn.close()


@pytest.fixture(scope="session")
def database_manager():
    manager = Manager(user='conexion', password='plsL3tM3in',
                      host='127.0.0.1', database_name='tfg_test')
    yield manager
    writer = manager.main_connection.cursor()
    writer.execute(open('tests/sql_files/dbjudge_tables_dropper.sql').read())
    writer.close()
    manager.main_connection.commit()
    del manager


@pytest.fixture(scope="session")
def database_cursor(database_connection):
    cursor = database_connection.cursor()
    yield cursor

    cursor.close()


@pytest.fixture(scope="module")
def cleandb(database_connection):
    cursor = database_connection.cursor()
    cursor.execute(open("tests/sql_files/cleandb.sql").read())
    cursor.close()
    database_connection.commit()
    database_connection.close()
