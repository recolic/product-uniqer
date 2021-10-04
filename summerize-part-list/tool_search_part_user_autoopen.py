#!/usr/bin/python3
# A script to deal with product sheet. (see test-*.xlsx)
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

# Allow import parent
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

################################### BEGIN #####################################
import config, xlsx_conv, utils

def main():
    def contains_id(fname, _id):
        try:
            s = xlsx_conv.read_as_csv(fname)
            s = s.replace(' ', '').replace(',', '')
            return s.lower().find(_id.lower()) != -1
        except:
            # Catch PermissionError etc. 
            return False
    
    def got_result(filepath):
        print("DEBUG: HIT", filepath)
        import subprocess, os, platform, time
        if platform.system() == 'Darwin':       # macOS
            subprocess.call(('open', filepath))
        elif platform.system() == 'Windows':    # Windows
            os.startfile(filepath)
        else:                                   # linux variants
            subprocess.call(('xdg-open', filepath))
        exit(0)

    if len(sys.argv) == 1:
        raise RuntimeError('Usage: drag a file into me...')
    target_filename = os.path.basename(sys.argv[1])
    target_id = utils.get_id_prefix_from_string(target_filename)
    results = []

    print('Iterating... Please wait... (searching for', target_id)
    is_xlsx = lambda fname: fname.endswith('.xlsm') or fname.endswith('.xlsx') or fname.endswith('.xls') or fname.endswith('.XLSM') or fname.endswith('.XLSX') or fname.endswith('.XLS')
    for (dirpath, dirnames, filenames) in os.walk(config.library_path):
        for fname in filenames:
            if is_xlsx(fname):
                if contains_id(dirpath + os.path.sep + fname, target_id):
                    results.append(fname)
                    got_result(dirpath + os.path.sep + fname)
        # if config.search_only_top_level_directory:
        #     break

    if config.working_dir != "": 
        os.chdir(config.working_dir)
    print("找不到存在此引用的文件")
    import time
    time.sleep(1000)

main()
