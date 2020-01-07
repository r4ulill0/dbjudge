import psycopg2

from dbjudge import squema_recollector
from dbjudge import filler
from dbjudge.structures.table import Table
from dbjudge.structures.column import Column
from dbjudge.structures.context import Context

# conn = psycopg2.connect(host="127.0.0.1", dbname="main_tfg",
#                         user="conexion", password="plsL3tM3in")
# with conn:
#     context = squema_recollector.create_context(conn)
#     # ZONA DE DEPURACION
#     for t in context.tables:
#         print("#################")
#         print("*******"+t.name+"*********")
#         print(t.primary_key)
#         for k, c in t.columns.items():
#             print(c.name+"\t"+c.ctype+"\t"+str(c.reference))
#     print("###################")

#     filler.generate_fake_data(context, conn)
