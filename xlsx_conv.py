import xlrd
import csv, io

def xlsx2csv(xlsxPath, sheetIndex, outputFd):
    wb = xlrd.open_workbook(xlsxPath)
    sh = wb.sheet_by_index(sheetIndex)
    wr = csv.writer(outputFd, quoting=csv.QUOTE_MINIMAL)

    def fuck_number_ele(ele):
        if type(ele) is float:
            s = str(ele)
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

