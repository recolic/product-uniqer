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

import numpy as np
import ctypes
import os

def npmat_appendrow(src, toAppend):
    if src is None:
        return toAppend
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

def str_repeat(string_to_expand, length):
    return (string_to_expand * (int(length/len(string_to_expand))+1))[:length]

def alert(text, head='Alert'):
    if os.name == 'nt':
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, text, head, 0)
    else:
        print('{}> {}'.format(head, text))

def npmat_truncate_cols(mat, max_cols):
    result = None
    for line in mat:
        tmp = line.copy()
        tmp.resize(1, max_cols)
        result = npmat_appendrow(result, tmp)
    return result

def get_id_prefix_from_string(s):
    first_illegal_char_index = 0
    for i, c in enumerate(s):
        first_illegal_char_index = i
        if c not in 'QWERTYUIOPASDFGHJKLZXCVBNM1234567890qwertyuiopasdfghjklzxcvbnm':
            break
    return s[:first_illegal_char_index]

def stoi(s):
    # string to int
    return 0 if (s is None or s == '') else int(float(s))
 



