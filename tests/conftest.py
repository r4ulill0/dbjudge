import psycopg2
import pytest

from dbjudge.connection_manager.manager import Manager
from dbjudge.custom_fakes import custom_loader
from dbjudge.custom_fakes.custom_generator import Custom_cache
from dbjudge.structures.table import Table
from dbjudge.structures.column import Column

EXAMPLE_DATABASE_FILE = 'tests/sql_files/exampleDatabase.sql'
DROP_EXAMPLE_DATABASE_FILE = 'tests/sql_files/dbjudge_tables_dropper.sql'


@pytest.fixture(scope="session")
def database_connection():
    conn = psycopg2.connect(host="127.0.0.1",
                            dbname="tfg_test", user="conexion", password="plsL3tM3in")
    writer = conn.cursor()
    writer.execute(open(EXAMPLE_DATABASE_FILE).read())
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
    writer.execute(open(DROP_EXAMPLE_DATABASE_FILE).read())
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


@pytest.fixture
def make_database(database_manager):
    created_dbs = []

    # factory for database creation in tests
    def _make_database(name):
        database_manager.create_database(name)
        created_dbs.append(name)

    yield _make_database

    if (database_manager.selected_db_connection != None):
        database_manager.selected_db_connection.close()
        database_manager.selected_db_connection = None

    for db in reversed(created_dbs):
        database_manager.delete_database(db)


@pytest.fixture
def reset_main_db(database_manager):
    writer = database_manager.main_connection.cursor()
    writer.execute(open(DROP_EXAMPLE_DATABASE_FILE).read())
    database_manager.main_connection.commit()
    writer.execute(open(EXAMPLE_DATABASE_FILE).read())
    database_manager.main_connection.commit()
    writer.close()


@pytest.fixture
def db_empty_table(database_connection):
    created_tables = []

    writer = database_connection.cursor()

    def _create_table(name):
        table = Table(name, ('id',))
        column = Column('id', 'character varying', unique=True)
        table.add_column(column)

        query = 'CREATE TABLE {}(id varchar, PRIMARY KEY (id));'.format(name)
        writer.execute(query)
        database_connection.commit()
        created_tables.append(name)
        return table

    yield _create_table

    for name in reversed(created_tables):
        database_connection.commit()
        database_connection.autocommit = True
        cleaning_query = psycopg2.sql.SQL('DROP TABLE IF EXISTS {};').format(
            psycopg2.sql.Identifier(name)
        )
        writer.execute(cleaning_query)
        database_connection.autocommit = False
    writer.close()
