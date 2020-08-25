"""Tools to manage constraints permutations of complex queries."""
from dbjudge.connection_manager.manager import Manager


class TruthTable():
    """Truth table object to keep track of permutations of boolean states.
    """

    def __init__(self, query_list):
        self.state_size = len(query_list)
        self.table_size = 2 ** self.state_size
        self.table = set()

    def add(self, check_row):
        """Adds a permutation to the table.
        Each permutation is unique to each table
        and all permutations in a truth table must have the same size.

        :param check_row: Multiple ordered boolean values
        """
        if check_row and len(check_row) == self.state_size:
            self.table.add(check_row)

    def is_completed(self):
        """Checks if the truth table has all its possible permutations.

        :return: True if all possible permutations are stored, False otherwise.
        :rtype: boolean
        """
        return len(self.table) == self.table_size

    def check_row_state(self, table, query_list, fake_data):
        """Checks if the row state exists in the table and adds it if it does not exist.

        :param query_list: A list of SQL queries
        :type query_list: list
        :param fake_data: Fake data to insert in the database table
        :type fake_data: list
        :param table: Target database table
        :type table: Table
        :return: True if a new row is added to the table, False otherwise.
        :rtype: list
        """
        db_cursor = Manager.singleton_instance.selected_db_connection.cursor()
        check_row = []
        for check in query_list:
            db_cursor.execute(check)
            results = db_cursor.fetchall()
            len_before_insert = len(results)

            Manager.singleton_instance.custom_insert(
                table.name, table.columns.keys(), fake_data)

            db_cursor.execute(check)
            results = db_cursor.fetchall()
            len_after_insert = len(results)

            # No new results found means that boolean value of the expression is false
            bool_state = not len_after_insert - len_before_insert == 0
            db_cursor.connection.rollback()
            check_row.append(bool_state)

        result = tuple(check_row)
        is_new_row = result not in self.table
        if is_new_row:
            self.add(result)

        return is_new_row
