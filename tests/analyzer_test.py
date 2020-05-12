import pytest
from dbjudge.questions.isolation import analyzer


def test_get_used_tables():
    test_query = "Select lib.titulo from Libro lib, Prestamo, Persona Where lib.ejemplares > 10;"

    tables = analyzer.get_used_tables(test_query)

    expected_tables = set(("Libro", "Prestamo", "Persona"))

    assert tables == expected_tables


def test_used_tables_parser():
    test_query = 'select * from Libro INNER JOIN Prestamo ON Libro.titulo=Prestamo.titulo;'
    expected_tables = set(('Libro', 'Prestamo'))

    tables = analyzer.get_used_tables(test_query)

    assert tables == expected_tables
