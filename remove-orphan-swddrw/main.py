#!/usr/bin/env python3
# A script to deal with product sheet. (see test-*.csv)
import traceback
def show_exception_and_exit(exc_type, exc_value, tb):
    traceback.print_exception(exc_type, exc_value, tb)
    input("按回车键退出")
    sys.exit(-1)

import sys
import os
if os.name == 'nt':
    sys.excepthook = show_exception_and_exit


#########################################################################

import os, shutil

def main():
    print("DEBUG: workdir=", os.getcwd())
    is_drw = lambda fname: fname.lower().endswith('.slddrw')
    is_prt_asm = lambda fname: (fname.lower().endswith('.sldprt') or fname.lower().endswith('.sldasm'))
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    filesl = [f.lower() for f in os.listdir('.') if os.path.isfile(f)]
    for f in files:
        if is_drw(f):
            print("CHECKING ", f)

            ext_len = len('.slddrw')
            expecting1 = f[:-ext_len] + '.sldprt'
            expecting2 = f[:-ext_len] + '.sldasm'
            if expecting1.lower() in filesl or expecting2.lower() in filesl:
                # good
                pass
            else:
                # delete this file
                print("DELETE ", f)
                os.remove(f)


main()
input("按回车键退出")




