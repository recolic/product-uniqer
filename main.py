#!/usr/bin/env python3
# A script to deal with product sheet. (see test-*.csv)
import traceback
def show_exception_and_exit(exc_type, exc_value, tb):
    traceback.print_exception(exc_type, exc_value, tb)
    # input("Press any key to exit.")
    # PROG BETA calls this program. do not block
    sys.exit(-1)

import sys
import os
if os.name == 'nt':
    sys.excepthook = show_exception_and_exit

from uniqer import *
from utils import *
import material
import csv_preprocess, xlsx_conv
import numpy as np
from io import StringIO

def _dirty_func_return_empty_sheet(fname):
    materialFileName = fname[:-4] + '-(材料表).csv'
    partFileName = fname[:-4] + '-(下料表).csv'
    with open(materialFileName, 'w+') as f:
        f.write('空表')
    with open(partFileName, 'w+') as f:
        f.write('空表')
    exit(0)
    
def _main():
    if len(sys.argv) < 2:
        print('Usage: ./main.py <CsvToDeal>')
        exit(1)
    fname = sys.argv[1]

    index_part_name = 5
    index_material_name = 6
    index_arg_begin = 7
    index_addible = 10 # Ex: length is addible
    index_amount = 13
    index_comment = 12
    max_args = 3 # EXCLUDE addible arg, which is always the last one
    
    ignored_material_keywords = ['外购件'] # DO NOT contain junk_material_words, or it won't match.
    junk_material_words = ['（厚）', '（宽）', '（单件重）']
    junk_part_words = []
    
    fcontent = xlsx_conv.read_as_csv(fname)
    fcontent = csv_preprocess.clean_csv(fcontent)
    if fcontent.strip() == '':
        _dirty_func_return_empty_sheet(fname)
        # Although the following code supports empty sheet, but empty sheet still causes wrong-formatted output.
        # To make it easy, still enable this dirty function
    fcontent = csv_preprocess.clean_csv_2(fcontent)
    
    #contArr = np.loadtxt(StringIO(fcontent), delimiter=',', dtype=str)
    contArr = csv_preprocess.np_loadcsv_pycsv(StringIO(fcontent))
    contArr = csv_preprocess.trim_npArr(contArr)
    contMat = np.mat(contArr)
    
    # Clean junk words
    cleanedMat = np.matrix([[]], dtype=str)
    for line in contArr:
        if line.size == 0:
            continue # empty sheet
        for word in junk_material_words:
            if word in line[index_material_name]:
                line[index_material_name] = line[index_material_name].replace(word, '')
        for word in junk_part_words:
            if word in line[index_part_name]:
                line[index_part_name] = line[index_part_name].replace(word, '')
        cleanedMat = npmat_appendrow(cleanedMat, line)
    contArr = np.array(cleanedMat)
    contMat = cleanedMat

    # Pick these ignored materials out
    toSumMat = np.matrix([[]], dtype=str)
    ignoredMat = np.matrix([[]], dtype=str)
    for line in contArr:
        if line.size == 0:
            continue # empty sheet
        ignored = False
        for keyword in ignored_material_keywords:
            if keyword in line[index_material_name]:
                ignoredMat = npmat_appendrow(ignoredMat, line)
                ignored = True
                break
        if not ignored:
            toSumMat = npmat_appendrow(toSumMat, line)
    
    # Make summation
    keyIndexes = [index_material_name]
    for i in range(max_args):
        if index_arg_begin + i != index_addible:
            keyIndexes.append(index_arg_begin + i)
    sumedMaterialListMat = uniq(toSumMat, keyIndexes, [index_addible, index_amount])
    
    keyIndexes.append(index_part_name)
    keyIndexes.append(index_addible)
    sumedPartListMat = uniq(toSumMat, keyIndexes, [index_amount])
    sumedIgnoredMat = uniq(ignoredMat, keyIndexes, [index_amount])
    
    # tidify material list
    newMaterialList = [] # Tip: ignored materials are still ignored.
    for line in np.array(sumedMaterialListMat).tolist():
        if line == []:
            continue # empty sheet
        newLine = [line[index_material_name]]
        newLine.extend(line[index_arg_begin:index_arg_begin+max_args])
    
        material_class = material.material_find_class_obj(line[index_material_name])
        arg_list = [str_to_float(arg)/1000 for arg in line[index_arg_begin:index_arg_begin+max_args]]
        m_length = float(line[index_addible])/1000
        newLine.append(material_class.get_meter_per_unit()) # meter per unit
        newLine.append(material_class.get_weight(arg_list, material_class.get_meter_per_unit())) # weight per unit
        newLine.append(material_class.get_unit_amount(m_length)) # needed unit amount
        newLine.append(material_class.get_weight(arg_list, m_length)) # needed weight
    
        newLine = [str(i) for i in newLine]
        newMaterialList.append(newLine)
    
    # Add ignored materials before tidify part list
    sumedPartListMat = npmat_appendrow(sumedPartListMat, sumedIgnoredMat)

    # tidify part list
    newPartList = []
    for line in np.array(sumedPartListMat).tolist():
        if line == []:
            continue # empty sheet
        newLine = [line[index_part_name], line[index_material_name]]
        newLine.extend(line[index_arg_begin:index_arg_begin+max_args])
        newLine.append(line[index_addible])
        newLine.append(line[index_amount])
        newLine.append(line[index_comment])

        newPartList.append(newLine)
        

    # Add ignored materials to material list...
    #for line in np.array(ignoredMat).tolist():
    #    newLine = [line[index_material_name] + ' 数量' + line[index_amount]]
    #    newLine.extend(line[index_arg_begin:index_arg_begin+max_args])
    #    newLine.extend(['','','','']) # Warning: if outputMaterialSheet is edited, you must edit this line.
    #    newMaterialList.append(newLine)
    
    # Done.
    outputMaterialMat = np.mat(newMaterialList, dtype=str)
    outputPartMat = np.mat(newPartList, dtype=str) 

    # Make output sheet head
    materialLine1 = ['材料表']
    materialLine1.extend(['' for i in range(outputMaterialMat.shape[1]-1)])
    materialLine2 = ['材料名称']
    materialLine2.extend(['参数(mm)' for i in range(max_args)])
    materialLine2.extend(['每根长度(m)','每根质量(kg)','理论需根数','理论需质量(kg)'])
    materialLineEmpty = ['' for i in range(outputMaterialMat.shape[1])]
    outputMaterialMat = npmat_appendrow(np.mat([materialLine1, materialLine2, materialLineEmpty, materialLineEmpty]), outputMaterialMat)
    
    partLine1 = ['下料表']
    partLine1.extend(['' for i in range(outputPartMat.shape[1]-1)])
    partLine2 = ['零件名称','材料名称']
    partLine2.extend(['参数(mm)' for i in range(max_args)])
    partLine2.extend(['长度(mm)','数量','备注'])
    partLine2.extend(['' for i in range(outputPartMat.shape[1]-len(partLine2))])
    partLineEmpty = ['' for i in range(outputPartMat.shape[1])]
    outputPartMat = npmat_appendrow(np.mat([partLine1, partLine2, partLineEmpty, partLineEmpty]), outputPartMat)
    
    # Ok. Enjoy!
    materialFileName = fname[:-4] + '-(材料表).csv'
    partFileName = fname[:-4] + '-(下料表).csv'
    np.savetxt(materialFileName, outputMaterialMat, fmt='%s', delimiter=',')
    np.savetxt(partFileName, outputPartMat, fmt='%s', delimiter=',')

    # Dirty func here.
    cut_extra_info_for_2dmaterial(materialFileName)

def cut_extra_info_for_2dmaterial(csvName):
    # This is a dirty function.
    def _get_summed_weight(cont, niddle):
        w = 0.0
        for line in cont.split('\n'):
            if line[:len(niddle)] == niddle:
                w += str_to_float(line.split(',')[-1]) # Assume last element is weight
        return str(w)
    # No comma is allowed in 2dmaterial_name!
    _2dmaterial_names = list(filter(lambda x: x != '', [mclass.name if mclass.is2d else '' for mclass in material.material_class_list]))
    with open(csvName, 'r') as fd:
        cont = fd.read()
    result = ''
    newLine_must_merge = []
    for line in cont.split('\n'):
        double_continue_flag = False
        for name in _2dmaterial_names:
            niddle = name + ','
            if line[:len(niddle)] == niddle:
                arg1 = line.split(',')[1]
                newLine = niddle + arg1 + str_repeat(',', line.count(',')-1) + _get_summed_weight(cont, niddle+arg1+',')
                if newLine in newLine_must_merge:
                    double_continue_flag = True
                    break
                line = newLine
                newLine_must_merge.append(newLine)
        if double_continue_flag:
            continue
        result += line
        result += '\n'
    with open(csvName, 'w+') as fd:
        fd.write(result)

try:
    _main()
except Exception as e:
    #alert(repr(e), 'Error')
    raise
