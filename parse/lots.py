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
    return False

def check_complete(lot_data):
    for key in lot_data:
        if not lot_data[key]:
            print(lot_data[key])
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

    lot_data['name'] = get_article_name(lot_data['catgeory'])
    lot_data['purchase_date'] = dates.lot_date(lot_data['purchase_date'])
    lot_data['landed_price'] = get_landed(lot_data['landed_price'])
    if check_complete(lot_data):
        return lot_data
    return get_lot_info(attempt + 1)


