import os
import psycopg2
from structures import Table, Column, Context

TABLES_QUERY = "select IS_T.table_name from information_schema.tables IS_T where IS_T.table_schema='public'"
COLUMN_TYPE_QUERY = "select C.column_name, C.data_type from information_schema.columns C where C.table_name=%s"
CONSTRAINT_QUERY ="select TC.constraint_name, TC.constraint_type from information_schema.table_constraints TC where TC.table_name=%s"
REFERENCE_QUERY = "select KCUf.constraint_name, KCUf.table_name, KCUf.column_name, '**references**', KCUp.table_name, KCUp.column_name, KCUp.ordinal_position from information_schema.table_constraints TC, information_schema.key_column_usage KCUf, information_schema.key_column_usage KCUp, information_schema.referential_constraints RC where RC.constraint_name=KCUf.constraint_name and RC.unique_constraint_name=KCUp.constraint_name   and TC.constraint_type='FOREIGN KEY' and TC.constraint_name=KCUf.constraint_name   and KCUf.ordinal_position = KCUp.ordinal_position and KCUf.table_name=%s and KCUf.column_name=%s"
PRIMARY_KEY_QUERY = "select KCU.column_name from information_schema.key_column_usage KCU, information_schema.table_constraints TC where TC.constraint_type='PRIMARY KEY' and TC.constraint_name=KCU.constraint_name and KCU.table_name=%s"


def create_context(conn):
	
	database_cursor = conn.cursor()
	context = Context()

	_load_tables(context, database_cursor)

	for table in context.tables:
		_load_table_columns(table, database_cursor)

	_load_columns_references(context, database_cursor)

	database_cursor.close()
	return context


def _load_tables(context, database_cursor):
	database_cursor.execute(TABLES_QUERY)
	tables = database_cursor.fetchall()

	for i in tables:
		database_cursor.execute(PRIMARY_KEY_QUERY,(i[0],))
		primary_key = _format_primary_key(database_cursor.fetchall())
		new_table = Table(i[0],primary_key)
		context.add_table(new_table)

def _format_primary_key(raw_query_response):
	pk_list = []
	for element in raw_query_response:
		pk_list.append(element[0])
	pk_formatted = tuple(pk_list)
	return pk_formatted

def _load_table_columns(table, database_cursor):
	database_cursor.execute(COLUMN_TYPE_QUERY,(table.name,))
	columns_types = database_cursor.fetchall()
	for column_and_type in columns_types:
		column_name = column_and_type[0]
		column_type = column_and_type[1]
		new_column = Column(column_name,column_type)
		table.add_column(new_column)


def _load_columns_references(context, database_cursor):
	for table in context.tables:
		for key, column in table.columns.items():
			database_cursor.execute(REFERENCE_QUERY,(table.name,column.name))
			refq = database_cursor.fetchall()
			reference = None
			if (len(refq) == 1):
				target_table = refq[0][4]
				target_column = refq[0][5]
				reference = (target_table,target_column)
			column.add_reference(reference)