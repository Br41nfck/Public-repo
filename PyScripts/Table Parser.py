import pandas as pd
from datetime import date
import os
try:
    url = input('Enter url:')
    tables = pd.read_html(url)  # Returns list of all tables on page
    parse = tables[0]  # Select table of interest (you can add cycle for all tables)
    print('Founded table:\n')
    print(tables[0])  # Print founded table(s)
    print()
    print('Default path is -', os.path.abspath(os.getcwd()))
    path = input('Enter path (or press "Enter" to write in default path):')
    if path == '':
        parse.to_excel(f'F:/Projects/Python/WEB/Parsers/Table - {date.today()}.xlsx')
    else:
        parse.to_excel(path + f'Table - {date.today()}.xlsx')

    print('DONE!')

except Exception as e:
    print(e)
