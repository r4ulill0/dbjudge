import psycopg2
from psycopg2 import sql
from sqlparse import keywords

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
        if not installed:
            self._install()

    def __del__(self):
        self.main_connection.close()
        if self.selected_db_connection is not None:
            self.selected_db_connection.close()

    def _is_installed(self):
        cursor = self.main_connection.cursor()
        query = queries.CHECK_INTALLATION

        cursor.execute(query)
        result = cursor.fetchall()

        is_installed = (len(result) == 5)
        return is_installed

    def _install(self):
        writer = self.main_connection.cursor()
        writer.execute(queries.INSTALLATION_QUERY)
        writer.close()
        self.main_connection.commit()
        self._install_default_keywords()

    def _install_default_keywords(self):
        with self.main_connection.cursor() as writer:
            for keyword in keywords.KEYWORDS_COMMON:
                writer.execute(queries.REGISTER_KEYWORD, (keyword,))

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
        if db_name not in self.get_databases():
            exception = exceptions.MissingDatabaseError()
            raise exception
        writer = self.main_connection.cursor()
        self.main_connection.commit()
        self.main_connection.autocommit = True
        writer.execute(sql.SQL(queries.DELETE_DATABASE).format(
            sql.Identifier(db_name),
        ))
        writer.execute(queries.DELETE_DB_KEYWORDS, (db_name,))
        writer.execute(queries.DELETE_DB_QUESTIONS, (db_name,))
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

    def custom_insert(self, table_name, columns_names, values, db_cursor=None):
        if not db_cursor:
            db_cursor = self.selected_db_connection.cursor()

        query_template = "INSERT INTO {} ({}) VALUES ({});"

        insert_query = sql.SQL(query_template).format(
            sql.Identifier(table_name),
            sql.SQL(',').join(map(sql.Identifier, columns_names)),
            sql.SQL(',').join(sql.Placeholder() * len(values))
        )

        db_cursor.execute(insert_query, values)

    def register_question(self, question, query, database, keywords=None):
        '''Register a question in the main database.

            Parameters:
                question (str): Question about target database
                query (str): Correct answer written in SQL
                database (str): Name of the target database
                keywords (dict): Mapped keywords to a boolean value
                    that indicates if it is a expected keyword or not
        '''
        db_cursor = self.main_connection.cursor()
        db_cursor.execute(queries.REGISTER_QUESTION_QUERY,
                          (question, query, database))
        self.main_connection.commit()

        question_id = db_cursor.fetchall()[0]
        if keywords:
            for keyword, expected in keywords.items():
                db_cursor.execute(queries.REGISTER_KEYWORD_SELECTION,
                                  (question_id, keyword, expected))
            self.main_connection.commit()

    def get_questions(self, database=None):
        if not database:
            database = self.selected_db_connection.dbname
        db_cursor = self.main_connection.cursor()
        db_cursor.execute(queries.GET_QUESTIONS, (database,))

        questions = db_cursor.fetchall()
        return questions

    def get_question_keywords(self, question):
        reader = self.main_connection.cursor()
        reader.execute(queries.QUESTION_KEYWORDS, (question,))
        result = reader.fetchall()

        formatted_result = []
        for keyword in result:
            formatted_result.append(keyword[0])

        return set(formatted_result)

    def get_question_expected_keywords(self, question):
        with self.main_connection.cursor() as reader:
            reader.execute(queries.GET_EXPECTED_KEYWORDS, (question,))
            result = reader.fetchall()
            formatted_result = dict()
            for keyword in result:
                name = keyword[0]
                expected = keyword[1]
                formatted_result[name] = expected

        return formatted_result

    def execute_in_readonly(self, query):
        self.selected_db_connection.set_session(readonly=True)

        reader = self.selected_db_connection.cursor()
        reader.execute(query)
        result = reader.fetchall()

        self.selected_db_connection.commit()
        self.selected_db_connection.set_session(readonly=False)

        return result

    def get_correct_answer(self, question):
        reader = self.main_connection.cursor()
        reader.execute(queries.SHOW_CORRECT_ANSWER_TO_QUESTION, (question,))
        result = reader.fetchall()
        return result
