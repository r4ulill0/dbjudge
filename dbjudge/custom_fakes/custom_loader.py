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
"""Tools to create new data types."""
import csv
from dbjudge.connection_manager.manager import Manager


def load_csv_fakes(csv_file_path):
    """Load in memory a csv file

    :param csv_file_path: path to the file
    :type csv_file_path: string
    :return: multiple rows read from the file
    :rtype: list
    """
    with open(csv_file_path) as csv_file:

        reader = csv.reader(csv_file)
        results = []
        for row in reader:
            results.append(row)

    return results


def save_to_database(results, selected_columns=None, selected_names=None):
    '''
    Save custom types into database. First row of the input is reserved for
    type names.

    :param results: Iterable with data rows to insert into the database
    :param selected_columns: Iterable with the indexes of desired columns from results rows
    :param selected_names: Iterable with the type name for each column.
        If no selected_name provided, first row from results will be used instead.

    If provided, selected columns and names must have the same size.
    '''

    transactions = []
    for row in results:
        selected_data = []
        for idx, column in enumerate(row):
            if selected_columns and idx not in selected_columns:
                continue
            selected_data.append(column)
        transactions.append(selected_data)

    manager = Manager.singleton_instance

    for idx, transaction in enumerate(transactions):
        # Do not read first row, but if there are no names specified,
        # take first row as names row
        if idx == 0:
            if not selected_names:
                selected_names = transactions[0]

        else:
            for col, fake_type_name in enumerate(selected_names):
                manager.register_fake_data(transaction[col], fake_type_name)

    manager.main_connection.commit()
