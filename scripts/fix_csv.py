import pandas as pd

path = 'data/raw/ss_raw_conflict.csv'
df = pd.read_csv(path)

if 'Status' not in df.columns:
    df['Status'] = 'verified'
if 'Source URL' not in df.columns:
    df['Source URL'] = ''

# Fill existing NaNs in these new columns
df['Status'] = df['Status'].fillna('verified')
df['Source URL'] = df['Source URL'].fillna('')

df.to_csv(path, index=False)
print("CSV columns fixed successfully.")
