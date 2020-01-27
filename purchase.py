from navigation import traverse
from parse import parse, dates, lots
from interface import keyboard, window
import time, datetime
from database import update_data, get_data, insert_data


def get_input_purchase_lots(system, purchase_date):
    attempts = 0
    lots = {}
    if traverse.main_menu_purchase_default_input_purchases_flowers_date(system, purchase_date):
        while attempts < 5:
            try:
                old_lot_length = len(lots)
                lots.update(parse.get_input_purchase_lots(system, purchase_date))
                new_lot_length = len(lots)
                if old_lot_length == new_lot_length:
                    attempts += 1
                    keyboard.command('pagedown')
                else:
                    attempts = 0

            except:
                attempts += 1
    return lots


def get_lot_data(lot, system):
    lot_number = lot[0]
    purchase_date = lot[1]
    window.drag_window()
    keyboard.command("f7")
    keyboard.write_text(lot_number)
    keyboard.enter()
    for i in range(5):
        try:
            lot_main = parse.get_input_purchase_lots(system, purchase_date)
            break
        except:
            lot_main = False
            time.sleep(.1)
    if not lot_main or lot_number not in lot_main:
        return False
    lot_main = lot_main[lot_number]
    print(45, lot_main)
    supplier_code = lot_main['supplier_code']
    print(47, supplier_code)
    if not supplier_code or supplier_code[0] in ('M','1') and 'f2_canada' in system:
        return False
    print(lot_number, purchase_date, supplier_code)
    data = lots.get_lot_info_purchase(lot_number, purchase_date, supplier_code)
    print(data)
    keyboard.f12()
    return data

def update_time_since_last_report(system, purchase_date):
    reference = dates.get_database_date(purchase_date)
    action = "input_purchase"
    if get_data.get_time_since_report(system, action, reference):
        update_data.update_last_done(system, action, reference)
    else:
        insert_data.insert_last_done(system,action, reference)

def update_purchases(system, purchase_date):
    data = get_input_purchase_lots(system, purchase_date)
    if data:
        insert_data.insert_purchase_lots(data)
        update_data.update_unmatched_purchases()
        null_lots = get_data.get_purchases_assortment_null(system)
        for lot in null_lots:
            data = get_lot_data(lot, system)
            print(data)
            if data:
                update_data.update_purchases_assortment(system, data['lot_number'], data['assortment_code'],
                                                        data['supplier_code'])
    update_time_since_last_report(system,purchase_date )
    return True

def get_time_since_last_report(system, day):
    reference = dates.get_database_date(day)
    action = "input_purchase"
    report_time = get_data.get_time_since_report(system, action, reference)
    if report_time:
        return datetime.datetime.now(datetime.timezone.utc) - report_time


def is_purchase_day_due(system,day, distance):
    time = get_time_since_last_report(system, day)
    if not time:
        return True
    hours = abs(distance)
    if time > datetime.timedelta(hours=hours):
        return True
    return False

if __name__ == '__main__':
    system = 'f2_canada_real'
    # data = get_lot_data(['574399', dates.menu_date('03/01/19')], system)
    # print(data)
    # update_data.update_purchases_assortment(system, data['lot_number'], data['assortment_code'])
    update_purchases(system, dates.menu_date('31/01/20'))

    # update_purchases(system, '19/12/19')
