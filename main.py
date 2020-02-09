import getpass, os, sys
import login
import closef2
from auth.passwords import f2_password
import stock
import time
from database import get_data
import pyautogui
import commands
import datetime
from parse import dates
import reports
import purchase

def add_to_startup(executable, file_path=""):
    if file_path == "":
        file_path = os.path.dirname(os.path.realpath(__file__))
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % getpass.getuser()
    print(bat_path)

    with open(bat_path + '\\' + "f2_connection3.bat", "w+") as bat_file:
        bat_file.write(rf'"{executable}" "{file_path}.main.py"')
        bat_file.write("\n")
        bat_file.write(
            rf'"{file_path}/database/cloud_sql_proxy.exe" -instances="fmc-crm-252016:northamerica-northeast1:fmc-crm-db"=tcp:3306')

    with open(bat_path + '\\' + "f2_connection4.bat", "w+") as bat_file:
        bat_file.write(rf"{file_path}/env/Scripts/activate")
        bat_file.write("\n")
        bat_file.write(rf'"{executable}" "{file_path}/main.py"')
        bat_file.write("\npause")


def schedule_purchase_reports(system, today, weeks=12):
    for i in range(weeks):
        day = today + datetime.timedelta(weeks=i)
        year = dates.get_year(day)
        week = dates.get_week(day)
        if reports.is_report_due(system, year, week):
            return reports.update_week(system, year, week)

def schedule_input_purchase(system,today, days=30):
    for i in range(-5, days):
        day = today + datetime.timedelta(days=i)
        if purchase.is_purchase_day_due(system,day,i):
            purchase.update_purchases(system, day)
            return True



def schedule(system):
    # priority events
    if commands.process_command(system):
        return True
    # scheduled Events
    ## get current_ time/date
    today = datetime.datetime.now()
    if schedule_purchase_reports(system, today, weeks=12):
        return True
    if schedule_input_purchase(system,today, days=30):
        return True
    stock.price_system()

def maintainance(system, index):

    if index % 30 == 0:
        closef2.close()
        login.sign_in_toronto(username, password, system)
    if index > 119:
        closef2.restart_pc()



# database_cmd ='"database/cloud_sql_proxy.exe" -instances="fmc-crm-252016:northamerica-northeast1:fmc-crm-db"=tcp:3306'
# add_to_startup(sys.executable)

# log into system

if __name__ == '__main__':
    ### log in with only one F2 window open
    logged_in = False
    tries = 0
    while not logged_in:
        tries += 1
        username = f2_password['username']
        password = f2_password['password']
        system = 'f2_canada_real'
        closef2.close()
        print(f'Login Attempt: {tries}')
        if tries > 10:
            closef2.restart_pc()
        try:
            if login.sign_in_toronto(username, password, system, attempts=0):
                logged_in = True

        except pyautogui.FailSafeException:
            print("Corner exit Detected")
            exit()
        except:
            closef2.close()
    print("checking for database connection...")
    while True:
        # wait for database to open
        try:
            # if database isn't open yet will get error
            get_data.check_priced_lots_bulk("12345", "test")
            print('database connected...')
            break
        except pyautogui.FailSafeException:
            print("Corner exit Detected")
            exit()
        except:
            time.sleep(.5)
            print("Waiting for Database connection")

    index = 1
    error_count = 0

    while True:  # main loop
        try:
            if error_count > 5:  # if the are 5 failures in a row, restart computer
                closef2.restart_pc()

            # do the item that is scheduled to do next
            schedule(system)
            maintainance(system, index)
            index += 1
            error_count = 0
            print(index)

        except pyautogui.FailSafeException:  # manual stop program

            print("Corner exit Detected")
            exit()

        except Exception as err:  # on error close f2 and relogin
            print(err)
            error_count += 1
            print(f"error count: {error_count}")
            try:
                closef2.close()
                login.sign_in_toronto(username, password, system, attempts=0)

            except:  # if there is an error closing f2 and relogging in, then restart computer
                error_count += 1
