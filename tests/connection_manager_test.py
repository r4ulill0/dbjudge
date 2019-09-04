import psycopg2
import pytest

from connection_manager.manager import Manager


@pytest.fixture
def make_database(manager):
    created_dbs = []
    
    # factory for database creation in tests
    def _make_database(name):
        manager.create_database(name)
        created_dbs.append(name)

    yield _make_database

    for db in created_dbs:
        manager.delete_database(db)


@pytest.fixture(scope='module')
def manager():
    manager = Manager(user="conexion", password="plsL3tM3in",
                      host="127.0.0.1", database_name="tfg_test")
    yield manager
    writer = manager.main_connection.cursor()
    writer.execute(open('tests/sql_files/dbjudge_tables_dropper.sql').read())
    writer.close()
    manager.main_connection.commit()
    del manager


def test_installation(manager):
    installed_after = manager._is_installed()

    assert(installed_after)


def test_singleton(manager):

    instance1 = manager
    instance2 = Manager._singleton_instance

    assert(isinstance(instance1, Manager))
    assert(isinstance(instance2, Manager))


def test_db_create(manager, make_database):
    db_name = 'db_creation_test'
    before_creation = len(manager.show_databases())
    make_database(db_name)
    after_creation = len(manager.show_databases())

    assert(after_creation > before_creation)
    assert(db_name in manager.show_databases())


def test_db_delete(manager, make_database):
    db_target_name = 'db_delete_test'
    manager.create_database(db_target_name)

    before_creation = len(manager.show_databases())
    manager.delete_database(db_target_name)
    after_creation = len(manager.show_databases())

    assert(before_creation > after_creation)
    assert(db_target_name not in manager.show_databases())


def test_db_show(make_database, manager):
    db_name1 = 'db_show_test1'
    db_name2 = 'db_show_test2'
    db_name3 = 'db_show_test3'

    make_database(db_name1)
    make_database(db_name2)
    make_database(db_name3)

    databases = manager.show_databases()

    assert(db_name1 in databases)
    assert(db_name2 in databases)
    assert(db_name3 in databases)
    assert(len(databases) == 3)
