import xlrd
import csv
import config

def xlsx2csv(xlsxPath, sheetName, outputFd):
    wb = xlrd.open_workbook(xlsxPath)
    sh = wb.sheet_by_name(sheetName)
    wr = csv.writer(outputFd, quoting=csv.QUOTE_NONNUMERIC)

    for rownum in range(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    your_csv_file.close()

