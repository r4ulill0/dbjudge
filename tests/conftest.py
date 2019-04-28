import psycopg2
import pytest

@pytest.fixture(scope = "module")
def database_cursor():
    conn = psycopg2.connect(host="127.0.0.1",
        dbname="tfg_test", user="conexion", password="plsL3tM3in")
    cursor = conn.cursor()
    yield cursor
    
    cursor.close()
    conn.close()