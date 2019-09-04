
import psycopg2
from psycopg2 import sql
from utils import queries
from utils.metaclasses import Singleton


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
        try:
            new_connection = psycopg2.connect(
                host=self.host, dbname=db_name,
                user=self.username, password=self.password)
            self.selected_db_connection.close()
            self.selected_db_connection = new_connection
        finally:
            return

    def create_database(self, db_name):
        if(db_name in self.show_databases()):
            exception = Exception()
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
        if(db_name not in self.show_databases()):
            exception = Exception()
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

    def show_databases(self):
        reader = self.main_connection.cursor()
        reader.execute(queries.SHOW_DATABASES)
        results = reader.fetchall()

        formatted_results = []
        for result in results:
            formatted_results.append(result[0])

        return formatted_results
