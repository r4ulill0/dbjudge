from collections import Counter
from copy import deepcopy

import psycopg2
import pytest

from dbjudge.exceptions import DuplicatedDatabaseError
from dbjudge.exceptions import MissingDatabaseError
from dbjudge.connection_manager.manager import Manager


def test_installation(database_manager):
    installed_after = database_manager._is_installed()

    assert(installed_after)


def test_instantiation_after_install(database_manager):
    db_name = database_manager.main_connection.info.dbname
    second_instance = Manager.__new__(Manager)
    Manager.__init__(second_instance,
                     user=database_manager.username,
                     password=database_manager.password,
                     host=database_manager.host,
                     database_name=db_name)

    assert(second_instance._is_installed())


def test_already_created_manager(database_manager):
    new_manager = Manager(
        user=database_manager.username,
        password=database_manager.password,
        host=database_manager.host,
        database_name=database_manager.main_connection.info.dbname
    )
    assert(new_manager == database_manager)


def test_singleton(database_manager):

    instance1 = database_manager
    instance2 = Manager.singleton_instance

    assert(isinstance(instance1, Manager))
    assert(isinstance(instance2, Manager))


def test_delete_manager(database_manager):
    manager_copy = deepcopy(database_manager)
    manager_copy.__del__()

    assert(manager_copy.main_connection.closed != 0)


def test_delete_manager_with_selection(database_manager, make_database):
    selected_db_name = 'delete_manager_test'
    make_database(selected_db_name)
    database_manager.select_database(selected_db_name)

    manager_copy = deepcopy(database_manager)
    manager_copy.__del__()

    assert(manager_copy.main_connection.closed != 0)
    assert(manager_copy.selected_db_connection != 0)


def test_db_create(database_manager, make_database):
    db_name = 'db_creation_test'
    before_creation = len(database_manager.get_databases())
    make_database(db_name)
    after_creation = len(database_manager.get_databases())

    assert(after_creation > before_creation)
    assert(db_name in database_manager.get_databases())


def test_db_create_duplicated(database_manager, make_database):
    with pytest.raises(DuplicatedDatabaseError):
        make_database('duplicated_table')

        make_database('duplicated_table')


def test_db_delete(database_manager, make_database):
    db_target_name = 'db_delete_test'
    database_manager.create_database(db_target_name)

    before_creation = len(database_manager.get_databases())
    database_manager.delete_database(db_target_name)
    after_creation = len(database_manager.get_databases())

    assert(before_creation > after_creation)
    assert(db_target_name not in database_manager.get_databases())


def test_db_delete_nonexistent(database_manager):
    with pytest.raises(MissingDatabaseError):
        database_manager.delete_database('nonexistent_db')


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


def test_select_database(database_manager, make_database):
    db_name1 = 'selection_test'
    db_name2 = 'selection_test2'
    make_database(db_name1)
    make_database(db_name2)

    database_manager.select_database(db_name1)
    result_name1 = database_manager.selected_db_connection.info.dbname
    database_manager.select_database(db_name2)
    result_name2 = database_manager.selected_db_connection.info.dbname

    assert(result_name1 == db_name1)
    assert(result_name2 == db_name2)


def test_selected_database_execution(database_manager, make_database):
    db_name = 'selection_exec_test'
    make_database(db_name)
    sql = 'CREATE TABLE test_exec(test integer)'
    database_manager.select_database(db_name)
    database_manager.execute_sql(sql)


def test_select_nonexistent_database(database_manager):
    with pytest.raises(MissingDatabaseError):
        database_manager.select_database('nonexistent_db')


def test_get_fake_types(database_manager, load_csv_fakes):

    expected = (('woman_names',), ('man_names',), ('surnames',))
    result = database_manager.get_fake_types()

    assert(Counter(result) == Counter(expected))


def test_custom_insert_without_cursor(database_manager, make_database):
    name = 'test_insert_nocursor'
    make_database(name)
    sql = 'CREATE TABLE {} (test integer);'.format(name)
    database_manager.select_database(name)
    database_manager.execute_sql(sql)

    database_manager.custom_insert(name, ('test',), (1,))
    proof_sql = 'select test from {} where test=1;'.format(name)
    database_manager.selected_db_connection.commit()

    result = database_manager.execute_in_readonly(proof_sql)

    assert len(result) == 1


def test_get_questions(database_manager, make_database):
    db_name = 'test_get_questions'
    make_database(db_name)
    database_manager.select_database(db_name)
    q1 = 'some question'
    q2 = 'another one'
    q3 = 'num3r1c question'
    a1 = 'an answer'
    a2 = 'another answer'
    a3 = 'answer with numbers'

    database_manager.register_question(q1, a1, db_name)
    database_manager.register_question(q2, a2, db_name)
    database_manager.register_question(q3, a3, db_name)

    result1 = database_manager.get_questions()
    result2 = database_manager.get_questions(db_name)
    expected_result = [(q1,), (q2,), (q3,)]

    assert expected_result[0] in result1
    assert expected_result[1] in result1
    assert expected_result[2] in result1
    assert expected_result[0] in result2
    assert expected_result[1] in result2
    assert expected_result[2] in result2


def test_get_tables(database_manager, make_database):
    db_name = 'test_get_tables'
    make_database(db_name)
    database_manager.select_database(db_name)
    table1 = 'test_get_tables_1'
    table2 = 'test_get_tables_2'
    table3 = 'test_get_tables_3'
    sql1 = 'CREATE TABLE {} (test integer);'.format(table1)
    sql2 = 'CREATE TABLE {} (test integer);'.format(table2)
    sql3 = 'CREATE TABLE {} (test integer);'.format(table3)
    database_manager.execute_sql(sql1)
    database_manager.execute_sql(sql2)
    database_manager.execute_sql(sql3)
    database_manager.selected_db_connection.commit()

    result = database_manager.get_tables()

    assert table1 in result
    assert table2 in result
    assert table3 in result
    assert len(result) == 3


def test_get_total_data_count(database_manager, make_database):
    db_name = 'test_data_count'
    make_database(db_name)
    database_manager.select_database(db_name)
    table1 = 'test_get_data_count_1'
    table2 = 'test_get_data_count_2'
    table3 = 'test_get_data_count_3'
    sql1 = 'CREATE TABLE {} (test integer);'.format(table1)
    sql2 = 'CREATE TABLE {} (test integer);'.format(table2)
    sql3 = 'CREATE TABLE {} (test integer);'.format(table3)
    data1 = 'INSERT INTO {} (test) VALUES (1);'.format(table1)
    data2 = 'INSERT INTO {} (test) VALUES (1);'.format(table2)
    data3 = 'INSERT INTO {} (test) VALUES (2);'.format(table2)
    data4 = 'INSERT INTO {} (test) VALUES (1);'.format(table3)
    data5 = 'INSERT INTO {} (test) VALUES (2);'.format(table3)
    data6 = 'INSERT INTO {} (test) VALUES (3);'.format(table3)
    database_manager.execute_sql(sql1)
    database_manager.execute_sql(sql2)
    database_manager.execute_sql(sql3)
    database_manager.execute_sql(data1)
    database_manager.execute_sql(data2)
    database_manager.execute_sql(data3)
    database_manager.execute_sql(data4)
    database_manager.execute_sql(data5)
    database_manager.execute_sql(data6)
    database_manager.selected_db_connection.commit()
    sql1 = 'ANALYZE {};'.format(table1)
    sql2 = 'ANALYZE {};'.format(table2)
    sql3 = 'ANALYZE {};'.format(table3)
    database_manager.execute_sql(sql1)
    database_manager.execute_sql(sql2)
    database_manager.execute_sql(sql3)
    database_manager.selected_db_connection.commit()

    result = database_manager.get_total_data_count()

    assert result == 6
