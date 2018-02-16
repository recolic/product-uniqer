#!/usr/bin/env python3
# A script to deal with product sheet. (see template.csv)
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

from uniqer import *
from utils import *
import material
import csv_preprocess
import numpy as np
from io import StringIO
import sys

if len(sys.argv) < 2:
    print('Usage: ./main.py <CsvToDeal>')
    exit(1)
fname = sys.argv[1]
index_part_name = 5
index_material_name = 6
index_amount = 11
index_arg_begin = 7
index_addible = 10 # Ex: length is addible
max_args = 3 # Exclude addible arg, which is the last one
# If there're some comments, just set as an extra argument.

ignored_material_keywords = ['外购件'] # DO NOT contain junk_material_words, or it won't match.
junk_material_words = ['（厚）', '（宽）', '（单件重）']
junk_part_words = []

with open(fname, 'r') as fd:
    fcontent = fd.read()
fcontent = csv_preprocess.clean_csv(fcontent)

contArr = np.loadtxt(StringIO(fcontent), delimiter=',', dtype=str)
contMat = np.mat(contArr)

# Clean junk words
cleanedMat = np.matrix([[]], dtype=str)
for line in contArr:
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
sumedPartListMat = uniq(toSumMat, keyIndexes, [index_amount]) # This list is ok.

# tidify material list
newMaterialList = [] # Tip: ignored materials are still ignored.
for line in np.array(sumedMaterialListMat).tolist():
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

# Add ignored materials...
sumedPartListMat = npmat_appendrow(sumedPartListMat, ignoredMat)
#for line in np.array(ignoredMat).tolist():
#    newLine = [line[index_material_name] + ' 数量' + line[index_amount]]
#    newLine.extend(line[index_arg_begin:index_arg_begin+max_args])
#    newLine.extend(['','','','']) # Warning: if outputMaterialSheet is edited, you must edit this line.
#    newMaterialList.append(newLine)

# Done.
outputMaterialMat = np.mat(newMaterialList, dtype=str)
outputPartMat = sumedPartListMat

# Make output sheet head
materialLine1 = ['材料表']
materialLine1.extend(['' for i in range(outputMaterialMat.shape[1]-1)])
materialLine2 = ['材料名称']
materialLine2.extend(['参数(mm)' for i in range(max_args)])
materialLine2.extend(['每根长度(m)','每根质量(kg)','理论需根数','理论需质量(kg)'])
outputMaterialMat = npmat_appendrow(npmat_appendrow(materialLine1, materialLine2), outputMaterialMat)

partLine1 = ['零件表']
partLine1.extend(['' for i in range(outputPartMat.shape[1]-1)])
partLine2 = ['零件名称','材料名称']
partLine2.extend(['参数(mm)' for i in range(max_args)])
partLine2.extend(['长度(mm)','数量'])
partLine2.extend(['' for i in range(outputPartMat.shape[1]-len(partLine2))])
outputPartMat = npmat_appendrow(npmat_appendrow(partLine1, partLine2), outputPartMat)

# Ok. Enjoy!
materialFileName = fname[:-4] + '-材料表.csv'
partFileName = fname[:-4] + '-下料表.csv'
np.savetxt(materialFileName, outputMaterialMat, fmt='%s', delimiter=',')
np.savetxt(partFileName, outputPartMat, fmt='%s', delimiter=',')
