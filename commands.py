from database import get_data, update_data, insert_data
import purchase, reports
import closef2
from parse import dates
import datetime

def get_next_command(system):
    return get_data.get_command(system)


def update_status(command, status):
    update_data.update_command_status(command['id'], STATUS[status])


def restart(command):
    update_data.update_command_status(command['id'], STATUS['completed'])
    closef2.restart_pc()

def get_order_lines(command):
    print(command)
    update_status(command, "started")
    reference = int(command['reference'])
    date = datetime.datetime.now() + datetime.timedelta(days= reference)
    if reports.update_week(system, dates.get_year(date), dates.get_week(date)):
        update_status(command, 'completed')




def get_input_purchases(command):
    update_status(command, "started")
    purchase_date = get_data.get_input_purchase_date_cmd(command['reference'])
    if purchase.update_purchases(system, purchase_date):
        update_status(command, 'completed')
    else:
        update_status(command, 'error')
    return True


def create_command(system, command, reference, status):
    if command == get_input_purchases:
        d = reference['purchase_date']
        id = get_data.get_cmdpurchasedates_id(d)
        if not id:
            insert_data.insert_cmd_purchase_dates(d)
            return create_command(system, command, reference, status)
        insert_data.insert_command('get_input_purchases', id, status, system)
    elif command == restart:
        insert_data.insert_command('restart_pc', None, status, system)


def two_weeks_purchases(system):
    today = datetime.datetime.now()
    days = set()
    for i in range(7):
        days.add(today + datetime.timedelta(days=i))
        days.add(today - datetime.timedelta(days=i))
    days = list(days)
    days.sort()
    for d in days:
        day = dates.get_database_date(d)
        print(day)
        create_command(system, get_input_purchases, {'purchase_date': day}, STATUS["unstarted"])




COMMANDS = {'restart_pc': restart, 'get_input_purchases': get_input_purchases, 'get_open_lines':get_order_lines}
system = 'f2_canada_real'
STATUS = {"started": "started", "unstarted": "unstarted", "completed": "completed", "error": "error"}


def process_command(system):
    command = get_next_command(system)
    print(command)
    if command:
        # update_data.update_command_status(command['id'], STATUS['started'])
        if command['command'] in COMMANDS:
            func = COMMANDS[command['command']]
            if func(command):
                update_data.update_command_status(command['id'], STATUS['completed'])
                return True
            else:
                update_data.update_command_status(command['id'], STATUS['error'])
                return True


if __name__ == "__main__":
    '''
    today = datetime.datetime.now()
    days = set()
    for i in range(20):
        days.add(today + datetime.timedelta(days=30 + i))
    days = list(days)
    days.sort()
    index = 0
    for d in days:
        index += 1
        day = dates.get_database_date(d)
        print(day)
        create_command(system, get_input_purchases, {'purchase_date': day}, STATUS["unstarted"])
        if index > 25:
            create_command(system, restart, None, STATUS['unstarted'])
            index = 0
            '''
    #command = {'id': 1514, 'command': 'get_open_lines', 'reference': 1, 'status': 'unstarted', 'system': 'f2_canada_real'}
    #get_order_lines(command)
    two_weeks_purchases(system)