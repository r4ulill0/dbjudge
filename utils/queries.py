
TABLES_QUERY = '''
    with recursive fk_tree as (
    -- All tables not referencing anything else
    select t.oid as reloid,
        t.relname as table_name,
        s.nspname as schema_name,
        null::text as referenced_table_name,
        null::text as referenced_schema_name,
        1 as level
    from pg_class t
        join pg_namespace s on s.oid = t.relnamespace
    where relkind = 'r'
        and not exists (select *
                    from pg_constraint
                    where contype = 'f'
                      and conrelid = t.oid)
        and s.nspname = 'public' -- limit to one schema

    union all

    select ref.oid,
        ref.relname,
        rs.nspname,
        p.table_name,
        p.schema_name,
        p.level + 1
  from pg_class ref
    join pg_namespace rs on rs.oid = ref.relnamespace
    join pg_constraint c on c.contype = 'f' and c.conrelid = ref.oid
    join fk_tree p on p.reloid = c.confrelid
), tables_hierarchy as (
    -- this picks the highest level for each table
    select schema_name, table_name,
        level,
        row_number() over (partition by schema_name, table_name order by level desc) as last_table_row
  from fk_tree
)
    select R.table_name
    from (select distinct IS_T.table_name, TH.level
    from information_schema.tables IS_T, tables_hierarchy TH
    where IS_T.table_schema='public' and IS_T.table_name=TH.table_name) R
    order by level

    '''
COLUMN_TYPE_QUERY = '''
    select C.column_name, C.data_type, C.is_nullable, C.character_maximum_length
    from information_schema.columns C
    where C.table_name=%s
    '''

CONSTRAINT_QUERY = '''
    select TC.constraint_name, TC.constraint_type
    from information_schema.table_constraints TC
    where TC.table_name=%s
    '''

REFERENCE_QUERY = '''
    select KCUf.constraint_name, KCUf.table_name, KCUf.column_name, '**references**',
        KCUp.table_name, KCUp.column_name, KCUp.ordinal_position
    from information_schema.table_constraints TC, information_schema.key_column_usage KCUf,
        information_schema.key_column_usage KCUp, information_schema.referential_constraints RC
    where RC.constraint_name=KCUf.constraint_name
        and RC.unique_constraint_name=KCUp.constraint_name
        and TC.constraint_type='FOREIGN KEY' and TC.constraint_name=KCUf.constraint_name
        and KCUf.ordinal_position = KCUp.ordinal_position and KCUf.table_name=%s
    '''

PRIMARY_KEY_QUERY = '''
    select KCU.column_name
    from information_schema.key_column_usage KCU, information_schema.table_constraints TC
    where TC.constraint_type='PRIMARY KEY'
        and TC.constraint_name=KCU.constraint_name and KCU.table_name=%s
    '''

UNIQUE_KEY_QUERY = '''
    select distinct KCU.column_name
    from information_schema.key_column_usage KCU, information_schema.table_constraints TC
    where (TC.constraint_type='UNIQUE' or TC.constraint_type='PRIMARY KEY')
        and TC.constraint_name=KCU.constraint_name and KCU.table_name=%s
    '''
INSTALLATION_QUERY = '''
    CREATE TABLE dbjudge_databases(
        name varchar(20) NOT NULL,
        PRIMARY KEY (name)
    );
    CREATE TABLE dbjudge_fake_data(
        data text,
        fake_type varchar(20),
        PRIMARY KEY (data)
    );
    CREATE TABLE dbjudge_questions(
        id integer,
        question text,
        sql_query text,
        PRIMARY KEY (id)
    );
    '''

CHECK_INTALLATION = '''
    SELECT relname
    FROM pg_catalog.pg_class c
        LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
    WHERE relname like 'dbjudge_%' AND relkind='r'
'''

CREATE_DATABASE = '''
    CREATE DATABASE {};
'''

CREATE_DB_REGISTRY = '''
    INSERT INTO dbjudge_databases (name) VALUES (%s);
'''

DELETE_DATABASE = '''
    DROP DATABASE {};
'''
DELETE_DB_REGISTRY = '''
    DELETE FROM dbjudge_databases WHERE (name = %s);
'''

SHOW_DATABASES = '''
    SELECT name FROM dbjudge_databases;
'''