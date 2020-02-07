#!/usr/bin/python3
# Unknown script

# Workaround for fucking Windows NT
import traceback
def show_exception_and_exit(exc_type, exc_value, tb):
    traceback.print_exception(exc_type, exc_value, tb)
    input("Press any key to exit.")
    sys.exit(-1)

import sys
import os, shutil
if os.name == 'nt':
    sys.excepthook = show_exception_and_exit

import main

def _main():
    main.main(sys.argv)

try:
    _main()
except Exception as e:
    #alert(repr(e), 'Error')
    raise

