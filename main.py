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




def schedule(system):
    # priority events
    if commands.process_command(system):
        return True
    # scheduled Events
    ## get current_ time/date
    today = datetime.datetime.now()
    if schedule_purchase_reports(system, today, weeks=12):
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
    while not logged_in:

        username = f2_password['username']
        password = f2_password['password']
        system = 'f2_canada_real'
        closef2.close()
        try:
            login.sign_in_toronto(username, password, system, attempts=0)
            logged_in = True
        except:
            closef2.close()

    while True:
        # wait for database to open
        try:
            # if database isn't open yet will get error
            get_data.check_priced_lots_bulk("12345", "test")
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

        except:  # on error close f2 and relogin
            error_count += 1
            print(f"error count: {error_count}")
            try:
                closef2.close()
                login.sign_in_toronto(username, password, system, attempts=0)

            except:  # if there is an error closing f2 and relogging in, then restart computer
                error_count += 1
"""
if __name__ == '__main__':
    username = f2_password['username']
    password = f2_password['password']
    system = 'f2_canada_real'
    closef2.close()
    try:
        login.sign_in_toronto(username, password, system, attempts=0)
    except:
        closef2.close()

    while True:
        try:
            # if database isn't open yet will get error
            get_data.check_priced_lots_bulk("12345", "test")
            break
        except pyautogui.FailSafeException:
            print("Corner exit Detected")
            exit()
        except:
            time.sleep(.5)
            print("Waiting for Database connection")

    index = 0
    error_count = 0
    while True:
        try:
            # if there are more than 5 errors in a row restart computer
            if error_count > 5:
                closef2.restart_pc()

            index += 1
            if index % 30 == 0:
                closef2.close()
                login.sign_in_toronto(username, password, system)
            if index > 100:
                closef2.restart_pc()

            if commands.process_command(system):
                pass
            else:
                today = datetime.datetime.now()
                for i in range(12):
                    day = today + datetime.timedelta(weeks=i)
                    year = dates.get_year(day)
                    week = dates.get_week(day)

                    if reports.is_report_due(system, year, week):
                        reports.update_week(system, year, week)
                try:

                    stock.price_system()
                except(pyautogui.FailSafeException):
                    print("Corner exit Detected")
                    exit()
                except:
                    try:
                        closef2.close()
                        login.sign_in_toronto(username, password, system, attempts=0)
                        stock.price_system()

                    except(pyautogui.FailSafeException):
                        print("Corner exit Detected")
                        exit()
                    except:
                        closef2.close()
                        os.system("shutdown /r /t 1")
                error_count = 0
        except pyautogui.FailSafeException:
            print("Corner exit Detected")
            exit()
        except:
            # on error close f2 and relogin
            error_count += 1
            print(f"error count: {error_count}")
            try:
                closef2.close()
                login.sign_in_toronto(username, password, system)

            except pyautogui.FailSafeException:
                print("Corner exit Detected")
                exit()
            except:
                closef2.restart_pc()
"""
