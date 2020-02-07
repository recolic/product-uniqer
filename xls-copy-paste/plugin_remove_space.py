def _conv(ele):
    if type(ele) == str:
        return ele.replace(' ', '')
    return ele

def work(copied):
    res = []
    for line in copied:
        res += [[_conv(ele) for ele in line]]
    return res


