import psycopg2

import squemaGetter
import filler
from structures import Table, Column, Context

conn = psycopg2.connect(host="127.0.0.1", dbname="tfg_test", user="conexion", password="plsL3tM3in")
context = squemaGetter.create_context(conn)
#ZONA DE DEPURACION
for t in context.tables:
    print("#################")
    print("*******"+t.name+"*********")
    print(t.primary_key)
    for c in t.columns:
        print(c.name+"\t"+c.ctype+"\t"+str(c.table_reference))
print("###################")

filler.generate_fake_data(context,conn)
conn.close()