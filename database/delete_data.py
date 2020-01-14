from database.connect import c_engine
import datetime
import json

def delete_open_lines(system, date):
    engine = c_engine()
    connection = engine.connect()
    query = f'''
    DELETE FROM f2connection_openorders
    WHERE 
    order_date=%s and system=%s
    '''
    connection.execute(query, (date,system))
    connection.close()

