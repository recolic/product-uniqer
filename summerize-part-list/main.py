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
import os
if os.name == 'nt':
    sys.excepthook = show_exception_and_exit

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

    for line in contMat:
        product_id, product_name, quantity = line[0:2]
        print('Adding product {} {}({}) ...'.format(quantity, product_name, product_id))
        add_product(product_id, product_name, quantity, must_have_xlsx=True) # first-level recursive is enabled



def get_part_metadata_from_csv_text(csvText):
    # Part Unique ID, Part Name

    
def add_product(_id, name, quantity, must_have_xlsx=False, allow_recursive_part_ref=True):
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
    if found_xlsx is not None:
        csvIO = io.StringIO()
        xlsx_conv.xlsx2csv(found_xlsx, config.sheet_name, csvIO)
        fcontent = csvIO.getvalue()
        part_id, part_name = get_part_metadata_from_csv_text(fcontent)
        fcontent = csv_preprocess.clean_csv(fcontent, begin_keyword='_begin__', end_keyword='_end__')
        fcontent = csv_preprocess.clean_csv_2(fcontent)
        contArr = csv_preprocess.np_loadcsv_pycsv(StringIO(fcontent))
        contArr = csv_preprocess.trim_npArr(contArr)
        contMat = np.mat(contArr)





        # recursive part reference
        add_product()



try:
    _main()
except Exception as e:
    #alert(repr(e), 'Error')
    raise

