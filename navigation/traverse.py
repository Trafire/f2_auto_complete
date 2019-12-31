from interface import window, keyboard
from verification.reference import VERIFICATION
from verification import f2
from parse import parse, dates
import login
import time
import copy
import datetime


def traverse_menu(previous_menu, menu_str, system, attempt=0, ):
    if not f2.is_system_open(tries=25):
        login.sign_in_toronto(login.username, login.password, system)

    window_data = VERIFICATION['system'][system]

    if not f2.verify(window_data, attempts=50):
        login.sign_in_toronto(login.username, login.password, system)

    if attempt > 2:
        return False
    if previous_menu(system):
        window_data = VERIFICATION['screens'][menu_str]
        cmd = VERIFICATION['navigation'][menu_str]
        print(cmd)
        if '{' in cmd:
            keyboard.write_mix(cmd)
        else:
            keyboard.write_text(cmd)
        keyboard.enter(1)
        if not f2.verify(window_data, 50):
            return traverse_menu(previous_menu, menu_str, system, attempt=attempt + 1)
        return True
    return False


def main_menu_call(attempt=0):
    window_data = VERIFICATION['screens']['main_menu']
    if attempt > 20:
        return False
    if not f2.verify(window_data, 2):
        keyboard.f12(7)
        keyboard.write_text('n')
        keyboard.home(3)
        time.sleep(.01)
        return main_menu_call(attempt + 1)
    else:
        keyboard.home(3)
        return True


def main_menu(system):
    window_data = VERIFICATION['system'][system]
    if not f2.is_system_open(tries=25):
        login.sign_in_toronto(login.username, login.password, system)
    if not f2.verify(window_data, attempts=500):
        login.sign_in_toronto(login.username, login.password, system)
    main_menu_call()
    main_menu_call()
    return main_menu_call()


############## STOCK COMMANDS ######################
def main_menu_stock(system, attempt=0):
    return traverse_menu(main_menu, 'main_menu-stock', system, attempt=0)


def main_menu_stock_stock_per_location(system, attempt=0):
    keyword = 'main_menu-stock-stock_per_location'
    return traverse_menu(main_menu_stock, keyword, system, attempt=0)


def main_menu_stock_stock_per_location_edit_stock(system, attempt=0):
    keyword = 'main_menu-stock-stock_per_location-edit_stock'
    return traverse_menu(main_menu_stock_stock_per_location, keyword, system, attempt=0)


def main_menu_stock_stock_per_location_edit_stock_date(system, from_date, to_date, attempt=0):
    if attempt > 10:
        return False

    if type(from_date) == datetime.datetime:
        from_date = dates.get_menu_date(from_date)

    if type(to_date) == datetime.datetime:
        to_date = dates.get_menu_date(to_date)

    if main_menu_stock_stock_per_location_edit_stock(system, attempt=0):
        keyboard.write_text(from_date)
        keyboard.enter()
        keyboard.write_text(to_date)
        keyboard.enter()
        window_data = copy.deepcopy(VERIFICATION['screens']['main_menu-stock-stock_per_location-edit_stock-date'])
        swaps = {
            '{from_date}': from_date,
            '{to_date}': to_date,
        }
        for w in window_data:
            w['target'] = swap_values(swaps, w['target'])
        # print(window_data)
        if not f2.verify(window_data, 50):
            return main_menu_stock_stock_per_location_edit_stock_date(system, from_date, to_date, attempt + 1)
        else:
            return True
    return False


def main_menu_stock_stock_per_location_edit_stock_date_flowers(system, from_date, to_date, attempt=0):
    if attempt > 10:
        return False

    if type(from_date) == datetime.datetime:
        from_date = dates.get_menu_date(from_date)

    if type(to_date) == datetime.datetime:
        to_date = dates.get_menu_date(to_date)

    if main_menu_stock_stock_per_location_edit_stock_date(system, from_date, to_date, attempt=0):
        keyword = "main_menu-stock-stock_per_location-edit_stock-date-flowers"
        window_data = VERIFICATION['screens'][keyword]
        cmd = VERIFICATION['navigation'][keyword]
        keyboard.write_mix(cmd)
        keyboard.enter(1)
        if not f2.verify(window_data, 50):
            return main_menu_stock_stock_per_location_edit_stock_date_flowers(system, from_date, to_date, attempt + 1)
        else:
            return True
    return False


def get_actual_stock_locations(system, from_date, to_date, attempt=0):
    if attempt > 10:
        return False
    if main_menu_stock_stock_per_location_edit_stock_date_flowers(system, from_date, to_date, attempt=0):
        locations = parse.get_stock_locations()
        if len(locations) == 0:
            return get_actual_stock_locations(system, from_date, to_date, attempt + 1)
        return locations
    return False


def stock_per_location_location(system, from_date, to_date, location, attempt=0):
    if attempt > 10:
        return False
    if location in get_actual_stock_locations(system, from_date, to_date):
        keyword = 'stock_per_location-flowers-location'
        keyboard.write_text(location)
        keyboard.enter(2)
        window_data = copy.deepcopy(VERIFICATION['screens'][keyword])
        swaps = {
            '{location}': location,
        }
        for w in window_data:
            w['target'] = swap_values(swaps, w['target'])
        print(f"location is {location}: {window_data}")
        if not f2.verify(window_data, 100):
            return stock_per_location_location(system, from_date, to_date, location, attempt + 1)
        return True
    return False


def swap_values(swaps, text):
    for s in swaps:
        if s in text:
            return text.replace(s, swaps[s])
    return text


##### Maintenance Data Commands #####
def main_menu_maintainance_data(system, attempt=0):
    if attempt > 10:
        return False
    if main_menu(system):
        window_data = VERIFICATION['screens']['main_menu-maintenance_data']
        cmd = VERIFICATION['navigation']['main_menu-maintenance_data']
        keyboard.write_text(cmd)
        keyboard.enter(1)
        if not f2.verify(window_data, 50):
            return main_menu_maintainance_data(attempt + 1)
        return True
    return False


##### Maintenance Data > Price List Commands #####
def main_menu_maintainance_data_pricelists(system, attempt=0):
    return traverse_menu(main_menu_maintainance_data, 'main_menu-maintenance_data-pricelists', system, attempt=0)


def main_menu_maintainance_data_pricelists_edit_pricelist(system, attempt=0):
    menu_str = 'main_menu-maintenance_data-pricelists-edit_pricelist'
    return traverse_menu(main_menu_maintainance_data_pricelists,
                         menu_str,
                         system,
                         attempt=0)


def main_menu_maintainance_data_pricelists_edit_pricelist_flowers(system, attempt=0):
    menu_str = 'main_menu-maintenance_data-pricelists-edit_pricelist-flowers'
    f = main_menu_maintainance_data_pricelists_edit_pricelist
    return traverse_menu(f, menu_str, attempt=0)


def main_menu_maintainance_data_pricelists_edit_pricelist_flowers_select(price_list, date, system, attempt=0):
    menu_str = 'main_menu-maintenance_data-pricelists-edit_pricelist-flowers'
    f = main_menu_maintainance_data_pricelists_edit_pricelist
    if traverse_menu(f, menu_str, system, attempt=0):

        if date:
            keyboard.command(('shift', '3'))
            keyboard.write_text(date)
            keyboard.enter()
        keyboard.write_text(price_list)
        price_list_name = VERIFICATION['price_list'][price_list]['name']
        window_data = VERIFICATION['screens']['main_menu-maintenance_data-pricelists-edit_pricelist-flowers-select']
        window_data[1]['target'] = price_list_name
        if not f2.verify(window_data, 50):
            return False
        else:
            return True
    return False


def price_list_category(price_list, date, category):
    #
    price_list_name = VERIFICATION['price_list'][price_list]['name']
    window_data = VERIFICATION['screens']['main_menu-maintenance_data-pricelists-edit_pricelist-flowers-select']
    window_data[1]['target'] = price_list_name


########### Purchasing ##############

def main_menu_purchase(system, attempt=0):
    keyword = 'main_menu-purchase'
    return traverse_menu(main_menu, keyword, system, attempt=0)


def main_menu_purchase_default(system, attempt=0):
    keyword = 'main_menu-purchase-default'
    return traverse_menu(main_menu_purchase, keyword, system, attempt=0)



def main_menu_purchase_default_purchase_distribute(system, attempt=0):
    keyword = 'main_menu-purchase-default-purchase_distribute'
    return traverse_menu(main_menu_purchase_default, keyword, system, attempt=0)


def main_menu_purchase_default_purchase_distribute_flowers(system, attempt=0):
    keyword = 'main_menu-purchase-default-purchase_distribute_flowers'
    return traverse_menu(main_menu_purchase_default_purchase_distribute, keyword, system, attempt=0)

####### Purchase List #########



###############################

# to purchase menu
def main_menu_purchase_default_purchase_distribute_flowers_purchase(system, purchase_date, attempts=0):
    if type(purchase_date) == datetime.datetime:
        purchase_date = dates.get_menu_date(purchase_date)

    if main_menu_purchase_default_purchase_distribute_flowers(system):
        keyboard.write_text(purchase_date)
        keyboard.enter()
        keyboard.f11()


# to insert purchase

def main_menu_purchase_default_insert_virtual_purchase(system, attempts=0):
    keyword = 'main_menu-purchase-default_insert_virtual_purchase'
    return traverse_menu(main_menu_purchase_default, keyword, system, attempt=0)


def main_menu_purchase_default_insert_virtual_purchase_flowers(system, attempts=0):
    keyword = 'main_menu-purchase-default_insert_virtual_purchase_flowers'
    return traverse_menu(main_menu_purchase_default_insert_virtual_purchase, keyword, system, attempt=0)


def main_menu_purchase_default_insert_virtual_purchase_flowers_date(system, purchase_date, attempts=0):
    if main_menu_purchase_default_insert_virtual_purchase_flowers(system):
        keyboard.write_text(purchase_date)
        keyboard.enter()


# to input purchase

def main_menu_purchase_default_input_purchases(system, attempts=0):
    keyword = 'main_menu-purchase-default-input_purchases'
    return traverse_menu(main_menu_purchase_default, keyword, system, attempt=0)


def main_menu_purchase_default_input_purchases_flowers(system, attempts=0):
    keyword = 'main_menu-purchase-default-input_purchases-flowers'
    return traverse_menu(main_menu_purchase_default_input_purchases, keyword, system, attempt=0)


def main_menu_purchase_default_input_purchases_flowers_date(system, purchase_date, attempts=0):
    if type(purchase_date) in (datetime.datetime, datetime.date):
        purchase_date = dates.get_menu_date(purchase_date)

    if main_menu_purchase_default_input_purchases_flowers(system):
        keyboard.write_text(purchase_date)
        keyboard.enter()
        keyboard.shift_f11()
        keyboard.home(3)
        return True


## print(main_menu_maintainance_data_pricelists_edit_pricelist_flowers_select('051', '18/11/19', ))
# print(main_menu_maintainance_data_pricelists_edit_pricelist_flowers_select('051', '18/11/19', ))
# cmd = stock_per_location_location(system, '00/00/00', '31/12/30', 'col')
# cmd = main_menu_stock_stock_per_location_edit_stock(system)
# print(cmd)

if __name__ == '__main__':
    system = 'f2_canada_real'
    from_date = '00/00/00'
    to_date = '30/11/45'
    price_level = 1
    location = 'on'
    main_menu_stock_stock_per_location(system)
