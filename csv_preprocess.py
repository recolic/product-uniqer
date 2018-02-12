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
        