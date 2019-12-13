import getpass, os, sys
import login
import closef2
from auth.passwords import f2_password
import stock
import time
from database import get_data


def add_to_startup(executable, file_path=""):
    if file_path == "":
        file_path = os.path.dirname(os.path.realpath(__file__))
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' %  getpass.getuser()
    print(bat_path)

    with open(bat_path + '\\' + "f2_connection3.bat", "w+") as bat_file:
        bat_file.write(rf'"{executable}" "{file_path}.main.py"')
        bat_file.write("\n")
        bat_file.write(rf'"{file_path}/database/cloud_sql_proxy.exe" -instances="fmc-crm-252016:northamerica-northeast1:fmc-crm-db"=tcp:3306')

    with open(bat_path + '\\' + "f2_connection4.bat", "w+") as bat_file:
        
        bat_file.write(rf"{file_path}/env/Scripts/activate")
        bat_file.write("\n")
        bat_file.write(rf'"{executable}" "{file_path}/main.py"')
        bat_file.write("\npause")



#database_cmd ='"database/cloud_sql_proxy.exe" -instances="fmc-crm-252016:northamerica-northeast1:fmc-crm-db"=tcp:3306'
#add_to_startup(sys.executable)

# log into system
username = f2_password['username']
password = f2_password['password']
system = 'f2_canada_real'
closef2.close()
time.sleep(1)
login.sign_in_toronto(username, password, system, attempts=0)

while True:
    try:
        # if database isn't open yet will get error
        get_data.check_priced_lots_bulk("12345", "test")
        break
    except:
        time.sleep(.5)
        print("Waiting for Database connection")

index = 0        
while True:
    index += 1
    
    if index % 30 == 0 :
        closef2.close()
        login.sign_in_toronto(username, password, system, attempts=0)
    elif index > 998 == 0:
        closef2.close()
        os.system("shutdown /r /t 1")
    else:
        stock.price_system()
    

