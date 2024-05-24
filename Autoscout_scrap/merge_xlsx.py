import pandas as pd

# Load both Excel files into dataframes
df1 = pd.read_excel("cars.xlsx")
df2 = pd.read_excel("links.xlsx")

# Check which dataframe has more columns
if len(df1.columns) >= len(df2.columns):
    # Merge df1 and df2
    merged_df = pd.concat([df1, df2], axis=1)
else:
    # Merge df2 and df1
    merged_df = pd.concat([df2, df1], axis=1)

# Save the merged dataframe to a new Excel file
merged_df.to_excel("merged_file.xlsx", index=False) 
