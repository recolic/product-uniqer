from uniqer import *
from utils import *
import material
import csv_preprocess
import numpy as np
from io import StringIO

fl = 'test.csv'
index_part_name = 0
index_material_name = 1
index_amount = 5
index_arg_begin = 2
index_addible = 4 # Ex: length is addible
max_args = 3
# If there're some comments, just set as an extra argument.

ignored_material_keywords = ['板材', '外购件'] # DO NOT contain junk_material_words, or it won't match.
junk_material_words = ['（厚）', '（宽）', '（单件重）']
junk_part_words = []

with open(fl, 'r') as fd:
    fcontent = fd.read()
fcontent = csv_preprocess.clean_csv(fcontent)

contArr = np.loadtxt(StringIO(fcontent), delimiter=',')
contMat = np.mat(contArr)

# Clean junk words
cleanedMat = np.matrix([[]])
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
toSumMat = np.matrix([[]])
ignoredMat = np.matrix([[]])
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
sumedPartListMat = uniq(toSumMat, keyIndexes, [index_amount]) # This list is ok.

# tidify material list
newMaterialList = [] # Tip: ignored materials are still ignored.
for line in np.array(sumedMaterialListMat).tolist():
    newLine = [line[index_material_name]]
    newLine.extend(line[index_arg_begin:index_arg_begin+max_args])

    material_class = material.material_find_class_obj(line[index_material_name])
    arg_list = [float(arg)/1000 for arg in line[index_arg_begin:index_arg_begin+max_args]]
    newLine.append(material_class.get_meter_per_unit()) # meter per unit
    newLine.append(material_class.get_weight(arg_list, material_class.get_meter_per_unit())) # weight per unit
    newLine.append(material_class.get_unit_amount(float(line[index_addible]))) # needed unit amount
    newLine.append(material_class.get_weight(arg_list, float(line[index_addible]))) # needed weight

    newLine = [str(i) for i in newLine]
    newMaterialList.append(newLine)

# Add ignored materials...
for line in np.array(ignoredMat).tolist():
    newLine = [line[index_material_name]]
    newLine.extend(['' for i in range(max_args + 4)])
    newMaterialList.append(newLine)

###TODO:
# Print newMaterialList
# Print sumedPartList
    
