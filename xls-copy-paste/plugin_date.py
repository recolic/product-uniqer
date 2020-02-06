import datetime

OLE_TIME_ZERO = datetime.datetime(1899, 12, 30, 0, 0, 0)

def parse_ole(ole):
    """ Input:  ole - float. Gives ole time, the number of DAYS since midnight 12/30/1899
        Output: float - epoch time
    """
    return OLE_TIME_ZERO + datetime.timedelta(days=ole)

def add_date_col(date_cell_val, copied, input_title):
    res = []
    try:
        curr_date = parse_ole(date_cell_val)
    except:
        print('[ERROR] Adding date column: `{}` is not a valid date stamp. Should be an int from epoch.'.format(date_cell_val))
        return copied, input_title

    for line in copied:
        res.append([curr_date.year, curr_date.month, curr_date.day] + line)

    return  res, (['年','月','日'] + input_title)
    

