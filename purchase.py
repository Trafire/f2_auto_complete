from navigation import traverse
from parse import parse, dates, lots
from interface import keyboard, window


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
    window.drag_window()
    lot_number = lot[0]
    lot_main = parse.get_input_purchase_lots(system, '27/05/19')[lot_number]
    purchase_date = lot_main['purchase_date']
    supplier_code = lot_main['supplier_code']
    keyboard.command("f7")
    keyboard.write_text(lot)
    keyboard.enter()
    data = lots.get_lot_info_purchase(lot_number, purchase_date, supplier_code)
    keyboard.f12()
    return data


def update_purchases(system, purchase_date):
    data = get_input_purchase_lots(system, purchase_date)
    if data:
        insert_data.insert_purchase_lots(data)
        update_data.update_unmatched_purchases()
        null_lots = get_data.get_purchases_assortment_null(system)
        for lot in null_lots:
            data = get_lot_data(lot, purchase_date, system)
            if data:
                update_data.update_purchases_assortment(system, data['lot_number'], data['assortment_code'])

    return True


if __name__ == '__main__':
    print("start")
    system = 'f2_canada_real'
    print(parse.get_input_purchase_lots(system, '27/05/19')['614590'])

    data = get_lot_data('614590', system)
    print(data)
    # update_data.update_purchases_assortment(system, data['lot_number'], data['assortment_code'])
    # update_purchases(system, '31/12/19')
    # update_purchases(system, '19/12/19')
