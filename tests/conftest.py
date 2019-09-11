import psycopg2
import pytest
from connection_manager.manager import Manager
from custom_fakes import custom_loader
from custom_fakes.custom_generator import Custom_cache


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


@pytest.fixture(scope='session')
def load_csv_fakes(database_manager):
    file_paths = []
    names = []
    file_paths.append('tests/csv_files/woman_names.csv')
    names.append('woman_names')
    file_paths.append('tests/csv_files/man_names.csv')
    names.append('man_names')
    file_paths.append('tests/csv_files/surnames.csv')
    names.append('surnames')
    for file_path, name in zip(file_paths, names):
        results = []
        results = custom_loader.load_csv_fakes(file_path)
        custom_loader.save_to_database(results, (0,), (name,))


@pytest.fixture
def reset_cache():
    def _reset_cache(fake_type):
        if (not hasattr(Custom_cache, 'singleton_instance')):
            Custom_cache(fake_type)
        else:
            Custom_cache.singleton_instance.fake_type = fake_type
            Custom_cache.singleton_instance._update_data()
    return _reset_cache
