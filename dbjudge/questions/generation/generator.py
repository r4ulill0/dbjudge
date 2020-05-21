"""Question generation module."""
import time
from dbjudge.connection_manager.manager import Manager
from dbjudge.fake_data_gen import Faker
from dbjudge.questions.isolation import slicer
from dbjudge.questions.generation.constraints_truth_table import Truth_table
from dbjudge import squema_recollector

TIMEOUT_PER_QUERY = 20


def create_question(database, query, question):
    """Creates a question and stores it in db_judge database.
    It also tries to generate enough different data to make the judge more reliable.

    :param database: target database
    :param query: Correct answer, it has to be a valid SQL query for the target database.
    :type query: string
    :param question: Question about database data.
    :type question: string
    """
    Manager.singleton_instance.select_database(database)
    connection = Manager.singleton_instance.selected_db_connection
    context = squema_recollector.create_context(connection)
    squema_recollector.update_context_instances(context)

    creation_cursor = connection.cursor()

    slices = slicer.slice_sql(query)
    mapped_slices = slicer.map_slices(slices)

    for table_name, relevant_slices in mapped_slices.items():
        table = context.get_table_by_name(table_name)
        table_data = _generate_table_data(
            context, table, relevant_slices)

        for data in table_data:
            Manager.singleton_instance.custom_insert(
                table.name, table.columns.keys(), data, creation_cursor)
        connection.commit()

    Manager.singleton_instance.register_question(question, query, database)


def _generate_table_data(context, table, query_list):
    table_faker = Faker(table, context)
    db_cursor = Manager.singleton_instance.selected_db_connection.cursor()

    final_data = []
    truth_table = Truth_table(query_list)
    completed_data_generation = False
    start_time = time.process_time()
    while not completed_data_generation:
        fake_data = table_faker.generate_fake(table)

        check_row = []
        for check in query_list:
            db_cursor.execute(check)
            results = db_cursor.fetchall()
            len_before_insert = len(results)

            Manager.singleton_instance.custom_insert(
                table.name, table.columns.keys(), fake_data, db_cursor)

            db_cursor.execute(check)
            results = db_cursor.fetchall()
            len_after_insert = len(results)

            # No new results found means that boolean value of the expression is false
            bool_state = not len_after_insert - len_before_insert == 0
            db_cursor.connection.rollback()
            check_row.append(bool_state)

        inmutable_check_row = tuple(check_row)

        if inmutable_check_row not in truth_table.table:
            final_data.append(fake_data)
            truth_table.add(inmutable_check_row)
        completed_data_generation = truth_table.is_completed()

        if time.process_time() - start_time > TIMEOUT_PER_QUERY*len(query_list):
            break

    return final_data
