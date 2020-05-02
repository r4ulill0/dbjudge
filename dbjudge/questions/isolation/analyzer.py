import sqlparse


def get_used_tables(query):
    ''' Returns the tables used in the query after the "FROM" keyword.
    '''
    from_clause = None

    used_tables = []
    parsed_query = sqlparse.parse(query)

    from_clause_found = False
    for token in parsed_query[0].tokens:

        if token.match(sqlparse.keywords.KEYWORDS_COMMON['FROM'], None):
            from_clause_found = True

        elif from_clause_found and isinstance(token, sqlparse.sql.IdentifierList):
            tables_tokens = token
            break

    for table_token in tables_tokens:
        if isinstance(table_token, sqlparse.sql.Identifier):
            for token in table_token:
                if token.match(sqlparse.tokens.Name, None):
                    used_tables.append(table_token.normalized)

    return tuple(used_tables)
