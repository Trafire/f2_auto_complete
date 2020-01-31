from database.connect import c_engine
import datetime
import json

def delete_open_lines(system, date):
    connection = engine.connect()
    query = f'''
    DELETE FROM f2connection_openorders
    WHERE 
    order_date=%s and system=%s
    '''
    connection.execute(query, (date,system))
    connection.close()

def delete_items_in_location(system, location):
    connection = engine.connect()
    query = f'''
        DELETE FROM f2connection_itemsinlocation
        WHERE 
        location =%s and system=%s
        '''
    connection.execute(query, (location, system))
    connection.close()

engine = c_engine()
system = 'f2_canada_real'
location = 'on'
