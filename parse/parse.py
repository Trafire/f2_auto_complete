from interface import window
# from autof2.readf2 import parse
import re


def get_parsed_screen():
    return process_scene(window.get_window())


def get_parsed_screen_body():
    return process_scene(window.get_window())[6:-4]


def process_scene(uscreen):
    for j in range(10):
        try:
            return uscreen.split('\r\n')
        except:
            uscreen = window.get_window()
    return None


def get_pricelist_categories_strings(uscreen):
    match_str = '║[0-9][0-9]' + "." * 23
    return re.findall(match_str, uscreen)


def get_pricelist_categories_dict(uscreen):
    cat_dict = {}
    categories = get_pricelist_categories_strings(uscreen)
    for c in categories:
        number = c[1:3]
        name = c[4:].rstrip()
        cat_dict[name] = number
    return cat_dict


def get_pricelist_categories_list(uscreen):
    cat = []
    categories = get_pricelist_categories_strings(uscreen)
    for c in categories:
        name = c[4:].rstrip()
        cat.append(name)
    cat.sort()
    return cat


def count_category(uscreen):
    match_str = '║[0-9][0-9].'
    items = re.findall(match_str, uscreen)
    return len(items)


def get_stock_locations():
    uscreen = window.get_window()
    match_str = '║[a-zA-Z][a-z]   ║'
    a = re.findall(match_str, uscreen)
    match_str = '║[a-zA-Z][a-z][a-z]  ║'
    a.extend(re.findall(match_str, uscreen))
    match_str = '║[a-zA-Z][a-z][a-z][a-z] ║'
    a.extend(re.findall(match_str, uscreen))
    for index in range(len(a)):
        a[index] = a[index].strip('║')
        a[index] = a[index].strip()
    return a


def get_stock_lots():
    uscreen = window.get_window()
    screen = process_scene(uscreen)
    data = {}
    for s in screen[6:-4]:
        row = s.split('║')
        if row[1].strip():
            lot = row[1].strip()[:-1]
            rdata = {'lot': lot,
                     'price': row[11].replace(',', '.').strip()}
            data[lot] = (rdata)
    return data

import time
def get_input_purchase_lots(system, purchase_date):
    time.sleep(.1)
    uscreen = window.get_window()
    screen = process_scene(uscreen)
    data = {}
    for s in screen[6:-4]:
        row = s.split('║')
        lot = row[1].strip()

        rdata = {
            'system': system,
            'purchase_date': purchase_date,
            'lot': lot,
            'landed_price': row[6].replace(',', '.').strip(),
            'supplier_code': row[8].strip()
        }
        if rdata['lot'].isdigit():
            data[lot] = (rdata)
    return data
if __name__ == '__main__':
    system = 'f2_canada_real'
    import dates
    data = get_input_purchase_lots(system, dates.menu_date('27/01/20'))
    for i in data:
        print(i, data[i])