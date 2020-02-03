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

        



