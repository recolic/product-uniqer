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