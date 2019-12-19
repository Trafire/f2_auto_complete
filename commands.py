from database import get_data, update_data
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






COMMANDS = {'restart_pc': restart, 'get_input_purchases':get_input_purchases}
system = 'f2_canada_real'
STATUS = {"started": "started", "unstarted": "unstated", "completed": "completed", "error": "error"}

def process_command(system):
    command = get_next_command(system)
    if command:
        # update_data.update_command_status(command['id'], STATUS['started'])
        if command['command'] in COMMANDS:
            func = COMMANDS[command['command']]
            if func(command):
                update_data.update_command_status(command['id'], STATUS['completed'])
                return True



