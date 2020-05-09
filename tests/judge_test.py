import pytest
from dbjudge import exceptions
from dbjudge.judge.judge import Session, Judge
from dbjudge.connection_manager.manager import Manager

q1 = "Libros con mas de 10 ejemplares"
q2 = "Personas que esten sancionadas y no puedan sacar libros"
q3 = "Dni de los chicos que tienen un libro prestado"
a1 = "Select titulo from Libro Where ejemplares > 10;"
a2 = "Select * FROM Persona Where Persona.suspension = TRUE;"
a3 = "Select dni FROM Persona, Prestamo WHERE Persona.userid = Prestamo.persona AND (now() - Prestamo.fecha) > Prestamo.duracion_maxima;"


@pytest.fixture
def mocked_judge(make_database):
    keywords1 = {"GROUP": False, "BY": False}
    mock_map = {q1: a1, q2: a2, q3: a3}

    dbname = 'judge_reportgen_test'
    make_database(dbname)
    Manager.singleton_instance.select_database(dbname)
    Manager.singleton_instance.execute_sql(
        open('tests/sql_files/exampleDatabase.sql').read())
    Manager.singleton_instance.selected_db_connection.commit()
    Manager.singleton_instance.register_question(q1, a1, dbname, keywords1)
    Manager.singleton_instance.register_question(q2, a2, dbname)
    Manager.singleton_instance.register_question(q3, a3, dbname)

    judge = Judge()
    session = Session([])
    session.mapped_answers = mock_map
    judge.session = session
    return judge


def test_generate_report(mocked_judge):
    report = mocked_judge.generate_report()
    question_1, question_2, question_3 = mocked_judge.session.mapped_answers

    assert report[question_1].correct_result
    assert report[question_2].correct_result
    assert report[question_3].correct_result
    assert not report[question_1].excess_tables_used
    assert not report[question_2].excess_tables_used
    assert not report[question_3].excess_tables_used
    assert not report[question_1].used_keywords
    assert not report[question_2].used_keywords
    assert not report[question_3].used_keywords
    assert report[question_1].answered
    assert report[question_2].answered
    assert report[question_3].answered


def test_excess_tables_report(mocked_judge):
    alternative_answer = "Select lib.titulo from Libro lib, Prestamo, Persona Where lib.ejemplares > 10;"
    mocked_judge.session.mapped_answers[q1] = alternative_answer
    report = mocked_judge.generate_report()

    expected_excess_tables = set(("Prestamo", "Persona"))

    assert report[q1].correct_result
    assert report[q1].excess_tables_used == expected_excess_tables


def test_used_keywords_report(mocked_judge):
    alternative_answer = "Select titulo from Libro Where ejemplares > 10 GROUP BY titulo;"
    mocked_judge.session.mapped_answers[q1] = alternative_answer
    report = mocked_judge.generate_report()

    expected_used_keywords = set(("GROUP", "BY"))

    assert report[q1].correct_result
    assert report[q1].used_keywords == expected_used_keywords


def test_unanswered_report(mocked_judge):
    no_response = ""
    mocked_judge.session.mapped_answers[q1] = no_response
    mocked_judge.session.mapped_answers[q2] = no_response
    mocked_judge.session.mapped_answers[q3] = no_response

    report = mocked_judge.generate_report()

    assert not report[q1].answered
    assert not report[q2].answered
    assert not report[q3].answered

    assert not report[q1].correct_result
    assert not report[q2].correct_result
    assert not report[q3].correct_result


def test_report_without_session():
    with pytest.raises(exceptions.SessionNotFound):
        new_judge = Judge()
        new_judge.generate_report()
