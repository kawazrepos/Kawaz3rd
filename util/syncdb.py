# -*- coding: utf-8 -*-
#
# syncdb.py
# created by giginet on 2014/06/22
#
import os
import sys
import subprocess

BASE_DIR = os.path.join(os.path.dirname(__file__), '../')
SQLITE_NAME = 'db.sqlite3'

if __name__ == '__main__':
    os.chdir(BASE_DIR)
    db = os.path.join(BASE_DIR, SQLITE_NAME)
    if os.path.exists(db):
        print("{} is already exists in your repository".format(SQLITE_NAME))
        print("Do you want to delete this file? [Y/other]")
        answer = input()
        if not answer or not answer.lower() in ('y', 'yes'):
            sys.exit()
        os.remove(db)
    print(subprocess.check_output(['python', 'manage.py', 'syncdb' ,'--noinput'], universal_newlines=True))
    print(subprocess.check_output(['python', 'manage.py', 'loaddata' ,'production'], universal_newlines=True))
    print(subprocess.check_output(['python', 'manage.py', 'loaddata' ,'debug'], universal_newlines=True))
    print(("Development environment is set up\n"
           "Please access to http://localhost:8000/central-dogma/ in your browse\n"
           "You can login via following user\n"
           "User : system\n"
           "Password : password"
          )
    )
