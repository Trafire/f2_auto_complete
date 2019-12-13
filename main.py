import getpass, os, sys


def add_to_startup(executable, file_path=""):
    if file_path == "":
        file_path = os.path.dirname(os.path.realpath(__file__))
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' %  getpass.getuser()
    print(bat_path)
    with open(bat_path + '\\' + "f2_connection1.bat", "w+") as bat_file:
        bat_file.write(rf'"{executable}" "{file_path}.main.py"')
        bat_file.write("\n")
        bat_file.write(rf'"{file_path}/database/cloud_sql_proxy.exe" -instances="fmc-crm-252016:northamerica-northeast1:fmc-crm-db"=tcp:3306')

    with open(bat_path + '\\' + "f2_connection2.bat", "w+") as bat_file:
        bat_file.write(rf'"{executable}" "{file_path}/main.py"')
        bat_file.write("\npause")



#database_cmd ='"database/cloud_sql_proxy.exe" -instances="fmc-crm-252016:northamerica-northeast1:fmc-crm-db"=tcp:3306'
add_to_startup(sys.executable)
print('test')


