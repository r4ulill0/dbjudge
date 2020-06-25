# MIT License

# Copyright (c) 2020 Raúl Medina González <raulmgcontact@gmail.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Tools for sql parsing purposes"""
import sqlparse


def get_used_tables(query):
    """
    Returns the tables used in the query after the "FROM" keyword.

    :param query: valid SQL query
    """

    used_tables = []
    parsed_query = sqlparse.parse(query)

    from_clause_found = False
    for token in parsed_query[0].tokens:

        if token.match(sqlparse.keywords.KEYWORDS_COMMON['FROM'], None):
            from_clause_found = True

        elif from_clause_found and isinstance(token, sqlparse.sql.IdentifierList):
            tables = token
            _parse_identifier_list_into_used_tables(tables, used_tables)

        elif from_clause_found and isinstance(token, sqlparse.sql.Identifier):
            used_tables.append(token.normalized)

    return set(used_tables)


def _parse_identifier_list_into_used_tables(tables, used_tables):
    for table in tables:
        if isinstance(table, sqlparse.sql.Identifier):
            for definition_element in table:
                if definition_element.match(sqlparse.tokens.Name, None):
                    used_tables.append(definition_element.normalized)
