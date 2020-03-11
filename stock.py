from navigation import traverse
from navigation import lots as lots_navigation
from verification import f2_page, f2
from interface import keyboard
from parse import parse
from parse import lots, dates
from database import get_data, update_data
import pricing
from database import insert_data, delete_data
# import sqlalchemy
import closef2
import time
import threading

SHIPMENT_LOCATIONS = ['on', 'ec', 'col','nl','sale']
SHIPMENT_LOCATIONS = ['sale']
SELLING_LOCATIONS = ['sale']
COOLER_LOCATIONS = ['cel']
system = 'f2_canada_real'


# system = 'f2_canada_test'


def price_item(price):
    points = VERIFICATION['pricing']['f8-pricing']
    if True or f2.verify(points, attempts=10):
        keyboard.home()
        keyboard.enter()
        keyboard.paste_write(pricing.make_price_str(price))
        keyboard.f11()
        keyboard.f12()
    else:
        return False


def price_lot(system, lot, location, price, virtual=False):
    # window.drag_window()
    keyboard.command(('shift', 'F10'))
    if f2_page.verify_lot_info(lot, virtual=virtual):
        keyboard.f12()
        if change_price_level(system, location, 0):
            keyboard.command('f2')
            pricing.top_of_list()
            price_str = pricing.make_price_str(price)
            pricing.price_item(price)


def change_price_level(system, location, price_level):
    if f2_page.verify_per_location(location) and f2.verify_system(system):
        keyboard.command('F1')
        keyboard.write_text(str(price_level))
        keyboard.enter()
        return f2_page.verify_per_location_price_level(location, price_level)


def go_to_lot_virtual(system, location, lot, attempt=0):
    if f2_page.verify_per_location_virtual(location) and f2.verify_system(system):
        time.sleep(attempt * .05)
        keyboard.command('F7')
        keyboard.write_text(lot)
        keyboard.enter(2)
        keyboard.command(('shift', 'F10'))
        found = f2_page.verify_lot_info(lot, virtual=True)
        keyboard.command('f12')
        if not found and attempt < 5:
            found = go_to_lot_virtual(system, location, lot, attempt=attempt + 1)
        return found


def go_to_lot(system, location, lot, attempt=0):
    if f2_page.verify_per_location(location) and f2.verify_system(system):
        time.sleep(attempt * .05)
        keyboard.command('F7')
        keyboard.write_text(lot)
        keyboard.enter(2)
        keyboard.command(('shift', 'F10'))
        found = f2_page.verify_lot_info(lot)
        keyboard.command('f12')
        if not found and attempt < 5:
            found = go_to_lot(system, location, lot, attempt=attempt + 1)
        return found


def get_stock_lots(system, from_date, to_date, location, price_level, virtual=False):
    if traverse.stock_per_location_location(system, from_date, to_date, location, virtual=virtual):
        if change_price_level(system, location, price_level):
            old_screen = ''
            stock = {}
            while True:
                for i in range(10):
                    new_screen = parse.get_parsed_screen_body()
                    if new_screen != old_screen:
                        break
                    if i == 8:
                        return stock
                old_screen = new_screen
                stock.update(parse.get_stock_lots())
                keyboard.pgdn()
    return {}


def check_lot_priced(system, lot_data):
    lot = lot_data['lot']
    price = lot_data['price']
    # if get_data.check_priced_lots(lot, system):
    return str(get_data.get_lot_price_specials(lot, system)) == price.replace(',', '.')


def get_lots_to_price(location, from_date='00/00/00', to_date='31/12/30'):
    price_level = 1
    lots = get_stock_lots(system, from_date, to_date, location, price_level)

    to_price = []
    if lots:
        priced_lots = get_data.check_priced_lots_bulk(lots, system)
        for lot in lots:

            lot_data = lots[lot]
            if lot not in priced_lots or not check_lot_priced(system, lot_data):
                to_price.append(lot)
    return to_price


def get_lots_to_price_quick(location, from_date='00/00/00', to_date='31/12/30'):
    price_level = 1
    lots = get_stock_lots(system, from_date, to_date, location, price_level)
    to_price = []
    if lots:
        priced_lots = get_data.check_priced_lots_bulk(lots, system)
        for lot in lots:
            lot_data = lots[lot]
            if lot in priced_lots and not check_lot_priced(system, lot_data):
                to_price.append(lot)
    return to_price


def get_stock_information(system, location, lot, virtual=False):
    print(virtual)
    print(f"going to lot: {lot}")
    print(system, location, lot)
    if not virtual:
        go_to = go_to_lot
    else:
        go_to = go_to_lot_virtual
    if go_to(system, location, lot):
        print(f"at lot: {lot}")
        keyboard.command(('shift', 'f10'))
        info = lots.get_lot_info()
        keyboard.f12()
        return info
    return False


def clean_priced_lots(priced_lots, system):
    # check if NULL and remove
    return get_data.remove_null_priced_lots_specials(priced_lots, system)


'''
def price_location_virtual(system, from_date, to_date, location, price_level):
    # get list of articles already created to avoid double creation
    added_articles = set(get_data.get_articles_codes(system))
    stock_lots = get_stock_lots(system, from_date, to_date, location, price_level, virtual=True)
'''


def update_stock_info(lot_info, new_lot, added_articles, dsystem):
    assortment_code = lot_info['assortment_code']
    colour = lot_info['colour']
    category_code = lot_info['category_num']
    category_name = lot_info['catgeory']
    name = lot_info['name']
    grade = lot_info['grade']
    week = dates.get_pricing_week(lot_info['purchase_date'])
    year = dates.get_pricing_year(lot_info['purchase_date'])
    landed = lot_info['landed_price']

    # add article to db if it does not already exit
    if assortment_code not in added_articles:
        insert_data.insert_assortment(assortment_code, system, grade, colour, category_code, category_name,
                                      name)
        added_articles.add(assortment_code)
    try:
        insert_data.insert_weekly_price(system, week, year, assortment_code, None)
    except:
        pass
    result = get_data.check_assortment_price(assortment_code, week, year, system)
    id, price = result

    insert_data.insert_lot_price(new_lot, dsystem, id, landed)


def price_location_quick(system, from_date, to_date, location, price_level, virtual=False):
    # get list of articles already created to avoid double creation
    dsystem = system
    if virtual:
        dsystem = system + '_virtual'
    added_articles = set(get_data.get_articles_codes(system))
    stock_lots = get_stock_lots(system, from_date, to_date, location, price_level, virtual=virtual)
    for s in stock_lots:
        print(s, stock_lots[s])
    if not stock_lots:
        delete_data.delete_items_in_location(dsystem, location)
        return False
    stock_lots_list = list(stock_lots.keys())
    print(stock_lots_list)
    new_lots = []
    if stock_lots_list:
        delete_data.delete_items_in_location(system, location)
        insert_data.threaded_insert(insert_data.insert_items_in_location, (system, location, stock_lots_list))
        new_lots = get_data.get_new_lots(dsystem, stock_lots_list)
    else:
        delete_data.delete_items_in_location(system, location)

    print('newlots', new_lots)

    for new_lot in new_lots:
        lot_info = get_stock_information(system, location, new_lot, virtual=virtual)
        print(new_lot, lot_info)


        if lot_info:
            update_recommended(system, new_lot)
            try:
                x = threading.Thread(target=update_stock_info, args=(lot_info, new_lot, added_articles, dsystem))
                x.start()
            except Exception as err:
                print(err)
                print('threading failed')
                update_stock_info(lot_info, new_lot, added_articles, dsystem)

    price_lots = clean_priced_lots(stock_lots_list, system)
    print(price_lots)
    print(stock_lots)

    for lot in price_lots:
        lot_num = lot['lot']
        price = lot['price']
        if lot_num in stock_lots and stock_lots[lot_num]['price'] == price:
            pass
        else:
            lot_info = get_stock_information(system, location, lot_num, virtual=virtual)
            price_lot(system, lot_num, location, price, virtual=virtual)

    '''# returns lots that either are NULL price or wrong price.
    to_price_lots = get_lots_to_price(location, from_date, to_date)
    to_price_lots = clean_priced_lots(to_price_lots, system)
    for lot in to_price_lots:
        lot_info = get_stock_information(system, location, lot)
        #if lot_info:
    '''


def price_location(system, from_date, to_date, location, price_level):
    to_price_lots = get_lots_to_price(location, from_date, to_date)
    added_articles = get_data.get_articles_codes(system)
    for lot in to_price_lots:

        lot_info = get_stock_information(system, location, lot)
        if lot_info:
            assortment_code = lot_info['assortment_code']
            colour = lot_info['colour']
            category_code = lot_info['category_num']
            category_name = lot_info['catgeory']
            name = lot_info['name']
            grade = lot_info['grade']
            week = dates.get_pricing_week(lot_info['purchase_date'])
            year = dates.get_pricing_year(lot_info['purchase_date'])
            landed = lot_info['landed_price']
            result = get_data.check_assortment_price(assortment_code, week, year, system)
            update_data.update_landed(lot, system, landed)
            if assortment_code not in added_articles:
                insert_data.insert_assortment(assortment_code, system, grade, colour, category_code, category_name,
                                              name)
            added_articles.append(assortment_code)
            if result:
                id, price = result
                if price:
                    price_lot(system, lot, location, price)
                    # try:
                    #    insert_data.insert_lot_price(lot, system, id)
                    #    update_data.update_landed(lot, system, landed)
                    # except:
                    #    pass
                try:
                    insert_data.insert_lot_price(lot, system, id, landed)
                except:
                    pass
            else:
                insert_data.insert_weekly_price(system, week, year, assortment_code, None)


def price_system():
    from_date = '00/00/00'
    to_date = '30/11/45'
    price_level = 1
    # price_location_quick(system, from_date, to_date, location, price_level)

    for location in SHIPMENT_LOCATIONS:
        print(f"location: {location}")

        price_location_quick(system, from_date, to_date, location, price_level, virtual=True)
        price_location_quick(system, from_date, to_date, location, price_level, virtual=False)
        update_recommended_stock_location(system, location)
        keyboard.command(('alt', 'f2'))
        keyboard.command('esc')
        keyboard.command('esc')


def get_recommended(lot_number):
    lots_navigation.close_pricing()
    if lots_navigation.go_to_price_lot(lot_number):
        price = lots.get_recommended_price()
        lots_navigation.close_pricing()
        return price
    else:
        lots_navigation.close_pricing()
        return False

def update_recommended(system, lot_number):
    price =  get_recommended(lot_number)
    print(lot_number, price)
    if price:
        update_data.update_recommended_price(system,lot_number,price)
        return True

def update_recommended_stock_location(system, location):
    from_date = '00/00/00'
    to_date = '07/02/45'

    price_level = 1
    stock_lots = list(get_stock_lots(system, from_date, to_date, location, price_level).keys())
    stock_lots = get_data.get_null_recommended(system, stock_lots)
    for l in stock_lots:
        update_recommended(system, str(l))


if __name__ == "__main__" :
    from_date = '00/00/00'
    to_date = '07/02/45'
    price_level = 1
    location = 'sale'
    lot = '650878'
    # print(go_to_lot_virtual(system,location,'650743'))
    # lots = get_lots_to_price(location, from_date, to_date)
    # print(lots)
    # price_location_quick(system, from_date, to_date, location, price_level)
    # stock_lots = 6480(system, from_date, to_date, location, price_level, virtual=False)
    #lot_info = get_stock_information(system, location, lot, virtual=False)
    #lot_info = get_stock_information(system, location, '653637', virtual=True)
    #print(lot_info)
    #price_system(virtual=True)
    while True:

        price_system()
    # print(set(get_data.get_articles_codes(system)))

    #print(f2_page.verify_lot_info(lot, virtual=False))

    # print(go_to_lot_virtual(system, location, lot, attempt=0))

    # get_stock_information(system, 'on', '647804')
    # for location in SHIPMENT_LOCATIONS:
    #    print(f"location: {location}")
    #    price_location_quick(system, from_date, to_date, location, price_level)
    # pass

    # price_location_quick(system, from_date, to_date, location, price_level)
