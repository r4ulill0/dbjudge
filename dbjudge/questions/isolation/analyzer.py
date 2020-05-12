import sqlparse


def get_used_tables(query):
    ''' 
    Returns the tables used in the query after the "FROM" keyword.

    :param query: valid SQL query
    '''
    from_clause = None

    used_tables = []
    parsed_query = sqlparse.parse(query)

    from_clause_found = False
    for token in parsed_query[0].tokens:

        if token.match(sqlparse.keywords.KEYWORDS_COMMON['FROM'], None):
            from_clause_found = True

        elif from_clause_found and isinstance(token, sqlparse.sql.IdentifierList):
            tables = token

            for table in tables:
                if isinstance(table, sqlparse.sql.Identifier):
                    for definition_element in table:
                        if definition_element.match(sqlparse.tokens.Name, None):
                            used_tables.append(definition_element.normalized)
        elif from_clause_found and isinstance(token, sqlparse.sql.Identifier):
            used_tables.append(token.normalized)

    return set(used_tables)
