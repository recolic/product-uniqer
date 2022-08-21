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

import openpyxl
import os, shutil

def list_partnames_to_lookfor(xlsxPath):
    # returns a list of partnames found
    xls = openpyxl.load_workbook(xlsxPath)
    xls_sheet = xls.worksheets[0]

    name_colnum = -1
    NAME_COLNAME = '零件名称'
    result_list = []
    for rownum, row in enumerate(xls_sheet.rows):
        if name_colnum != -1:
            partname = row[name_colnum].value
            if partname is not None:
                if partname is not str:
                    partname = str(partname)
                result_list.append(partname.strip())
        else:
            for colnum, ele in enumerate(row):
                # if ele.value is not None:
                #     print("TRY: ", ele.value)
                if ele.value == NAME_COLNAME:
                    name_colnum = colnum
                    break
    if name_colnum == -1:
        raise RuntimeError('表格中未找到以下内容单元格： ' + NAME_COLNAME)

    return result_list


def copy_files_from_dir_to_dir_with_displayname(fromDir, toDir, fname_list_without_ext):
    # todir must exist
    # returns a list of filenames that never used
    mkrelpath = lambda fname: fromDir + os.path.sep + fname
    files = [f for f in os.listdir(fromDir) if os.path.isfile(mkrelpath(f))]
    never_used_fname_list = fname_list_without_ext
    for f in files:
        fname_without_ext = os.path.splitext(f)[0].strip()
        if fname_without_ext in fname_list_without_ext:
            # hit
            shutil.copy(mkrelpath(f), toDir)
            print("COPY from " + mkrelpath(f) + " TO " + toDir)
            if fname_without_ext in never_used_fname_list:
                never_used_fname_list = [ unused_fname for unused_fname in never_used_fname_list if unused_fname != fname_without_ext ]
    return never_used_fname_list



def main():
    print("DEBUG: workdir=", os.getcwd())
    is_xlsx = lambda fname: (fname.endswith('.xlsm') or fname.endswith('.xlsx') or fname.endswith('.xls') or fname.endswith('.XLSM') or fname.endswith('.XLSX') or fname.endswith('.XLS')) and (not fname.startswith('~$'))
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    missing_parts = []
    for f in files:
        if is_xlsx(f):
            print("WORKING ON ", f)
            fname_without_ext = os.path.splitext(f)[0].strip()
            dest_dirname = fname_without_ext
            if os.path.isdir(dest_dirname):
                shutil.rmtree(dest_dirname)
            os.mkdir(dest_dirname)

            partnames = list_partnames_to_lookfor(f)
            print("DEBUG: partnames=", partnames)
            mpthis = copy_files_from_dir_to_dir_with_displayname('..', dest_dirname, partnames)
            print("DEBUG: missing_part_this=", mpthis)
            missing_parts += mpthis

            print("COPY from " + f + " TO " + dest_dirname)
            shutil.copy(f, dest_dirname)
    if len(missing_parts) > 0:
        with open('缺失零件.csv', 'w+') as f:
            f.write('\n'.join(missing_parts))


main()




