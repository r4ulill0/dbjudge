# MIT License

# Copyright (c) 2020 Raúl Medina González <raulmgcontact@gmail.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Question generation module."""
import time
from dbjudge.connection_manager.manager import Manager
from dbjudge.fake_data_gen import Faker
from dbjudge.questions.isolation import slicer
from dbjudge.questions.generation.constraints_truth_table import TruthTable
from dbjudge import squema_recollector

TIMEOUT_PER_QUERY = 20


def create_question(database, query, question, context):
    """Creates a question and stores it in db_judge database.
    It also tries to generate enough different data to make the judge more reliable.

    :param database: target database
    :param query: Correct answer, it has to be a valid SQL query for the target database.
    :type query: string
    :param question: Question about database data.
    :type question: string
    :param context: Context of the target database
    :type context: Context
    """
    Manager.singleton_instance.select_database(database)
    connection = Manager.singleton_instance.selected_db_connection
    squema_recollector.update_context_instances(context)

    creation_cursor = connection.cursor()

    slices = slicer.slice_sql(query)
    mapped_slices = slicer.map_slices(slices, context)

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

    final_data = []
    truth_table = TruthTable(query_list)
    completed_data_generation = False
    start_time = time.process_time()
    while not completed_data_generation:
        fake_data = table_faker.generate_fake(table)

        is_new_row = truth_table.check_row_state(table, query_list, fake_data)

        if is_new_row:
            final_data.append(fake_data)

        completed_data_generation = truth_table.is_completed()

        if time.process_time() - start_time > TIMEOUT_PER_QUERY*len(query_list):
            break

    return final_data
