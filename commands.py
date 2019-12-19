from database import get_data, update_data
import closef2

def get_next_command(system):
    return get_data.get_command(system)


def restart(command):
    update_data.update_command_status(command['id'], STATUS['completed'])
    closef2.restart_pc()


COMMANDS = {'restart_pc': restart}
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

