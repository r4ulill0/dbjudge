import psycopg2
import pytest


@pytest.fixture(scope="module")
def database_connection():
    conn = psycopg2.connect(host="127.0.0.1",
                            dbname="tfg_test", user="conexion", password="plsL3tM3in")
    yield conn

    conn.close()


@pytest.fixture(scope="module")
def database_cursor(database_connection):
    cursor = database_connection.cursor()
    yield cursor

    cursor.close()
