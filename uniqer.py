import numpy as np
from utils import *
import hashlib

def __quick_sha2(text):
    # This function is slow, as it may become performance bottleneck sometimes.
    # Use intel cpu hash cmd instead!
    return str(hashlib.sha224(text.encode()).hexdigest())

def __sorter(matToSort):
    # first col must be hash value, which is checked.
    return matToSort[np.lexsort(matToSort.T[::-1])][0]
    # Fuck the shitting numpy!!!!!!!
    #matToSort.sort(axis=0)

def __hasher(matToAppendHash, keyIndexes):
    # append uniq hash to first col, to feed __sorter.
    results = np.matrix([[]])
    for line in matToAppendHash:
        currhash = 'sha2-'
        for keyIndex in keyIndexes:
            currhash = currhash + __quick_sha2(line[0, keyIndex])

        newLine = np.concatenate((np.mat([[currhash]]), line), axis=1) 
        results = npmat_appendrow(newLine, results)
    return results

def __uniqer(matToUniq, sumedIndexes):
    cachedLine = np.matrix([[]])
    results = np.matrix([[]])
    for line in matToUniq:
        sumedIndex = -1 # set to first sumedIndexes. -1 if none.
        for index in sumedIndexes:
            if sumedIndex == -1:
                sumedIndex = index
                continue
            line[0,sumedIndex] = str(str_to_float(line[0,sumedIndex]) * str_to_float(line[0,index]))
            line[0,index] = '1'

        if cachedLine.size == 0:
            cachedLine = line
            continue
        
        if line[0,0] == cachedLine[0,0]:
            # Merge
            if sumedIndex != -1:
                cachedLine[0,sumedIndex] = str(str_to_float(line[0,sumedIndex])+str_to_float(cachedLine[0,sumedIndex]))
        else:
            results = npmat_appendrow(results, cachedLine)
            cachedLine = line

    results = npmat_appendrow(results, cachedLine)
    return results

def uniq(matToUniq, keyIndexes, sumedIndexes = []):
    # If there're many sumedIndexes, I'll multiply them and put result in the first one.
    assert(type(matToUniq) == np.matrix)
    if matToUniq.size == 0:
        return matToUniq
    m = __hasher(matToUniq, keyIndexes)
    m = __sorter(m)
    m = __uniqer(m, [i+1 for i in sumedIndexes]) # plus one because of hash column
    return np.delete(m, 0, 1)
