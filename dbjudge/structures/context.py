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
"""Context class"""
from dbjudge import exceptions
from dbjudge.structures.table import Table


class Context:
    """Keeps track of the current database that is being managed.
    """

    def __init__(self):
        self.tables = []

    def add_table(self, table: Table):
        """Adds a table to the context

        :param table: target database table name
        :type table: Table
        """
        self.tables.append(table)

    def get_table_by_name(self, table_name):
        """Looks for a table in the context by name.

        :param table_name: The complete table name
        :type table_name: string
        :raises exceptions.TableNotInContext: If table is not present in the context
        :return: A table with the specified name in the context
        :rtype: Table
        """
        for table in self.tables:
            if table.name == table_name:
                return table
        raise exceptions.TableNotInContext()

    def resolve_column_reference(self, reference):
        """Looks for the column that is being referenced

        :param reference: reference to a column
        :type reference: Reference
        :raises exceptions.ColumnReferenceNotFound: If there is no table in the context
            that match with the reference taget
        :return: Referenced column
        :rtype: Column
        """
        table_name, column_name = reference
        for table in self.tables:
            if table.name == table_name:
                return table.columns[column_name]

        raise exceptions.ColumnReferenceNotFound(
            'column {column} not found in table: {table}'.format(
                column=column_name, table=table_name))
