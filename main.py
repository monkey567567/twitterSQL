import sqlite3
import re
import os
from getpass import getpass
from datetime import datetime
from main_functions import *

def main():
    global connection, cursor
    connect()
    login_page()

    return

if __name__ == "__main__":
    main()