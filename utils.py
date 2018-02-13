import numpy as np

def npmat_appendrow(src, toAppend):
    if type(src) != np.matrix:
        src = np.matrix(src)
    if type(toAppend) != np.matrix:
        toAppend = np.matrix(toAppend)
    if src.size == 0:
        return toAppend
    if toAppend.size == 0:
        return src
    return np.concatenate((src, toAppend), axis=0)

def str_to_float(text):
    text = text.replace(' ', '')
    return float(0) if len(text) == 0 else float(text)