import pandas as pd
import numpy as np

df1 = pd.read_csv('final_stat_mean.csv')
df2 = pd.read_csv('final_stat_count.csv')
df1.drop(columns=['Unnamed: 0'], axis=1, inplace=True)
df2.drop(columns=['Unnamed: 0'], axis=1, inplace=True)


print("Average Sales Amount")
print("------------------")
print(df1['Location'][:5])
print("\n\nNumber of Sales")
print("------------------")
print(df2['Location'][:5])

# df1.set_index('Location', inplace=True)
# df2.set_index('Location', inplace=True)

df1['Count'] = df2['Value']
df1['Val_Product'] = df1['Value'] * df2['Value']
df1 = df1.sort_values('Val_Product', ascending=False)

print("\n\nVolume (Mean*Count) of Sales")
print("------------------")
print(df1['Location'][:5])

df1.to_csv('final_mean_count_prod.csv')