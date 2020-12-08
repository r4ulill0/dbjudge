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
"""This module is capable of fill a database with fake data."""
import time
from dbjudge import fake_data_gen
from dbjudge.connection_manager.manager import Manager


def generate_fake_data(context, db_connection):
    """Fills a database with random data.
    The given context has to define the database that the connection reference to.

    :param context: Target database context
    :type context: Context
    :param db_connection: Target database connection
    """
    db_cursor = db_connection.cursor()

    for table in context.tables:
        faker = fake_data_gen.Faker(table, context)
        _fill_table(table, faker, db_cursor)
        db_connection.commit()

    db_cursor.close()


def _fill_table(table, faker, db_cursor):

    pending_inserts = table.fake_data_size
    while pending_inserts > 0:
        time.sleep(0.01)  # Avoid hogging the CPU
        values_list = faker.generate_fake(table)
        insert_success = Manager.singleton_instance.custom_insert(
            table.name, table.columns.keys(), values_list, db_cursor)
        if insert_success:
            pending_inserts -= 1
        else:
            table.row_instances.pop()
