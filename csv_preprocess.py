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

def clean_csv(csvText):
    # Use `__uniqer_begin__` to indicate a begin, `__uniqer_end__` to indicate an end.
    foundUniqerBegin = False
    result = ''
    for line in csvText.split('\n'):
        if '__uniqer_begin__' in line:
            foundUniqerBegin = True
            continue
        if not foundUniqerBegin:
            continue
        if '__uniqer_end__' in line:
            return result
        result += line + '\n'
    
    print('Warning: clean_csv returns abnormally because of reaching EOF.')
    return result
        