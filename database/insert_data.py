from database.connect import c_engine
from parse import dates
import pymysql
from database import get_data
import datetime


def insert_category(category_code, category_name):
    connection = engine.connect()
    query = f"INSERT INTO f2connection_categories (category_code,category_name) VALUES ('{category_code}','{category_name}')"
    connection.execute(query)
    connection.close()


def insert_lot_price(lot, system, price_id, landed):
    connection = engine.connect()
    query = f'''INSERT INTO 
                f2connection_pricedlots (lot, system, price_id, landed) 
                VALUES ('{lot}','{system}','{price_id}','{landed}')'''
    connection.execute(query)
    connection.close()



def insert_weekly_price(system, week, year, assortment_code, price):
    connection = engine.connect()
    assortment_code = assortment_code.replace("'", "''")
    if price:
        query = f'''INSERT INTO 
                    f2connection_weeklyprices (week, year, assortment_code, price, system) 
                    VALUES ('{week}','{year}','{assortment_code}','{price}','{system}')'''
    else:
        query = f'''INSERT INTO 
                            f2connection_weeklyprices (week, year, assortment_code, system) 
                            VALUES ('{week}','{year}','{assortment_code}','{system}')'''
    connection.execute(query)
    query = "SELECT currval('f2connection_weeklyprices_id_seq');"
    a = connection.execute(query).fetchone()[0]

    connection.close()
    return a


def escape_text(text):
    return pymysql.escape_string(text).replace(':', '\:')


def insert_assortment(assortment_code, system, grade, colour, category_code, category_name, name):
    connection = engine.connect()
    query = f'''INSERT INTO 
                        f2connection_assortment(assortment_code, system, grade, colour, category_code_id, category_name, name) 
                        VALUES ( %s,%s,%s,%s,%s,%s,%s)'''
    connection.execute(query, (assortment_code, system, grade, colour, category_code, category_name, name))
    connection.close()

def insert_items_in_location(system, location, lot_nums):
    connection = engine.connect()
    for lot_num in lot_nums:
        query = f'''
        INSERT INTO f2connection_itemsinlocation (system, location, lots_id)
        SELECT   f2connection_pricedlots.system, %s, f2connection_pricedlots.id
        FROM f2connection_pricedlots
        WHERE system= %s AND lot=%s;
        '''
        connection.execute(query, (location,system, lot_num))
    connection.close()


    connection = engine.connect()

    # '''assortment_code = escape_text(assortment_code)
    # colour = escape_text(colour)
    # category_name = escape_text(category_name)
    # name = escape_text(name)
    # engine = c_engine()

    # connection = engine.connect()
    # query = f'''INSERT INTO
    #                f2connection_assortment (assortment_code, system, grade, colour,  category_code_id, category_name, name)
    #                VALUES ('{assortment_code}', '{system}', '{grade}', '{colour}',  '{category_code}', '{category_name}', '{name}')'''
    # connection.execute(query)
    # connection.close()


def insert_purchase_lots(lots):

    for lot_num in lots:
        data = lots[lot_num]
        exists = get_data.get_purchse_lot(system, data['lot'])

        if not exists:
            engine = c_engine()
            connection = engine.connect()
            query = '''INSERT INTO f2connection_purchases (system, purchase_date, lot,landed_price,supplier_code) VALUES (%s,%s,%s,%s,%s)'''
            connection.execute(query,(data['system'],dates.get_database_date(data['purchase_date']),data['lot'], data['landed_price'], data['supplier_code']))
            connection.close()




def insert_cmd_purchase_dates(purchase_date):
    connection = engine.connect()
    query = f"INSERT INTO f2connection_cmdpurchasedates (purchase_date) VALUES ('{purchase_date}')"
    connection.execute(query)
    connection.close()


def insert_command(command, reference, state, system):
    connection = engine.connect()
    if reference:
        query = f'''INSERT INTO f2connection_commands (command, reference, status, system)
        VALUES ('{command}','{reference}','{state}','{system}')'''
    else:
        query = f'''INSERT INTO f2connection_commands (command, reference, status, system)
        VALUES ('{command}',NULL,'{state}','{system}')'''

    connection.execute(query)
    connection.close()


def bulk_insert_command(data):
    connection = engine.connect()
    for d in data:
        command, reference, state, system = d
        if reference:
            query = f'''INSERT INTO f2connection_commands (command, reference, status, system)
            VALUES ('{command}','{reference}','{state}','{system}')'''
        else:
            query = f'''INSERT INTO f2connection_commands (command, reference, status, system)
            VALUES ('{command}',NULL,'{state}','{system}')'''
        connection.execute(query)
    connection.close()



def insert_open_lines(system, data_list):
    connection = engine.connect()

    for data in data_list:
        query = f''' 
        INSERT INTO f2connection_openorders (system, category, variety, colour,grade, client_code, order_date, 
        quantity, supplier_code, standing, comment, updated)  
        VALUES 
        ('{system}', %s, %s, %s, %s,%s, '{data['order_date']}', '{data['quantity']}', 
        '{data['supplier_code']}', '{data['standing']}',  %s, '{datetime.datetime.now()}')
        
        '''
        connection.execute(query, (data['category'], data['variety'],data['colour'],data['grade'],data['client_code'], data['comment']))
    connection.close()

def insert_last_done(system,action, reference):
    connection = engine.connect()
    time_done = datetime.datetime.now(datetime.timezone.utc)
    query = ''' 
    INSERT into f2connection_lastdone (system, action, time_done, reference)
    VALUES
        (%s, %s,%s,%s)
    '''
    connection.execute(query, (system, action, time_done, reference))


engine = c_engine()
system = 'f2_canada_real'
location = 'on'
lot_num = '639765'
