import copy
import sqlparse


def slice(query):
    output_queries = []
    parsed_query = sqlparse.parse(query)

    where_clause = None
    for pos, element in enumerate(parsed_query[0]):
        if type(element) == sqlparse.sql.Where:
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
        if not ';' in recomposed_query:
            recomposed_query += ';'

        output_queries.append(recomposed_query)
        last_pos = pos
    where_clause.tokens = original_tokens[last_pos:len(original_tokens)]

    return output_queries
