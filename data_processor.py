
import pandas as pd

# Step 1: Load all 3 CSV files
df0 = pd.read_csv('data/daily_sales_data_0.csv')
df1 = pd.read_csv('data/daily_sales_data_1.csv')
df2 = pd.read_csv('data/daily_sales_data_2.csv')

# Step 2: Combine into one big table
df = pd.concat([df0, df1, df2], ignore_index=True)

# Step 3: Filter to Pink Morsel only
df = df[df['product'] == 'pink morsel']

# Step 4: Clean price column (remove $ sign) and convert to number
df['price'] = df['price'].str.replace('$', '', regex=False).astype(float)

# Step 5: Calculate sales = price x quantity
df['sales'] = df['price'] * df['quantity']

# Step 6: Keep only the 3 columns we need
df = df[['sales', 'date', 'region']]

# Step 7: Save to processed_data.csv
df.to_csv('processed_data.csv', index=False)

print("Done! processed_data.csv has been created.")
print(df.head(10))