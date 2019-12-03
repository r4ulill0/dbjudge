import pytest
from dbjudge.connection_manager.manager import Manager
from dbjudge.questions.isolation import slicer
from dbjudge.questions.isolation import table_isolator


def test_slice_querie():
    test_query = ("SELECT * "
                  "FROM person p "
                  "WHERE p.age > 20 and "
                  "p.name not like 'juan' and "
                  "p.color NOT red and "
                  "p.adress<30000;")
    expected_results = [
        ("SELECT * "
         "FROM person p "
            "WHERE p.age > 20 ;"),
        ("SELECT * "
            "FROM person p "
            "WHERE p.name not like 'juan' ;"
         ),
        ("SELECT * "
         "FROM person p "
         "WHERE p.color NOT red ;"
         ),
        ("SELECT * "
         "FROM person p "
         "WHERE p.adress<30000;"
         )
    ]

    results = slicer.slice_sql(test_query)

    assert results == expected_results


def test_table_isolation(database_manager, make_database):
    db_name = 'isolation_test'
    make_database(db_name)
    database_manager.select_database(db_name)

    table_name = 'dummy'
    ddl = '''
        CREATE TABLE dummy(
            id INT PRIMARY KEY,
            age INT CONSTRAINT legal_age CHECK (age > 18)
        );
    '''
    database_manager.singleton_instance.execute_sql(ddl)
    database_manager.singleton_instance.selected_db_connection.commit()

    table_isolator.isolate(db_name, table_name)
    insert_template = 'INSERT INTO dbjudge_isolation(id, age) VALUES (%s, %s)'
    valid_values = (1, 23)
    invalid_values = (2, 1)

    writer = database_manager.selected_db_connection.cursor()
    writer.execute(insert_template, valid_values)
    database_manager.selected_db_connection.commit()
    try:
        writer.execute(insert_template, invalid_values)
        database_manager.selected_db_connection.commit()
    except:
        database_manager.selected_db_connection.rollback()

    query = 'SELECT * FROM dbjudge_isolation;'
    writer.execute(query)
    results = writer.fetchall()

    expected_result = 1

    assert len(results) == expected_result
