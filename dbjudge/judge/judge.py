from dbjudge import exceptions
from dbjudge.connection_manager.manager import Manager
from dbjudge.questions.isolation import analyzer


class Judge:
    def __init__(self):
        self.session = None

    def start_session(self, questions):
        self.session = Session(questions)

    def generate_report(self):
        '''Keywords are not case sensitive'''
        if not self.session:
            raise exceptions.SessionNotFound()

        db_connection = Manager.singleton_instance
        report = {}
        for question, answer in self.session.mapped_answers.items():
            if answer:
                perfect_query = db_connection.get_correct_answer(question)
                perfect_query = perfect_query[0][0]

                expected_result = db_connection.execute_in_readonly(
                    perfect_query)
                actual_result = db_connection.execute_in_readonly(answer)
                correct_result = expected_result == actual_result

                expected_tables_used = analyzer.get_used_tables(perfect_query)
                actual_tables_used = analyzer.get_used_tables(answer)
                excess_tables_used = actual_tables_used - expected_tables_used

                watched_keywords = db_connection.get_question_keywords(
                    question)
                expected_keywords = db_connection.get_question_expected_keywords(
                    question)
                used_keywords = self._check_keywords(watched_keywords, answer)
            else:
                correct_result = False
                excess_tables_used = set()
                used_keywords = set()
                expected_keywords = dict()

            report[question] = Analysis(
                correct_result, excess_tables_used, used_keywords, expected_keywords, bool(answer))

        return report

    def _check_keywords(self, keywords, answer):
        result = []
        for keyword in keywords:
            if keyword == '':
                continue
            if keyword.lower() in answer.lower():
                result.append(keyword)

        return tuple(result)


class Session:
    def __init__(self, questions):
        self.mapped_answers = {}
        for question in questions:
            self.mapped_answers[question] = None

    def answer(self, question, answer):
        self.mapped_answers[question] = answer


class Analysis:
    def __init__(self, correct_result, excess_tables_used, used_keywords, expected_keywords, answered):
        self.excess_tables_used = excess_tables_used
        self.used_keywords = used_keywords
        self.expected_keywords = expected_keywords
        self.answered = answered
        self.keyword_compliant = self._keywords_check()
        self.correct_result = correct_result and self.keyword_compliant

    def is_correct(self):
        return self.correct_result and self.keyword_compliant

    def _keywords_check(self):
        result = True
        for keyword, expected in dict():
            if (keyword in self.used_keywords) and not expected:
                result = False

        return result
