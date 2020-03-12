from navigation import traverse
from parse import parse, dates, lots
from interface import keyboard, window
import time, datetime
from database import update_data, get_data, insert_data



def get_virtual_purchase_todo():
    purchase =  get_data.get_virtual_purchases_unentered()
    if purchase:
        return purchase[-2]
    return None




##### Availability
def set_availability_dates(from_date,to_date, cut_off_start_date,cut_off_start_time, cut_off_date,cut_off_time):
    time.sleep(1)
    window.drag_window()

    if not verify((('Available', 22, 54), ('Visible', 25, 56))):
        time.sleep(1)
        if not verify((('Available', 22, 54), ('Visible', 25, 56))):
            print("sent")
            keyboard.command("INSERT")

    keyboard.command("F6")

    for d in (from_date,to_date):
        keyboard.write_text(d)
        keyboard.command("enter")
        keyboard.write_text('0000')
        keyboard.command("enter")

    keyboard.write_text(cut_off_start_date)
    keyboard.command("enter")
    keyboard.write_text(cut_off_start_time)
    keyboard.command("enter")
    keyboard.write_text(cut_off_date)
    keyboard.command("enter")
    keyboard.write_text(cut_off_time)
    keyboard.command("enter")
    keyboard.command("enter")

    keyboard.f11()



##########


### virtual Purchasing

def enter_virtual_purchase(purchase_order_id):

    id, supplier_code, purchase_date, end_date, visible_from, visible_to, system  = get_data.get_virtual_purchase_order(
        purchase_order_id)
    purchase_date = dates.get_menu_date(purchase_date)
    end_date = dates.get_menu_date(end_date)
    visible_from_date = dates.get_menu_date(visible_from)
    visible_from_time = dates.get_time(visible_from)
    visible_to_date= dates.get_menu_date(visible_to)
    visible_to_hours = dates.get_time(visible_to)
    traverse.main_menu_purchase_default_insert_virtual_purchase_flowers_date(system, purchase_date)
    set_availability_dates(purchase_date, end_date, visible_from_date, visible_from_time, visible_to_date, visible_to_hours)
    keyboard.command('insert')
    keyboard.f12()
    keyboard.command('f10')
    purchases = get_data.get_virtual_purchases_from_order(id)
    for purchase in purchases:
        print(purchase)
        p_id, code, quantity, packing, fob, landed, order_id, entered = purchase
        if not entered:
            enter_purchase_normal(code, str(fob), str(landed), str(quantity), str(packing), supplier_code)

    update_data.update_purchase_orders_mark_entered(id,True)









#####/virtual Purchasing
def verify(points):

    time.sleep(1)
    screen = parse.process_scene(window.get_window())
    for p in points:
        if not p[0] in screen[p[1]][p[2]:]:
            return False
    return True



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
    supplier_code = lot_main['supplier_code']
    if not supplier_code or supplier_code[0] in ('M', '1') and 'f2_canada' in system:
        return False
    data = lots.get_lot_info_purchase(lot_number, purchase_date, supplier_code)
    keyboard.f12()
    return data


def update_time_since_last_report(system, purchase_date):
    reference = dates.get_database_date(purchase_date)
    action = "input_purchase"
    if get_data.get_time_since_report(system, action, reference):
        update_data.update_last_done(system, action, reference)
    else:
        insert_data.insert_last_done(system, action, reference)


def update_purchases(system, purchase_date):
    data = get_input_purchase_lots(system, purchase_date)
    if data:
        insert_data.insert_purchase_lots(data)
        update_data.update_unmatched_purchases()
        null_lots = get_data.get_purchases_assortment_null(system)
        for lot in null_lots:
            print(lot, purchase_date.date(), lot == purchase_date.date())
            if lot[1] == purchase_date.date():
                data = get_lot_data(lot, system)
                if data:
                    update_data.update_purchases_assortment(system, data['lot_number'], data['assortment_code'],
                                                            data['supplier_code'])
    update_time_since_last_report(system, purchase_date)
    return True


def get_time_since_last_report(system, day):
    reference = dates.get_database_date(day)
    action = "input_purchase"
    report_time = get_data.get_time_since_report(system, action, reference)
    if report_time:
        return datetime.datetime.now(datetime.timezone.utc) - report_time


def is_purchase_day_due(system, day, distance):
    time = get_time_since_last_report(system, day)
    if not time:
        return True
    hours = abs(distance)
    if hours == 0:
        hours = 1

    if time > datetime.timedelta(hours=hours):
        return True
    return False

def enter_purchase_normal(code, fob, landed, quantity, packing, supplier):
    keyboard.command('f10')
    keyboard.write_text(code)
    keyboard.enter()
    keyboard.write_text(fob)
    keyboard.enter()
    keyboard.write_text(landed)
    keyboard.enter()
    keyboard.write_text(quantity)
    keyboard.enter()
    keyboard.write_text(packing)
    keyboard.enter()
    keyboard.write_text(supplier)
    keyboard.f11(2)




if __name__ == '__main__':
    system = 'f2_canada_real'
    # data = get_lot_data(['574399', dates.menu_date('03/01/19')], system)
    # update_data.update_purchases_assortment(system, data['lot_number'], data['assortment_code'])
    # update_purchases(system, dates.menu_date('31/01/20'))

    # update_purchases(system, '19/12/19')
    #update_data.update_purchase_orders_mark_entered(11, False)
    window.get_window()
    print(get_virtual_purchase_todo())
    #enter_virtual_purchase(259)
    #window.get_window()

    #enter_purchase_normal('tecligpi+r', '.43', '.43', '5', '100', 'CASPFL')


