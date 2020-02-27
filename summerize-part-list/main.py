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

import config, xlsx_conv, io
import csv_preprocess
import numpy as np
from utils import *
import beta2alpha
csv_buf = io.StringIO()

import logging
############################ Change working directory. ################################
if config.working_dir != "":
    os.chdir(config.working_dir)

def log_error(msg):
    print('Error:', msg)
def log_warn(msg):
    print('Warning:', msg)

missing_parts = []
def _main():
    if len(sys.argv) < 2:
        print('Usage: ./main.py <XlsToDeal>')
        exit(1)
    fname = sys.argv[1]
    output_prefix = fname[:-4]
    config.output_dirname = output_prefix + config.output_dirname 

    csvIO = io.StringIO()
    xlsx_conv.xlsx2csv(fname, 0, csvIO)

    fcontent = csvIO.getvalue()
    fcontent = csv_preprocess.clean_csv(fcontent, begin_keyword='__summarize_begin__', end_keyword='__summarize_end__')
    fcontent = csv_preprocess.clean_csv_2(fcontent)
    
    contArr = csv_preprocess.np_loadcsv_pycsv(io.StringIO(fcontent))
    contArr = csv_preprocess.trim_npArr(contArr)
    contMat = np.mat(contArr)

    os.mkdir(config.output_dirname)

    for line in contMat:
        line = line.tolist()[0]
        serial, product_id, product_name, quantity = line[0], line[1], line[2], line[3]
        print('[{}]Adding product {} {}({}) ...'.format(serial, quantity, product_name, product_id))

        add_product(serial, product_id, product_name, quantity, load_xlsx=True, allow_recursive_part_ref=True) # first-level recursive is enabled.
 
    _magic_merge_missing_parts()

    with open(output_prefix + '.csv', 'w+') as f:
        # Force windows NT use Linux LF. M$ office don't like CRLF csv.
        msg = '序号,,,套数,单套数量,零件名称,材料规格,参数A,参数B,参数C,长度,单件重,备注\n' + csv_buf.getvalue().replace('\r\n', '\n')
        f.write(beta2alpha.csv_beta2alpha(msg))
    with open(output_prefix + '-(缺失图纸材料表).csv', 'w+') as f:
        # Force windows NT use Linux LF. M$ office don't like CRLF csv.
        f.write('\n'.join(missing_parts))

    beta2alpha.execute_program_alpha(sys.argv[0], output_prefix + '.csv')

def get_part_metadata_from_csv_text(csvText):
    # Part Unique ID, Part Name
    try:
        ar = csvText.split('\n')[3].split(',')
        return ar[1], ar[2]
    except:
        log_error("Error: Invalid csvText while parsing part_metadata")
        raise

def add_product(serial, _id, name, quantity, load_xlsx=False, allow_recursive_part_ref=True):
    global csv_buf, missing_parts
    _id = _id.replace(' ', '')
    print('ADD_PRODUCT: serial={}, _id={}, name={}, quantity={}'.format(serial, _id, name, quantity))
    # Search & read product/part file.
    found_pdf, found_xlsx = None, None
    is_xlsx = lambda fname: fname.endswith('.xlsm') or fname.endswith('.xlsx') or fname.endswith('.xls') or fname.endswith('.XLSM') or fname.endswith('.XLSX') or fname.endswith('.XLS')
    is_pdf = lambda fname: fname.endswith('.pdf') or fname.endswith('.PDF')

    for (dirpath, dirnames, filenames) in os.walk(config.library_path):
        for fname in filenames:
            if fname.startswith(_id):
                if is_pdf(fname):
                    found_pdf = dirpath + os.path.sep + fname
                elif is_xlsx(fname):
                    found_xlsx = dirpath + os.path.sep + fname
                else:
                    log_error('Unknown file {} while looking for {}. Skipped.'.format(fname, _id))
        if (found_pdf is not None) or config.search_only_top_level_directory:
            break
    
    if found_pdf is None:
        name_and_id = '{}({})'.format(name, _id)
        log_error('Unable to locate part `{}` in `{}`, with search_only_top_level_directory={}.'.format(name_and_id, config.library_path, config.search_only_top_level_directory))
        missing_parts.insert(0, '{},{},{}'.format(_id, name, '少图')) # PDF should always appear in front of XLSx.
    else:
        # Found the product pdf.
        try_copy(found_pdf, config.output_dirname)

    if load_xlsx and found_xlsx is None:
        name_and_id = '{}({})'.format(name, _id)
        log_error('Error: Unable to find xls for {} (xls/xlsm/xlsx)'.format(name_and_id))
        missing_parts.append('{},{},{}'.format(_id, name, '少材料'))
        # ERROR RETURN
    elif load_xlsx:
        #try_copy(found_xlsx, config.output_dirname)
        # Write CSV
        csvIO = io.StringIO()
        xlsx_conv.xlsx2csv(found_xlsx, 0, csvIO)
        fcontent = csvIO.getvalue()
        part_id, part_name = get_part_metadata_from_csv_text(fcontent)
        fcontent = csv_preprocess.clean_csv(fcontent, begin_keyword='_begin__', end_keyword='_end__')
        fcontent = csv_preprocess.clean_csv_2(fcontent)
        contArr = csv_preprocess.np_loadcsv_pycsv(io.StringIO(fcontent))
        contArr = csv_preprocess.trim_npArr(contArr)
        contMat = np.mat(contArr)

        contMat[:,0] = serial
        contMat[:,1] = part_id
        contMat[:,2] = part_name
        contMat[:,3] = quantity
        contMat = npmat_truncate_cols(contMat, 13) # magic number: only keep the first 13 columns of material list.

        ############## dirty begin
        ### dirty part: append POSTFIX part_id to each part without PREFIX id. shitty, right?
        ##_dirty_subpart_name_counter = {} # 'name' -> 3
        ##def _get_subpart_name_count(name):
        ##    if name in _dirty_subpart_name_counter:
        ##        _dirty_subpart_name_counter[name] = 1 + _dirty_subpart_name_counter[name]
        ##    else:
        ##        _dirty_subpart_name_counter[name] = 1
        ##    return str(_dirty_subpart_name_counter[name])
        ##_new_contMat = np.matrix([[]], dtype=str)
        ##for line in contMat:
        ##    line = line.tolist()[0]
        ##    subpart_name = line[config.part_name_col_index]
        ##    if get_id_prefix_from_string(subpart_name) == '':
        ##        line[config.part_name_col_index] = subpart_name + part_id + '-' + _get_subpart_name_count(subpart_name)
        ##    _new_contMat = npmat_appendrow(_new_contMat, [line])
        ##contMat = _new_contMat
        ############## dirty end
        ## dirty part removed at 2020.02.17, unknown reason. backup it up, and do not remove this!

        # moved down # csv_preprocess.npmat2csv(contMat, csv_buf)

        for line in contMat:
            # recursive part reference
            if allow_recursive_part_ref:
                line_ar = line.tolist()[0]
                part_name = line_ar[config.part_name_col_index]
                part_id = get_id_prefix_from_string(part_name)
                if part_id != '':
                    if part_id.startswith(_id):
                        log_warn('Self-reference detected on part {}. Skipping recursive walking.'.format(_id))
                    else:
                        if add_product(serial, part_id, part_name, stoi(quantity)*stoi(line_ar[config.part_quantity_col_index]), load_xlsx=config.allow_part_tree_reference, allow_recursive_part_ref=config.allow_part_tree_reference): # If already included sub-part xlsx:
                            continue # DO not put the parent material into csv_buf again!
            # put line into csv_buf
            csv_preprocess.npmat2csv(line, csv_buf)

    print('ADD_PRODUCT END. found_xlsx =', found_xlsx, ', load_xlsx=', load_xlsx)
    return found_xlsx != None and load_xlsx

def _magic_merge_missing_parts():
    global missing_parts
    buf = {}
    for line in missing_parts:
        line = line.split(',')
        k = (line[0], line[1])
        v = line[2]
        v_old = buf.get(k)
        if v_old == None:
            buf[k] = v
        elif v in v_old:
            continue
        else:
            buf[k] = v + v_old
    missing_parts = []
    for k in buf:
        missing_parts.append('{},{},{}'.format(k[0], k[1], buf.get(k)))

try:
    _main()
except Exception as e:
    #alert(repr(e), 'Error')
    raise

