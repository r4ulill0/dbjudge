import pytest
from dbjudge.queries.isolation import slicer


def test_slice_querie():
    test_query = ("SELECT * "
                  "FROM person p "
                  "WHERE p.age > 20 and "
                  "p.name not like 'juan' and "
                  "p.color NOT red and "
                  "p.adress<30000;")
    expected_results = [
        ("SELECT * "
         "FROM person p "
            "WHERE p.age > 20 ;"),
        ("SELECT * "
            "FROM person p "
            "WHERE p.name not like 'juan' ;"
         ),
        ("SELECT * "
         "FROM person p "
         "WHERE p.color NOT red ;"
         ),
        ("SELECT * "
         "FROM person p "
         "WHERE p.adress<30000;"
         )
    ]

    results = slicer.slice(test_query)

    assert results == expected_results
