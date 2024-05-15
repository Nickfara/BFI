def check(doc): # Сканер json чека
    print('СКАН: check')

def doc(shop, doc):
    print('СКАН: doc')
    import xlrd
    items = []
    # Open the Workbook
    if shop == 'Чек':
        return check(doc)