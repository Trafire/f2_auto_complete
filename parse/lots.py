import time
from interface import window
from interface import keyboard
from database import get_data
import parse

try:
    from parse import dates
except:
    import dates


lot_reference = [
    {'data_point': 'assortment_code', 'text': 'Ofsht:', 'length': 12},
    {'data_point': 'purchase_date', 'text': 'Inkoopdatum          :', 'length': 12},
    {'data_point': 'lot_number', 'text': 'Intern partijnummer  :', 'length': 12},
    {'data_point': 'grade', 'text': 'Lengte           :', 'length': 12},
    {'data_point': 'colour', 'text': 'Kleur            :', 'length': 4},
    {'data_point': 'supplier_code', 'text': 'Aanvoercode          :', 'length': 12},
    {'data_point': 'supplier_code', 'text': 'Aanvoercode          :', 'length': 12},
    {'data_point': 'category_num', 'text': 'Agrp: ', 'length': 5},
    {'data_point': 'landed_price', 'text': 'Left in stock    :', 'length': 16},
]

def get_landed(s):
    if s:
        return s[s.find("(") + 1:s.find(")")].replace(',','.')
    return '0.00'

def get_category_name(num):
    return get_data.get_category_name(num)


def get_buying_price():
    pass


def get_article_name(category):
    if category:
        text = parse.get_parsed_screen_body()[0].split('║')[-1][:-1]
        if text == '':
            text = parse.get_parsed_screen_body()[0].split('║')[-2][:-1]
        if '<' in text:
            end = text.index('<')
            text = text[:end]
        text = text[len(category):]
        return text.strip()
    return None


def find_text_end(screen, reference):
    text = reference['text']
    length = reference['length']
    if text in screen:
        index = screen.index(text) + len(text)
        return screen[index: index + length].strip()
    #print(reference, 'failed')
    return False

def check_complete(lot_data):
    #print(lot_data)
    for key in lot_data:
        if key != 'colour' and not lot_data[key]:
            print('key',key)
            return False
    return True

def get_lot_info(attempt = 0):
    keyboard.command(('shift', 'f10'))
    if attempt > 4:
        return False
    print(f"attemtpt {attempt}")
    screen = window.get_window()
    lot_data = {}
    for reference in lot_reference:
        lot_data[reference['data_point']] = find_text_end(screen, reference)

    if not lot_data['assortment_code']:
        return get_lot_info(attempt + 1)
    lot_data['catgeory'] = get_category_name(lot_data['category_num'])
    print(lot_data['catgeory'])
    lot_data['name'] = get_article_name(lot_data['catgeory'])
    try:
        lot_data['purchase_date'] = dates.lot_date(lot_data['purchase_date'])
    except:
        return get_lot_info(attempt + 1)
    lot_data['landed_price'] = get_landed(lot_data['landed_price'])
    if not lot_data['landed_price']:
        lot_data['landed_price'] = '0.01'

    if check_complete(lot_data):
        return lot_data
    return get_lot_info(attempt + 1)

def get_lot_info_assortment(attempt = 0):
    keyboard.command(('shift', 'f10'))
    if attempt > 20:

        return False
    #print(f"attemtpt {attempt}")
    screen = window.get_window()
    lot_data = {}
    for reference in lot_reference:
        try:
            lot_data[reference['data_point']] = find_text_end(screen, reference)
        except:
            pass
    if not lot_data['assortment_code']:
        return get_lot_info_assortment(attempt + 1)
    lot_data['catgeory'] = get_category_name(lot_data['category_num'])
    lot_data['name'] = get_article_name(lot_data['catgeory'])
    return lot_data

def get_lot_info_purchase(lot_number, purchase_date,supplier_code, attempt = 0):
    keyboard.command(('shift', 'f10'))
    if attempt > 4:
        return False
    screen = window.get_window()
    lot_data = {}

    for reference in lot_reference:
        lot_data[reference['data_point']] = find_text_end(screen, reference)
    if not lot_data['assortment_code']:
        return get_lot_info_purchase(purchase_date, lot_number,supplier_code, attempt + 1)
    lot_data['catgeory'] = get_category_name(lot_data['category_num'])

    lot_data['name'] = get_article_name(lot_data['catgeory'])
    lot_data['landed_price'] = get_landed(lot_data['landed_price'])
    lot_data['purchase_date'] = purchase_date
    lot_data['supplier_code'] = supplier_code
    if not lot_data['lot_number']:
        lot_data['lot_number'] = lot_number
    if check_complete(lot_data):
        return lot_data
    return get_lot_info_purchase(lot_number, purchase_date,supplier_code, attempt + 1)


def get_recommended_price(attempt=0):
    for i in range(20):
        screen = window.get_window()
        text = '1N║Flowers C&C'
        if text in screen:
            start = screen.index(text) + 37
            end = start + 6
            return screen[start:end].replace(',','.').strip()
        time.sleep(.1)
    return False
