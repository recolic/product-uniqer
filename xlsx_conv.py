import xlrd
import csv, io

def float_to_str(f):
    float_string = repr(f)
    if 'e' in float_string:  # detect scientific notation
        digits, exp = float_string.split('e')
        digits = digits.replace('.', '').replace('-', '')
        exp = int(exp)
        zero_padding = '0' * (abs(int(exp)) - 1)  # minus 1 for decimal point in the sci notation
        sign = '-' if f < 0 else ''
        if exp > 0:
            float_string = '{}{}{}.0'.format(sign, digits, zero_padding)
        else:
            float_string = '{}0.{}{}'.format(sign, zero_padding, digits)
    return float_string

def xlsx2csv(xlsxPath, sheetIndex, outputFd):
    wb = xlrd.open_workbook(xlsxPath)
    sh = wb.sheet_by_index(sheetIndex)
    wr = csv.writer(outputFd, quoting=csv.QUOTE_MINIMAL)

    def fuck_number_ele(ele):
        if type(ele) is float:
            s = float_to_str(ele)
            if 'e' in s.lower():
                raise RuntimeError('Fuck python Float2Str: THIS IS A BUG. PLEASE REPORT.')
            if s.endswith('.0'):
                return s[:-2]
            else:
                return s
        else:
            return ele

    for rownum in range(sh.nrows):
        wr.writerow([fuck_number_ele(ele) for ele in sh.row_values(rownum)])

def read_as_csv(fname):
    is_xlsx = lambda fname: fname.endswith('.xlsm') or fname.endswith('.xlsx') or fname.endswith('.xls') or fname.endswith('.XLSM') or fname.endswith('.XLSX') or fname.endswith('.XLS')
    # read xlsx or csv
    if is_xlsx(fname):
        buf = io.StringIO()
        xlsx2csv(fname, 0, buf)
        return buf.getvalue()
    else:
        with open(fname, mode='r') as fd:
            return fd.read()

