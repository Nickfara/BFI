log = False
def items(items = "iIko_items_exel_base.xlsx"):
    print('\033[32miIko_items_read: items\033[0m')
    import xlrd
    workbook = xlrd.open_workbook(items)
    worksheet = workbook.sheet_by_index(0)

    items = []
    for i in range(0, 900):
        for j in range(0, 4):
            try:
                if len(str(worksheet.cell_value(i, j))) > 1 and worksheet.cell_value(i, j) != '\t':
                    item = worksheet.cell_value(i, j)
                    items.append(item)
                    if log: print(item)
            except:
                pass
        if log: print('')
    return items

