
import psycopg2
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

    def _select_database(self, db_name):
        if(db_name == None):
            return None
        else:
            return psycopg2.connect(
                host=self.host, dbname=db_name, user=self.username, password=self.password)
