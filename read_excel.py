import pandas as pd

df = pd.read_excel(r'/Users/aaron.john/Desktop/Composer/SPFD_Emission Factors_All Contributors.xlsx', names=['Contributor', 'Sub Category', 'Category', 'Multiplying Factor', 'Area code', 'Feature Factors', 'NULL', 'NULL'],header=1)
df.fillna(value="NULL", inplace=True)
print(df)