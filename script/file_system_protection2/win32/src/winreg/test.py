# CHINE\SOFTWARE\ATI Technologies\Install\Packages\W-06-0U03-000-002-131-001-00-25\SubPackages\W-06-0U03-000-002-136-001-00-05->InstallOrder
# Insert HKEY_LOCAL_MACHINE\SOFTWARE\ATI Technologies\Install\Packages\W-06-0U03-000-002-131-001-00-25\SubPackages\W-06-0U03-000-002-136-001-00-05->breboot_req
# Insert HKEY_LOCAL_MACHINE\SOFTWARE\ATI Technologies\Install\Packages\W-06-0U03-000-002-131-001-00-25\SubPackages\W-06-0U03-000-002-136-001-00-05->RebootInstallCondition
# Insert HKEY_LOCAL_MACHINE\SOFTWARE
import winreg
import hashlib
import sqlite3
from regcontroller import get_connect_db
hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\ATI Technologies\Install\Packages\W-06-0U03-000-002-131-001-00-25\SubPackages\W-06-0U03-000-002-136-001-00-05')

hkeyInfo = winreg.QueryInfoKey(hkey)

def query(name):
    try:
        conn = get_connect_db(r'F:\BKCS\z_More\Host-IPS\Host-IPS\win32\src\test\database\test.db')
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT id_registry, name_registry, hash_str " +
                        "FROM registry_hash_table " 
                        "WHERE name_registry = ?", (name,))
            ret = cur.fetchone()
            # ret = cur.fetchall()
            print(ret)
        conn.close()
    except:
        print("error")
hash = hashlib.sha1()

name = r"HKEY_LOCAL_MACHINE\SOFTWARE\ATI Technologies\Install\Packages\W-06-0U03-000-002-131-001-00-25\SubPackages\W-06-0U03-000-002-136-001-00-05->RebootInstallCondition"
for i in range(hkeyInfo[1]):
    n, v, t = winreg.EnumValue(hkey, i)
    if n == 'RebootInstallCondition':
        retv =  name
        print(retv)
        retv = retv + str(t) + str(v)
        hash.update(retv.encode())
        print(hash.hexdigest())

query(name)
