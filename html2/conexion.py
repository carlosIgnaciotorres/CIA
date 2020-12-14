import sqlite3

# El \ se conoce como caracter de escape, se usa para construir códigos especiales
# \n, \t, C:\sqlite3\db\c03.db  ==> \s    \d     \c
# \\  ==> C:\sqlite3\db\c03.db
# /sqlite3/db/c03.db
#
def ejecutar_consulta_sel(sql,datos=None):
    # try:
        #print(f"{sql} - {datos}")
        with sqlite3.connect('cia.db') as con:
            cur = con.cursor()                  # Crea un cursor (un lugar para almacenar los resultados de la consulta)
            if datos!=None:
                sal = cur.execute(sql,datos)
            else:
                sal = cur.execute(sql)
            if sal!=None:
                sal = sal.fetchall()            # Recupera todos los resultados de la consulta (recordset - resultset)
    # except:
        # sal = None
        return sal

def ejecutar_consulta_acc(sql,datos=None):
    try:
        with sqlite3.connect('cia.db') as con:
            cur = con.cursor()                  # Crea un cursor (un lugar para almacenar los resultados de la consulta)
            if datos!=None:
                sal = cur.execute(sql,datos)
            else:
                sal = cur.execute(sql)
            con.commit()
    except:
        sal = 0
    return sal