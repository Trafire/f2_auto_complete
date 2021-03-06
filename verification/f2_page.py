import copy

from interface import window
from parse import parse
from verification import f2
from verification.reference import VERIFICATION


def verify_per_location(location):
    keyword = 'stock_per_location-flowers-location'
    window_data = copy.deepcopy(VERIFICATION['screens'][keyword])
    swaps = {
        '{location}': location,
    }

    for w in window_data:
        w['target'] = swap_values(swaps, w['target'])
    return f2.verify(window_data, 50)


def verify_per_location_virtual(location):
    keyword = 'virtual_stock_per_location-flowers-location'
    window_data = copy.deepcopy(VERIFICATION['screens'][keyword])
    swaps = {
        '{location}': location,
    }

    for w in window_data:
        w['target'] = swap_values(swaps, w['target'])
    return f2.verify(window_data, 50)


def verify_per_location_price_level(location, level, attempt=0):

    if attempt > 50:
        return False
    level = str(level)
    if level == '0':
        row = parse.process_scene(window.get_window())[4][55:-5].strip()
        print('row', row)
        if row == '' or row == 'Pricegroup :    0':
            print("TRUE")
            return True
        else:
            return verify_per_location_price_level(location, level, attempt + 1)

    keyword = "stock_per_location-flowers-location-price_level"
    window_data = VERIFICATION['screens'][keyword]
    swaps = {
        '{level}': level,
    }
    for w in window_data:
        w['target'] = swap_values(swaps, w['target'])
    return verify_per_location(location) and f2.verify(window_data, 50)


def verify_lot_info(lot_number, virtual=False):
    if virtual:
        screen = 'virtual_lot_info'
    else:
        screen = 'lot_info'

    window_data = copy.deepcopy(VERIFICATION['screens'][screen])
    swaps = {
        '{lot_number}': lot_number,
    }

    for w in window_data:
        w['target'] = swap_values(swaps, w['target'])
    return f2.verify(window_data, 10)


def swap_values(swaps, text):
    for s in swaps:
        if s in text:
            return text.replace(s, swaps[s])
    return text


if __name__ == '__main__':
    location = 'ec'
    level = '2'
    # cmd = verify_per_location_price_level(location, level)
    # print(cmd)
    # print(verify_lot_info('641921'))
    # print(verify_lot_info('641913'))

    a = f2.verify([{'target': 'Intern partijnummer  : 647801', 'location': (17, 97)}], 10)
    # b =  f2.verify([{'target': 'Intern partijnummer  : 647801', 'location': (18, 97)}], 10)

    print(a)

# [{'target': 'Inkooporder', 'location': (19, 97)}, {'target': 'Art. info', 'location': (5, 98)}, {'target': 'VBN', 'location': (8, 97)}, {'target': 'Intern partijnummer  : 639545', 'location': (18, 97)}]
