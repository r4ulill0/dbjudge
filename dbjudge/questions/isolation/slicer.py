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

    if not where_clause:
        return [query, ]

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


def map_slices(slices, context):
    """Relate SQL query slices to its corresponding table.
    Only "WHERE" restrictions tables are mapped.

    :param slices: Multiple SQL queries
    :type slices: Iterable of SQL strings
    :param context: Context of the target database
    :type context: Context
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

        if not where_clause:
            return {}

        for token in where_clause.tokens:
            if isinstance(token, sqlparse.sql.Comparison):
                names = _get_comparison_names(token)
                table = _find_table(names, table_aliases)
                if table is None:
                    table = _deduce_table(names, context)
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


def _deduce_table(names, context):
    for name in names:
        for table in context.tables:
            for column, _ in table.columns.items():
                if column == name:
                    result = table.name

    return result
