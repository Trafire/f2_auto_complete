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
    print("inserted", lot, price_id)


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
        print(data)
        {'system': 'f2_canada_real', 'purchase_date': '14/01/20', 'lot': '646490', 'landed_price': '2.88',
         'supplier_code': 'CASELM'}
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

#insert_assortment('ealnicep0', 'f2_canada_real', '80', 'PID', '3251',  ' Alstro SA', 'Nice')
#insert_week_done(system,2020, 3)
#data = {'orderid': 'ShrubsPussy WillowBR100CABRAN', 'category': 'Shrubs', 'variety': "Pussy Willow", 'colour': 'BR', 'grade': '100', 'client_code': 'BEYOND', 'order_date': datetime.datetime(2020, 1, 20, 0, 0), 'quantity': 4, 'supplier_code': 'CABRAN', 'standing': 'False', 'comment': ''}
#insert_open_lines(system, [data])
#data = {'orderid': 'ShrubsPussy WillowBR100CABRAN', 'category': 'Shrubs', 'variety': "Pussy 'Willow", 'colour': 'BR', 'grade': '100', 'client_code': 'BEYOND', 'order_date': datetime.datetime(2020, 1, 20, 0, 0), 'quantity': 4, 'supplier_code': 'CABRAN', 'standing': 'False', 'comment': ''}
#insert_open_lines(system, [data])
# insert_lot_price(641632, system, 2)
# print(insert_weekly_price(system, 52, 2019, 'appl6',  .59))


