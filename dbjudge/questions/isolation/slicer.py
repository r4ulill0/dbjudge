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
""" Module to slice queries into manageable fragments
"""
import sqlparse


def slice_sql(query):
    """Slice a complex query into simple ones.
    This complexity only takes into account the where clause.
    Constraints with 'OR' keyword are considered one single constraint.

    SELECT * FROM T WHERE X and Y and Z;
    SELECT * FROM T WHERE X;
    SELECT * FROM T WHERE Y;
    SELECT * FROM T WHERE Z;

    :param query: SQL query
    :type query: string
    :return: Simple queries that together are equivalent to the original.
    :rtype: list
    """
    output_queries = []
    parsed_query = sqlparse.parse(query)

    where_clause = None
    for pos, element in enumerate(parsed_query[0]):
        if isinstance(element, sqlparse.sql.Where):
            where_clause = element

    and_positions = []
    for pos, token in enumerate(where_clause.tokens):
        if token.is_keyword and token.normalized == 'AND':
            and_positions.append(pos)
    and_positions.append(len(where_clause.tokens))

    output_queries = []
    last_pos = 1  # Do not include WHERE token and first whitespace token
    original_tokens = where_clause.tokens
    modifier = 0
    for pos in and_positions:
        modifier = 1 if last_pos != 1 else 0
        # Where token + sliced tokens
        where_clause.tokens = original_tokens[:1] + \
            original_tokens[last_pos+modifier:pos]

        recomposed_query = str(parsed_query[0])
        if ';' not in recomposed_query:
            recomposed_query += ';'

        output_queries.append(recomposed_query)
        last_pos = pos
    where_clause.tokens = original_tokens[last_pos:len(original_tokens)]

    return output_queries


def map_slices(slices):
    """Relate SQL query slices to its corresponding table.
    Only "WHERE" restrictions tables are mapped.

    :param slices: Multiple SQL queries
    :type slices: Iterable of SQL strings
    :return: Dictionary relating tables with queries that use them
    :rtype: dict
    """
    mapping = {}

    for query in slices:
        parsed_query = sqlparse.parse(query)

        parsing_from = False
        where_clause = None
        table_aliases = {}
        for token in parsed_query[0]:
            if token.match(sqlparse.tokens.Keyword, 'FROM'):
                parsing_from = True
            elif parsing_from and isinstance(token, sqlparse.sql.Identifier):
                table, alias = _get_table_and_alias(token)
                table_aliases[alias] = table
            elif isinstance(token, sqlparse.sql.Where):
                where_clause = token
                parsing_from = False

        for token in where_clause.tokens:
            if isinstance(token, sqlparse.sql.Comparison):
                names = _get_comparison_names(token)
                table = _find_table(names, table_aliases)
                if table not in mapping.keys():
                    mapping[table] = []
                mapping[table].append(query)

    return mapping


def _get_table_and_alias(table_identifier):
    table = None
    alias = None
    for subtoken in table_identifier.tokens:
        if subtoken.ttype is sqlparse.tokens.Name:
            table = subtoken.normalized
        elif isinstance(subtoken, sqlparse.sql.Identifier):
            alias = subtoken.normalized
    output = (table, alias)
    return output


def _get_comparison_names(comparison_token):
    names = set()
    sides = (comparison_token.left, comparison_token.right)
    for side in sides:
        if isinstance(side, sqlparse.sql.Identifier):
            for token in side.tokens:
                if token.ttype is sqlparse.tokens.Name:
                    names.add(token.normalized)

    return names


def _find_table(names, table_aliases):
    result = None
    for name in names:
        if name in table_aliases.keys():
            result = table_aliases[name]
            break
    return result
