def items(items = "iIko_items.xlsx"):
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
                    print(item)
            except:
                pass
        print('')
    return items

