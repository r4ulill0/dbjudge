import pytest
from dbjudge import squema_recollector
from dbjudge.questions.isolation import slicer
from dbjudge.questions.generation.constraints_truth_table import Truth_table
from dbjudge.questions.generation import generator


@pytest.fixture
def test_query():
    query = ("SELECT * "
             "FROM person p "
             "WHERE p.age > 20 and "
             "p.name not like 'juan' and "
             "NOT p.color like 'red' and "
             "p.adress<30000;")
    return query


@pytest.fixture
def query_slices():
    slices = [("SELECT * "
               "FROM person p "
               "WHERE p.age > 20 ;"),
              ("SELECT * "
               "FROM person p "
               "WHERE p.name not like 'juan' ;"
               ),
              ("SELECT * "
               "FROM person p "
               "WHERE NOT p.color like 'red' ;"
               ),
              ("SELECT * "
               "FROM person p "
               "WHERE p.adress<30000;"
               )]
    return slices


@pytest.fixture
def database_table_context(database_manager):
    def _database_table_context():
        db_cursor = database_manager.selected_db_connection.cursor()
        db_cursor.execute(
            open('tests/sql_files/questions_tests_database.sql').read())
        db_cursor.connection.commit()
        context = squema_recollector.create_context(
            database_manager.selected_db_connection)
        return context
    return _database_table_context


def test_slice_querie(test_query, query_slices):

    results = slicer.slice_sql(test_query)

    assert results == query_slices


def test_slice_mapping(test_query):
    slices = slicer.slice_sql(test_query)
    mapped_slices = slicer.map_slices(slices)
    expected_result = {
        'person': ["SELECT * FROM person p WHERE p.age > 20 ;",
                   "SELECT * FROM person p WHERE p.adress<30000;"]
    }
    assert mapped_slices == expected_result


def test_truth_table_creation():
    expected_truth_table_max_entries = 4
    expected_truth_table_entries = 4
    expected_truth_table_state_elements = 2
    row1 = (False, False)
    row2 = (False, True)
    row3 = (True, False)
    row4 = (True, True)
    repeated_row = (True, True)
    wrong_row = (True, False, True)
    mock_query_list = [None, None]
    table = Truth_table(mock_query_list)

    table.add(row1)
    table.add(row2)
    table.add(row3)
    before_complete = table.is_completed()
    table.add(row4)
    table.add(repeated_row)
    table.add(wrong_row)
    after_complete = table.is_completed()

    assert table.table_size == expected_truth_table_max_entries
    assert table.state_size == expected_truth_table_state_elements
    assert len(table.table) == expected_truth_table_entries
    assert wrong_row not in table.table
    assert not before_complete
    assert after_complete


def test_data_generation(database_table_context, query_slices, database_manager, make_database):
    database = 'test_data_gen'
    make_database(database)
    database_manager.select_database(database)
    context = database_table_context()
    table = context.get_table_by_name('person')
    generator.TIMEOUT_PER_QUERY = 1
    data = generator._generate_table_data(
        context, table, query_slices)

    assert len(data) > 0


def test_create_question(test_query, database_manager, make_database):
    database = 'create_question'
    question = '''Select all data about persons whose name is not "juan",
     whose favorite color differs from red and 
     whose postal adress is lesser than 30000'''
    make_database(database)
    database_manager.select_database(database)
    alternative_cursor = database_manager.selected_db_connection.cursor()
    alternative_cursor.execute(
        open('tests/sql_files/questions_tests_database.sql').read())
    alternative_cursor.connection.commit()
    generator.TIMEOUT_PER_QUERY = 1
    generator.create_question(database, test_query, question)

    assert_1_query = '''
        SELECT question, sql_query
        FROM dbjudge_questions;
    '''
    assert_2_query = '''
        SELECT *
        FROM person;
    '''
    main_cursor = database_manager.main_connection.cursor()
    main_cursor.execute(assert_1_query)
    results = main_cursor.fetchall()

    alternative_cursor = database_manager.selected_db_connection.cursor()
    alternative_cursor.execute(assert_2_query)
    results2 = alternative_cursor.fetchall()

    assert results[0][0] == question
    assert results[0][1] == test_query
    assert len(results2) > 0
