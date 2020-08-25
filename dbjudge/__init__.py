"""Dbjudge is a module that manage SQL queries questions
and answers about databases. It also manages the connection with the databases
and offers random data generation for test answers against the correct answer."""
import psycopg2

from dbjudge import squema_recollector
from dbjudge import filler
from dbjudge.structures.table import Table
from dbjudge.structures.column import Column
from dbjudge.structures.context import Context
