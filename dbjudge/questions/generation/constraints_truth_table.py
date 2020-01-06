
class Truth_table():

    def __init__(self, query_list):
        self.state_size = len(query_list)
        self.table_size = 2 ** self.state_size
        self.table = set()

    def add(self, check_row):
        if check_row and len(check_row) == self.state_size:
            self.table.add(check_row)

    def is_completed(self):
        return len(self.table) == self.table_size
