# Calculate the effective yield by multiplying the CSI with the yield
from datetime import datetime
import pandas as pd

# read yield.csv
yield_df = pd.read_csv('yield.csv')

# read growing_season.csv
gdd = pd.read_csv('csi.csv')

print(yield_df)
print(gdd)

df_effective_yield = pd.DataFrame()

# Convert yield's production_year which is 1955/56 to 1955
yield_df['year'] = yield_df['production_year'].apply(lambda x: int(x.split('/')[0]))

# Convert to int
yield_df['year'] = yield_df['year'].apply(lambda x: int(x))

# Select entries from 1950 to 2024 in yield
yield_df = yield_df[yield_df['year'] >= 1950]

# Select wheat_ton_per_hectare from yield_df
wheat_ton_per_hectare = yield_df['wheat_ton_per_hectare']

print(wheat_ton_per_hectare)

# Duplicate entries to match the size of gdd
wheat_ton_per_hectare = [value for value in wheat_ton_per_hectare for _ in range(72)]

# Trim gdd to match the size of wheat_ton_per_hectare
gdd = gdd[:len(wheat_ton_per_hectare)]

# while True:
# Add the wheat_ton_per_hectare to the df_effective_yield
df_effective_yield['date'] = gdd['date']
df_effective_yield['wheat_ton_per_hectare'] = wheat_ton_per_hectare

# Add the CSI to the df_effective_yield
df_effective_yield['csi'] = gdd['csi']

# Calculate the effective yield
df_effective_yield['effective_yield'] = df_effective_yield['wheat_ton_per_hectare'] * df_effective_yield['csi']

# Write the effective yield to a CSV file
df_effective_yield.to_csv('effective_yield.csv', index=False)
