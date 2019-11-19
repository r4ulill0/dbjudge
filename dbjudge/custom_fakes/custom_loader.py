import csv
from dbjudge.connection_manager.manager import Manager


def load_csv_fakes(csv_file_path):
    with open(csv_file_path) as csv_file:

        reader = csv.reader(csv_file)
        results = []
        for row in reader:
            results.append(row)

    return results


def save_to_database(results, selected_columns=[], selected_names=[]):
    transactions = []
    for row in results:
        selected_data = []
        for idx, column in enumerate(row):
            if (idx not in selected_columns):
                continue
            selected_data.append(column)
        transactions.append(selected_data)

    manager = Manager.singleton_instance

    for idx, transaction in enumerate(transactions):
        # Do not read first row, but if there are no names specified,
        # take first row as names row
        if (idx == 0):
            if len(selected_names) == 0:
                selected_names = transactions[0]
            continue

        for col, fake_type_name in enumerate(selected_names):
            manager.register_fake_data(transaction[col], fake_type_name)

    manager.main_connection.commit()