import psycopg2
from psycopg2 import sql

from dbjudge import exceptions
from dbjudge.utils import queries
from dbjudge.utils.metaclasses import Singleton


class Manager(metaclass=Singleton):

    def __init__(self, *, user, password, host, database_name, port='5432'):
        self.main_connection = psycopg2.connect(
            host=host, dbname=database_name, user=user, password=password, port=port)
        self.selected_db_connection = None
        self.username = user
        self.password = password
        self.host = host
        self.port = port

        installed = self._is_installed()
        if(not installed):
            self._install()

    def __del__(self):
        self.main_connection.close()
        if(self.selected_db_connection != None):
            self.selected_db_connection.close()

    def _is_installed(self):
        cursor = self.main_connection.cursor()
        query = queries.CHECK_INTALLATION

        cursor.execute(query)
        result = cursor.fetchall()

        is_installed = (len(result) == 3)
        return is_installed

    def _install(self):
        writer = self.main_connection.cursor()
        writer.execute(queries.INSTALLATION_QUERY)
        writer.close()
        self.main_connection.commit()

    def select_database(self, db_name):
        if(db_name not in self.get_databases()):
            exception = exceptions.MissingDatabaseError()
            raise exception
        try:
            new_connection = psycopg2.connect(
                host=self.host, dbname=db_name,
                user=self.username, password=self.password)
            if (self.selected_db_connection != None):
                self.selected_db_connection.close()
            self.selected_db_connection = new_connection
        finally:
            return

    def create_database(self, db_name):
        if(db_name in self.get_databases()):
            exception = exceptions.DuplicatedDatabaseError()
            raise exception
        writer = self.main_connection.cursor()
        self.main_connection.commit()
        self.main_connection.autocommit = True
        writer.execute(sql.SQL(queries.CREATE_DATABASE).format(
            sql.Identifier(db_name)
        ))
        writer.execute(queries.CREATE_DB_REGISTRY, (db_name,))
        self.main_connection.autocommit = False

        writer.close()

    def delete_database(self, db_name):
        if(db_name not in self.get_databases()):
            exception = exceptions.MissingDatabaseError()
            raise exception
        writer = self.main_connection.cursor()
        self.main_connection.commit()
        self.main_connection.autocommit = True
        writer.execute(sql.SQL(queries.DELETE_DATABASE).format(
            sql.Identifier(db_name),
        ))
        writer.execute(queries.DELETE_DB_REGISTRY, (db_name,))
        self.main_connection.autocommit = False

        writer.close()

    def get_databases(self):
        reader = self.main_connection.cursor()
        reader.execute(queries.SHOW_DATABASES)
        results = reader.fetchall()

        formatted_results = []
        for result in results:
            formatted_results.append(result[0])

        return formatted_results

    def register_fake_data(self, data, fake_type):
        writer = self.main_connection.cursor()
        writer.execute(queries.REGISTER_FAKE_DATA, (data, fake_type))
        writer.close()

    def get_fake_types(self):
        reader = self.main_connection.cursor()
        reader.execute(queries.SHOW_CUSTOM_FAKE_TYPES)

        result = reader.fetchall()
        return result

    def get_custom_fakes(self, fake_type):
        reader = self.main_connection.cursor()
        reader.execute(queries.CUSTOM_FAKES_QUERY, (fake_type,))

        result = reader.fetchall()
        return result

    def execute_sql(self, query):
        writer = self.selected_db_connection.cursor()
        writer.execute(query)
