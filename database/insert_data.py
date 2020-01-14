from database.connect import c_engine
from database import connect
import pymysql
from database import get_data
#from datetime import datetime
import datetime
assortment_table = 'f2connection_assortment'
purchases_table = 'f2connection_purchases'
#Assortment = connect.get_base_class(c_engine(), assortment_table)
#Purchases = connect.get_base_class(c_engine(), purchases_table)


def insert_category(category_code, category_name):
    engine = c_engine()
    connection = engine.connect()
    query = f"INSERT INTO f2connection_categories (category_code,category_name) VALUES ('{category_code}','{category_name}')"
    connection.execute(query)
    connection.close()


def insert_lot_price(lot, system, price_id, landed):
    engine = c_engine()
    connection = engine.connect()
    query = f'''INSERT INTO 
                f2connection_pricedlots (lot, system, price_id, landed) 
                VALUES ('{lot}','{system}','{price_id}','{landed}')'''
    connection.execute(query)
    connection.close()
    print("inserted", lot, price_id)


def insert_weekly_price(system, week, year, assortment_code, price):
    engine = c_engine()
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
    assortment_code = assortment_code.replace("'", "''")
    session = connect.get_session()
    session.add(
        Assortment(assortment_code=assortment_code, system=system, grade=grade, colour=colour,
                   category_code_id=category_code, category_name=category_name, name=name)
    )
    session.commit()

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
    session = connect.get_session()
    for lot_num in lots:
        data = lots[lot_num]
        exists = get_data.get_purchse_lot(system, data['lot'])
        if not exists:
            # session.add(Purchases(lot=data['lot'], landed_price=data['landed_price'], supplier_code=data['supplier_code']))
            session.add(Purchases(**data))
    session.commit()


def insert_cmd_purchase_dates(purchase_date):
    engine = c_engine()
    connection = engine.connect()
    query = f"INSERT INTO f2connection_cmdpurchasedates (purchase_date) VALUES ('{purchase_date}')"
    connection.execute(query)
    connection.close()


def insert_command(command, reference, state, system):
    engine = c_engine()
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
    engine = c_engine()
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
    engine = c_engine()
    connection = engine.connect()

    for data in data_list:
        query = f''' 
        INSERT INTO f2connection_openorders (system, category, variety, colour, client_code, order_date, 
        quantity, supplier_code, standing, comment, updated)  
        VALUES 
        ('{system}', '{data['category']}', %s, %s, '{data['client_code']}', '{data['order_date']}', '{data['quantity']}', 
        '{data['supplier_code']}', '{data['standing']}',  %s, '{datetime.datetime.now()}')
        
        '''
        connection.execute(query, (data['variety'],data['colour'], data['comment']))
    connection.close()


''' inserts category names and codes into database
from interface import keyboard, window
from parse import parse
import time

def insert_to(answer):
    category_code, category_name = answer['category_code'], answer['category_name']
    if category_code and category_name:
        insert_category(category_code, category_name)

def find_text_end(screen, reference):
    text = reference['text']
    length = reference['length']
    if text in screen:
        index = screen.index(text) + len(text)
        return screen[index: index + length].rstrip()
    return False

def get_category():
    window.get_window()
    keyboard.f11(1)
    time.sleep(.1)
    screen = window.get_window()

    cat_name = "English    : "
    art = '(ArtGrp '
    d = [
        {'data_point': 'category_code', 'text': art, 'length': 4},
        {'data_point': 'category_name', 'text': cat_name, 'length': 30},
    ]
    answer = {}
    for reference in d:
        answer[reference['data_point']] = find_text_end(screen, reference)
    print(answer)
    keyboard.f12(1)
    keyboard.command('down')
    return answer

def update_categories():
    for i in range(300):
        answer = get_category()
        try:
            insert_to(answer)
        except:
            pass
    
        time.sleep(.1)
'''
# return bool(answer[0])
system = 'f2_canada_real'

#data = {'orderid': 'ShrubsPussy WillowBR100CABRAN', 'category': 'Shrubs', 'variety': "Pussy Willow", 'colour': 'BR', 'grade': '100', 'client_code': 'BEYOND', 'order_date': datetime.datetime(2020, 1, 20, 0, 0), 'quantity': 4, 'supplier_code': 'CABRAN', 'standing': 'False', 'comment': ''}
#insert_open_lines(system, [data])
#data = {'orderid': 'ShrubsPussy WillowBR100CABRAN', 'category': 'Shrubs', 'variety': "Pussy 'Willow", 'colour': 'BR', 'grade': '100', 'client_code': 'BEYOND', 'order_date': datetime.datetime(2020, 1, 20, 0, 0), 'quantity': 4, 'supplier_code': 'CABRAN', 'standing': 'False', 'comment': ''}
#insert_open_lines(system, [data])
# insert_lot_price(641632, system, 2)
# print(insert_weekly_price(system, 52, 2019, 'appl6',  .59))
