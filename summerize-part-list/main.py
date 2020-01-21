#!/usr/bin/python3
# A script to deal with product sheet. (see test-*.xlsx)
# Copyright (C) 2018  Recolic Keghart <root@recolic.net>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import traceback
def show_exception_and_exit(exc_type, exc_value, tb):
    traceback.print_exception(exc_type, exc_value, tb)
    input("Press any key to exit.")
    sys.exit(-1)

import sys
import os, shutil
if os.name == 'nt':
    sys.excepthook = show_exception_and_exit

csv_buf = io.StringIO()

def _main():
    import config, xlsx_conv, io
    
    if len(sys.argv) < 2:
        print('Usage: ./main.py <XlsToDeal>')
        exit(1)
    fname = sys.argv[1]

    csvIO = io.StringIO()
    xlsx_conv.xlsx2csv(fname, config.sheet_name, csvIO)

    fcontent = csvIO.getvalue()
    fcontent = csv_preprocess.clean_csv(fcontent, begin_keyword='__summarize_begin__', end_keyword='__summarize_end__')
    fcontent = csv_preprocess.clean_csv_2(fcontent)
    
    contArr = csv_preprocess.np_loadcsv_pycsv(StringIO(fcontent))
    contArr = csv_preprocess.trim_npArr(contArr)
    contMat = np.mat(contArr)

    os.mkdir(config.output_dirname)

    for cter, line in enumerate(contMat):
        product_id, product_name, quantity = line[0:2]
        serial = cter + 1
        print('[{}]Adding product {} {}({}) ...'.format(serial, quantity, product_name, product_id))

        add_product(serial, product_id, product_name, quantity, must_have_xlsx=True) # first-level recursive is enabled

    output_fname = os.path.basename(fname)[:-4] + '.csv'
    with open(output_fname, 'w+') as f:
        f.write(csv_buf.getvalue())

    input("Done. Press any key to exit.")

def get_part_metadata_from_csv_text(csvText):
    # Part Unique ID, Part Name
def get_id_prefix_from_string(s):
    for i, c in enumerate(s):
        first_illegal_char_index = i
        if c is not in 'QWERTYUIOPASDFGHJKLZXCVBNM1234567890qwertyuiopasdfghjklzxcvbnm':
            break
    return s[:first_illegal_char_index]

    
def add_product(serial, _id, name, quantity, must_have_xlsx=False, allow_recursive_part_ref=True):
    global csv_buf
    # Search & read product/part file.
    found_pdf, found_xlsx = None
    is_xlsx = lambda fname: fname.endswith('.xlsm') or fname.endswith('.xlsx') or fname.endswith('.xls')

    for (dirpath, dirnames, filenames) in os.walk(config.library_path):
        for fname in filenames:
            if fname.startswith(_id) and fname.endswith('.pdf'):
                found_pdf = config.library_path + dirpath + fname
            if fname.startswith(_id) and is_xlsx(fname):
                found_xlsx = config.library_path + dirpath + fname
        if (found_pdf is not None) or config.search_only_top_level_directory:
            break
    
    if found_pdf is None:
        print('Error: Unable to locate part `{}` in `{}`, with search_only_top_level_directory={}.'.format(_id+fname, config.library_path, config.search_only_top_level_directory))
        return

    # Found the product pdf.
    shutil.copy(found_pdf, config.output_dirname)

    if found_xlsx is not None:
        shutil.copy(found_xlsx, config.output_dirname)
        # Write CSV
        csvIO = io.StringIO()
        xlsx_conv.xlsx2csv(found_xlsx, config.sheet_name, csvIO)
        fcontent = csvIO.getvalue()
        part_id, part_name = get_part_metadata_from_csv_text(fcontent)
        fcontent = csv_preprocess.clean_csv(fcontent, begin_keyword='_begin__', end_keyword='_end__')
        fcontent = csv_preprocess.clean_csv_2(fcontent)
        contArr = csv_preprocess.np_loadcsv_pycsv(StringIO(fcontent))
        contArr = csv_preprocess.trim_npArr(contArr)
        contMat = np.mat(contArr)

        contMat[:,0] = serial
        contMat[:,1] = part_id
        contMat[:,2] = part_name
        contMat[:,3] = quantity
        contMat.resize(contMat.shape[0], 12)

        npmat2csv(contMat, csv_buf)

        # recursive part reference
        for line in contMat:
            part_name = contMat[config.part_name_col_index]
            part_id = get_id_prefix_from_string(part_name)
            add_product(serial, part_id, part_name, quantity*int(contMat[config.part_quantity_col_index]), allow_recursive_part_ref=config.allow_part_tree_reference)
    else:
        if must_have_xlsx:
            print('Error: Unable to find xls: {}.xlsx (xls/xlsm/xlsx)'.format(found_pdf[:-4]))

try:
    _main()
except Exception as e:
    #alert(repr(e), 'Error')
    raise

