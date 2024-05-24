import pandas as pd

df1 = pd.read_excel("cars.xlsx")
df2 = pd.read_excel("links.xlsx")

if len(df1.columns) >= len(df2.columns):
    merged_df = pd.concat([df1, df2], axis=1)
else:
    merged_df = pd.concat([df2, df1], axis=1)

merged_df.to_excel("merged_file.xlsx", index=False) 
