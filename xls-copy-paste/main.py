
import xlrd

# https://yagisanatode.com/2017/11/18/copy-and-paste-ranges-in-excel-with-openpyxl-and-python-3/
# https://stackoverflow.com/questions/35823835/reading-excel-file-is-magnitudes-slower-using-openpyxl-compared-to-xlrd

#Copy range of cells as a nested list
#Takes: start cell, end cell, and sheet you want to copy from.
def copyRange(startRow, startCol, endRow, endCol, sheet):
    rangeSelected = []
    #Loops through selected Rows
    for i in range(startRow,endRow,1):
        #Appends the row to a RowSelected list
        rowSelected = []
        for j in range(startCol,endCol,1):
            rowSelected.append(sheet.cell(row = i, column = j).value)
        #Adds the RowSelected List and nests inside the rangeSelected
        rangeSelected.append(rowSelected)

    return rangeSelected

#Paste range
#Paste data from copyRange into template sheet
def pasteRange(startRow, startCol, endRow, endCol, sheetReceiving, copiedData):
    countRow = 0
    for i in range(startRow,endRow,1):
        countCol = 0
        for j in range(startCol,endCol,1):

            sheetReceiving.cell(row = i, column = j).value = copiedData[countRow][countCol]
            countCol += 1
        countRow += 1

def enlarge_2darray_by_title(input_title, output_title, input_2darray):
    output_2darray = []
    
    def locate(t):
        index = output_title.index(t)
        if index == -1:
            raise RuntimeError('Unable to locate {} in output_titles {}'.format(t, output_title))
        return index
    # conv_list[index_in_input_arr] => index_in_output_arr
    conv_list = [locate(t) for t in input_title]

    def conv_1darr(arr):
        out_arr = ['' for _ in output_title]
        for cter, item in enumerate(arr):
            out_arr[conv_list[cter]] = item
        return out_arr
    return [conv_1darr(arr) for arr in input_2darray]

# (x,y) means (rowIndex, colIndex)
def main(argv):
    import config

    output_xls = xlrd.open_workbook(config.dst_filename)
    output_xls_sheet = output_xls.sheet_by_index(0)
    output_title = copyRange(dst_title_ULcorner[0], dst_title_ULcorner[1], dst_title_ULcorner[0]+1, dst_title_ULcorner[1]+1, output_xls_sheet)[0]

    output_x, output_y = config.dst_ULcorner # starts from 1
    all_copied_data = []
    def process_one_src(fname):
        input_sheet = xlrd.open_workbook(fname).sheet_by_index(0)
        x,y = init_x,init_y = config.src_ULcorner
        while input_sheet.cell_value(x, y) != '':
            x += 1
        copied = copyRange(init_x, init_y, x, y, input_sheet)

        input_title = copyRange(src_title_ULcorner[0], src_title_ULcorner[1], src_title_ULcorner[0]+1, src_title_ULcorner[1]+1, input_sheet)[0]
        all_copied_data += enlarge_2darray_by_title(input_title, output_title, copied)










