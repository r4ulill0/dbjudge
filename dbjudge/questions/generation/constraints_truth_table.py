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
        """Return a row state from a combination of fake data appearances
        in the results of multiple queries.

        :param query_list: A list of SQL queries
        :type query_list: list
        :param fake_data: Fake data to insert in the database table
        :type fake_data: list
        :param table: Target database table
        :type table: Table
        :return: Appearances in queries, True if it appears False otherwise
        :rtype: list
        """
        db_manager = Manager.singleton_instance
        check_row = []
        for check in query_list:
            results = db_manager.execute_sql(check)
            len_before_insert = len(results) if results else 0

            Manager.singleton_instance.custom_insert(
                table.name, table.columns.keys(), fake_data)

            results = db_manager.execute_sql(check)
            len_after_insert = len(results) if results else 0

            # No new results found means that boolean value of the expression is false
            bool_state = not len_after_insert - len_before_insert == 0
            db_manager.selected_db_connection.rollback()
            check_row.append(bool_state)

        return check_row
