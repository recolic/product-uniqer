def _stoi(s):
    # string to int
    return 0 if (s is None or s == '') else int(float(s))

# convert BETA output csv, to match the format of ALPHA input format.
def csv_beta2alpha(csvText):
    lines = csvText.split('\n')
    res = lines[0] + ',总数量(autogen), __uniqer_begin__\n' # Silly M$ office don't like \r\n.

    for line in lines[1:]:
        items = line.split(',')
        if len(items) <= 1:
            continue # empty line
        if len(items) != 13:
            raise RuntimeError('Invalid line while performing BETA => ALPHA: ' + line)

        actual_quantity = str(_stoi(items[3]) * _stoi(items[4]))
        res += '{},{}\n'.format(line.replace('"""','"'), actual_quantity)

    res += '__uniqer_end__\n'
    return res

import os, subprocess
def execute_program_alpha(mypath, parent_arg1):
    if not mypath.endswith('main.py'):
        raise RuntimeError('CurrPath should end with `main.py`, but it is: ' + mypath)
    par = os.path.abspath(mypath[:-7] + '../main.py')
    args = [par, parent_arg1]
    if os.name == 'nt':
        args = ['python'] + args

    print('EXEC =======================>', args)
    ret = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in ret.stdout:
        print(line)
    if ret.returncode != 0:
        raise RuntimeError('SubProcess returned in status ' + str(ret.returncode))
    print('EXEC SUBPROC EXITED =======================>')





