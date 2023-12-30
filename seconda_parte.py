import mysql.connector
def connessi_a_db():
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'localhost',
        'database': 'mydb',
        'raise_on_warnings': True
    }
    conn = mysql.connector.connect(**config)
    return conn
def chiud_connessi_a_db(conn):
    conn.close()
def v_temporanea(lista_tcin, lista_tcout,lista_id):
    databaseconn = connessi_a_db()
    try:
        query = "SELECT id_digitale, TC_in, TC_out FROM tc_intc_out"
        cursor = databaseconn.cursor()
        cursor.execute(query)
        risultati = cursor.fetchall()
        for i in risultati:
            TC_in, TC_out, id_digitale = i
            lista_tcin.append(TC_in)
            lista_tcout.append(TC_out)
            lista_id.append(id_digitale)
    except Exception as e:
        print(f"Errore: {e}")
    finally:
        if cursor:
            cursor.close()
        if databaseconn:
            databaseconn.close()
#visualizazzione del risultato
visualizzatcin = []
visualizzatcout = []
visualizzaid = []
v_temporanea(visualizzaid,visualizzatcin,visualizzatcout)
print(visualizzaid,'\n',visualizzatcin,'\n',visualizzatcout,'\n')

def aggiorna_tab():
   databaseconn = connessi_a_db()
   cursor = databaseconn.cursor()
   query_id = "SELECT DISTINCT id_digitale FROM tc_intc_out"
   cursor.execute(query_id)
   id_digitalelista = [result[0] for result in cursor.fetchall()]

   for id_digitale in id_digitalelista:
        query_select = "SELECT TC_in, TC_out FROM tc_intc_out WHERE id_digitale = %s"
        cursor.execute(query_select,(id_digitale,))
        righe_tcin_tcout = cursor.fetchall()

        for riga_tcin_tcout in righe_tcin_tcout:
            tc_in, tc_out = riga_tcin_tcout
            query_update = "UPDATE glc_t SET TC_in = %s, TC_out = %s WHERE id_digitale = %s AND TC_in IS NULL AND TC_out IS NULL LIMIT 1"
            cursor.execute(query_update,(tc_in, tc_out, id_digitale))
            databaseconn.commit()

        chiud_connessi_a_db(connessi_a_db())








