from navigation import traverse
from verification import f2_page, f2
from interface import keyboard
from parse import parse
from parse import lots, dates
from database import get_data, update_data
import pricing
from database import insert_data
#import sqlalchemy
import closef2


SHIPMENT_LOCATIONS = ['ec', 'nl', 'col', 'on']
SELLING_LOCATIONS = ['sale']
COOLER_LOCATIONS = ['cel']
system = 'f2_canada_real'
#system = 'f2_canada_test'


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


def price_lot(system, lot, location, price):
    # window.drag_window()
    keyboard.command(('shift', 'F10'))
    if f2_page.verify_lot_info(lot):
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


def go_to_lot(system, location, lot):
    if f2_page.verify_per_location(location) and f2.verify_system(system):
        keyboard.command('F7')
        keyboard.write_text(lot)
        keyboard.enter(2)
        keyboard.command(('shift', 'F10'))
        found = f2_page.verify_lot_info(lot)
        keyboard.command('f12')
        return found


def get_stock_lots(system, from_date, to_date, location, price_level):
    if traverse.stock_per_location_location(system, from_date, to_date, location):
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
    return str(get_data.get_lot_price(lot, system)) == price.replace(',', '.')


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


def get_stock_information(system, location, lot):
    print(f"going to lot: {lot}")
    if go_to_lot(system, location, lot):
        print(f"at lot: {lot}")
        keyboard.command(('shift', 'f10'))
        info = lots.get_lot_info()
        keyboard.f12()
        return info
    return False


def clean_priced_lots(priced_lots, system):
    # check if NULL and remove
    return get_data.remove_null_priced_lots(priced_lots, system)


def price_location_quick(system, from_date, to_date, location, price_level):
    # get list of articles already created to avoid double creation
    added_articles = set(get_data.get_articles_codes(system))

    stock_lots = get_stock_lots(system, from_date, to_date, location, price_level)
    if not stock_lots:
        return False
    stock_lots_list = list(stock_lots.keys())
    new_lots = []
    if stock_lots_list:
        new_lots = get_data.get_new_lots(system, stock_lots_list)

    for new_lot in new_lots:
        lot_info = get_stock_information(system, location, new_lot)
        if lot_info:
            assortment_code = lot_info['assortment_code']
            colour = lot_info['colour']
            category_code = lot_info['category_num']
            category_name = lot_info['catgeory']
            name = lot_info['name']
            grade = lot_info['grade']
            week = dates.get_week(lot_info['purchase_date'])
            year = dates.get_year(lot_info['purchase_date'])
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
            insert_data.insert_lot_price(new_lot, system, id, landed)

    #price_lots = get_lots_to_price(location, from_date, to_date)
    price_lots = clean_priced_lots(stock_lots_list, system)
    for lot in price_lots:
        print(lot)
        lot_num = lot['lot']
        price = lot['price']
        if lot_num in stock_lots and stock_lots[lot_num]['price'] == price:
            pass
        else:


            lot_info = get_stock_information(system, location, lot_num)
            print(lot_info)
            price_lot(system, lot_num, location, price)





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
        print(lot)
        lot_info = get_stock_information(system, location, lot)
        if lot_info:
            assortment_code = lot_info['assortment_code']
            colour = lot_info['colour']
            category_code = lot_info['category_num']
            category_name = lot_info['catgeory']
            name = lot_info['name']
            grade = lot_info['grade']
            week = dates.get_week(lot_info['purchase_date'])
            year = dates.get_year(lot_info['purchase_date'])
            landed = lot_info['landed_price']
            result = get_data.check_assortment_price(assortment_code, week, year, system)
            update_data.update_landed(lot, system, landed)
            if assortment_code not in added_articles:
                '''try:
                    print('start pass')
                    insert_data.insert_assortment(assortment_code, system, grade, colour, category_code, category_name, name)
                    print('pass')
                except(sqlalchemy.exc.IntegrityError):
                    print("fail")'''
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

    # print('done')
    for location in SHIPMENT_LOCATIONS:
        print(f"location: {location}")
        price_location_quick(system, from_date, to_date, location, price_level)


# get_lots_to_price(location)
# print(f2_page.verify_lot_info('641632'))
# print(get_lots_to_price(location))

# price_lot(system, '641632', location, '4.19')

if __name__ == "__main__":
    from_date = '00/00/00'
    to_date = '30/11/45'
    price_level = 1
    #price_location_quick(system, from_date, to_date, location, price_level)

    #print('done')
    for location in SHIPMENT_LOCATIONS:
        print(f"location: {location}")
        price_location_quick(system, from_date, to_date, location, price_level)
        #pass

        #price_location_quick(system, from_date, to_date, location, price_level)


    # l = '639733'
    # print(get_stock_information(system, location, l))

    # l = get_lots_to_price_quick(location, from_date, to_date)
    # l.sort()
    # print(l)
    '''
    lot = '641913'
    lot_info = get_stock_information(system, location, lot)
    print(lot_info)
    assortment_code = lot_info['assortment_code']
    week = dates.get_week(lot_info['purchase_date'])
    year = dates.get_year(lot_info['purchase_date'])
    price = get_data.check_assortment_price(assortment_code, week, year, system)
    
    if price:
        if go_to_lot(system, location, lot):
            price_lot(system, lot, location, price)
    
    # data = get_stock_lots(system, from_date, to_date, location, price_level)
    # print(data)
    # price_location(system, from_date, to_date, location, price_level)
    
    
    
    l = get_stock_information(system, location, lot)
    print(l)
    
    data = get_stock_lots(system, from_date, to_date, location, price_level)
    print(data)
    print(len(data))
    to_price = []
    for d in data:
        lot_data = data[d]
        print(lot_data)
        if not check_lot_priced(system, lot_data):
            to_price.append(d)
    
        print(d, go_to_lot(system, location, d))
        print(lots.get_lot_info())
    
    print = to_price
    '''
