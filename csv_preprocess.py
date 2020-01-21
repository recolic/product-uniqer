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

import csv
import numpy as np
import functools, utils, re

def _rstrip_csv(csvText):
    return '\n'.join([line.rstrip(',') for line in csvText.split('\n')])

def clean_csv(csvText, begin_keyword='__uniqer_begin__', end_keyword='__uniqer_end__'):
    # Use begin_keyword to indicate a begin, end_keyword to indicate an end.
    csvText = _rstrip_csv(csvText)

    foundUniqerBegin = False
    result = ''
    for line in csvText.split('\n'):
        if begin_keyword in line:
            foundUniqerBegin = True
            continue
        if not foundUniqerBegin:
            continue
        if end_keyword in line:
            result = result[:-1] if len(result) != 0 else result
            return result
        result += line + '\n'
    
    print('Warning: clean_csv returns abnormally because of reaching EOF.')
    return result

def clean_csv_2(csvText):
    # Append ',' to end of line, to make len(everyLine.split(',')) == max(anyLine.split(',')).
    def csv_bettercount_delim(line):
        return re.sub(r'"[^"]*"', '', line).count(',')
    max_count = functools.reduce(lambda a, b: max(a, b), [csv_bettercount_delim(line) for line in csvText.split('\n')])
    return '\n'.join([line+utils.str_repeat(',', max_count-csv_bettercount_delim(line)) for line in csvText.split('\n')])

def np_loadcsv_pycsv(reader_handle):
    return np.genfromtxt(("\t".join(i) for i in csv.reader(reader_handle)), delimiter="\t", dtype=str)

def trim_npArr(np_bi_arr):
    def _trim_str(s):
        goodstr = s.strip()
        if s != goodstr:
            print('Warning: trimming "{}", which is usually not expected.'.format(s))
        return goodstr
    assert(type(np_bi_arr) == np.ndarray)
    res = []
    for line in np_bi_arr:
        res.append([_trim_str(item) for item in line])
    return np.array(res)

import pandas

def npmat2csv(npmat, outputFd):
    pandas.DataFrame(npmat).to_csv(outputFd, header=False, index=False)


