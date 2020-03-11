from database.connect import c_engine
import json
import datetime


def update_landed(lot, system, landed):
    connection = engine.connect()
    query = f'''
    UPDATE f2connection_pricedlots
        SET landed = {landed}
        WHERE lot='{lot}' and system = '{system}';
    '''
    connection.execute(query)
    connection.close()


def update_command_status(id, status):
    connection = engine.connect()
    query = f'''
        UPDATE f2connection_commands
            SET status = '{status}'
            WHERE id={id};'''

    connection.execute(query)
    connection.close()


def update_unmatched_purchases():
    connection = engine.connect()
    query = f'''
        UPDATE f2connection_purchases
            SET assortment_code = f2connection_weeklyprices.assortment_code
            FROM f2connection_weeklyprices, f2connection_pricedlots
            WHERE f2connection_purchases.lot=f2connection_pricedlots.lot and f2connection_purchases.system = f2connection_pricedlots.system and f2connection_pricedlots.price_id= f2connection_weeklyprices.id;
        '''
    connection.execute(query)
    connection.close()


def update_purchases_assortment(system, lot, assortment_code, supplier):
    connection = engine.connect()

    query = f'''
            UPDATE f2connection_purchases
                SET assortment_code = %s, supplier_code = %s
                WHERE lot=%s and system=%s;'''
    connection.execute(query,(assortment_code, supplier, lot,system))
    connection.close()

def update_recommended_price(system, lot, price):
    connection = engine.connect()
    query = f'''
                UPDATE f2connection_pricedlots
                    SET recommended = %s
                    WHERE lot=%s and system=%s;'''
    connection.execute(query, (price, lot, system))
    connection.close()

def update_last_done(system, action, reference):
    connection = engine.connect()
    time_done = datetime.datetime.now(datetime.timezone.utc)
    query = f'''
    UPDATE f2connection_lastdone
    SET time_done=%s
    WHERE system=%s and action=%s and reference=%s
    '''
    connection.execute(query, (time_done, system, action, reference))
    connection.close()


def update_purchase_orders_mark_entered(order, status):
    connection = engine.connect()
    query = f'''
        UPDATE f2connection_virtualpurchases
        SET entered=%s
        WHERE virtual_purchase_order_id=%s
        '''
    connection.execute(query, (status, order))
    connection.close()

def update_weekly_price(system, year, week, code, price):
    connection = engine.connect()
    query = ''' 
    Update f2connection_weeklyprices
    SET price=%s
    WHERE system=%s AND year=%s AND week=%s AND assortment_code=%s
    '''
    connection.execute(query, (price, system, year, week, code))
    connection.close()


engine = c_engine()
