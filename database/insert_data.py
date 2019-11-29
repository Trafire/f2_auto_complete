from database.connect import c_engine
from database import connect
import pymysql

table = 'f2connection_assortment'
Assortment = connect.get_base_class(c_engine(), table)

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
    return pymysql.escape_string(text).replace(':','\:')

def insert_assortment(assortment_code, system, grade, colour, category_code, category_name, name):

    session = connect.get_session()
    session.add(
    Assortment(assortment_code=assortment_code, system=system, grade=grade, colour=colour,
               category_code_id=category_code, category_name=category_name, name=name)
    )
    session.commit()

    #'''assortment_code = escape_text(assortment_code)
    #colour = escape_text(colour)
    #category_name = escape_text(category_name)
    #name = escape_text(name)
    #engine = c_engine()

    #connection = engine.connect()
    #query = f'''INSERT INTO
    #                f2connection_assortment (assortment_code, system, grade, colour,  category_code_id, category_name, name)
    #                VALUES ('{assortment_code}', '{system}', '{grade}', '{colour}',  '{category_code}', '{category_name}', '{name}')'''
    #connection.execute(query)
    #connection.close()



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
# insert_lot_price(641632, system, 2)
# print(insert_weekly_price(system, 52, 2019, 'appl6',  .59))
