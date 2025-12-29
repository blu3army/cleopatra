import pandas as pd

df = pd.read_excel('../data/cheques_list.xlsx')

print("\nHere are the headers\n")
print(df.head())

print("\nHere are the columns\n")
print(df.columns)

print("\nHere are the indexes\n")
print(df.index)

print("\nHere are the values in dict form\n")
print(df.to_dict())

print("\nHere are the data in json format\n")
print(df.to_json(orient='records'))

print("\nIteration over df\n")
for i, row in df.iterrows():
    print(f"row {i}")
    print(row)

