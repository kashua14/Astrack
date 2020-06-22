import pandas as pd
# import xlsxwriter

cars = {'Brand': ['Honda Civic', 'Toyota Corolla', 'Ford Focus', 'Audi A4'],
        'Price': [22000, 25000, 27000, 35000]}

df = pd.DataFrame(cars, columns = ['Brand', 'Price'])
writer = pd.ExcelWriter('trialWriter.xlsx', engine = 'xlsxwriter')
df.to_excel(writer, index = None, header = True, sheet_name = 'Cars')
writer.save()
