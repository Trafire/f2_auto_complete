from database import get_data, update_data, insert_data
import purchase
import closef2


def get_next_command(system):
    return get_data.get_command(system)


def update_status(command, status):
    update_data.update_command_status(command['id'], STATUS[status])


def restart(command):
    update_data.update_command_status(command['id'], STATUS['completed'])
    closef2.restart_pc()


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


COMMANDS = {'restart_pc': restart, 'get_input_purchases': get_input_purchases}
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
