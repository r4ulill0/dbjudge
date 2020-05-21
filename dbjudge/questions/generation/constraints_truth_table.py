"""Tools to manage constraints permutations of complex queries."""


class Truth_table():
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
