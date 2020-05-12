import csv
from dbjudge.connection_manager.manager import Manager


def load_csv_fakes(csv_file_path):
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
