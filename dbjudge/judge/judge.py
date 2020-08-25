"""Judge module responsible of testing if user answers are correct
based on preloaded correct answers."""
from dbjudge import exceptions
from dbjudge.connection_manager.manager import Manager
from dbjudge.questions.isolation import analyzer


class Judge:
    """Judge object that manage user tests sessions.
    """

    def __init__(self):
        self.session = None

    def start_session(self, questions):
        """Starts a new test session.

        :param questions: Questions to answer on this session.
        :type questions: Iterable of SQL strings
        """
        self.session = Session(questions)

    def generate_report(self):
        """Generates a report with information about the current session.
        Each question has its own analisys.
        Keywords analisys is not case sensitive.

        :return: Report with an analisys to every question, even if it is unanswered.
        :rtype: dict
        """
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

        return set(result)


class Session:
    """Test session that stores answers to each question on it."""

    def __init__(self, questions):
        self.mapped_answers = {}
        for question in questions:
            self.mapped_answers[question] = None

    def answer(self, question, answer):
        """Stores an answer inside the session.

        :param question: question
        :type question: string
        :param answer: An SQL query that answers the question
        :type answer: string
        """
        self.mapped_answers[question] = answer


class Analysis:
    """Analysis about a question answer.
    """

    def __init__(self, correct_result, excess_tables_used, used_keywords,
                 expected_keywords, answered):
        self.excess_tables_used = excess_tables_used
        self.used_keywords = used_keywords
        self.expected_keywords = expected_keywords
        self.answered = answered
        self.keyword_compliant = self._keywords_check()
        self.correct_result = correct_result

    def is_correct(self):
        """Returns True if the answer is considered correct, False otherwise.

        :rtype: boolean
        """
        return self.correct_result and self.keyword_compliant

    def _keywords_check(self):
        result = True
        for keyword, expected in self.expected_keywords.items():
            if (keyword in self.used_keywords) and not expected:
                result = False

        return result
