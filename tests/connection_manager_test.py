import psycopg2
import pytest

from connection_manager.manager import Manager


@pytest.fixture
def make_database(database_manager):
    created_dbs = []

    # factory for database creation in tests
    def _make_database(name):
        database_manager.create_database(name)
        created_dbs.append(name)

    yield _make_database

    for db in created_dbs:
        database_manager.delete_database(db)


def test_installation(database_manager):
    installed_after = database_manager._is_installed()

    assert(installed_after)


def test_singleton(database_manager):

    instance1 = database_manager
    instance2 = Manager.singleton_instance

    assert(isinstance(instance1, Manager))
    assert(isinstance(instance2, Manager))


def test_db_create(database_manager, make_database):
    db_name = 'db_creation_test'
    before_creation = len(database_manager.get_databases())
    make_database(db_name)
    after_creation = len(database_manager.get_databases())

    assert(after_creation > before_creation)
    assert(db_name in database_manager.get_databases())


def test_db_delete(database_manager, make_database):
    db_target_name = 'db_delete_test'
    database_manager.create_database(db_target_name)

    before_creation = len(database_manager.get_databases())
    database_manager.delete_database(db_target_name)
    after_creation = len(database_manager.get_databases())

    assert(before_creation > after_creation)
    assert(db_target_name not in database_manager.get_databases())


def test_db_show(make_database, database_manager):
    db_name1 = 'db_show_test1'
    db_name2 = 'db_show_test2'
    db_name3 = 'db_show_test3'

    make_database(db_name1)
    make_database(db_name2)
    make_database(db_name3)

    databases = database_manager.get_databases()

    assert(db_name1 in databases)
    assert(db_name2 in databases)
    assert(db_name3 in databases)
    assert(len(databases) == 3)
