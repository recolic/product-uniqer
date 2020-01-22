import xlrd
import csv
import config

def xlsx2csv(xlsxPath, sheetIndex, outputFd):
    wb = xlrd.open_workbook(xlsxPath)
    sh = wb.sheet_by_index(sheetIndex)
    wr = csv.writer(outputFd, quoting=csv.QUOTE_NONNUMERIC)

    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))


