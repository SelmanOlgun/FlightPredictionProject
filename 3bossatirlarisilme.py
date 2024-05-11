import pandas as pd

df = pd.read_csv('2gereksizsutunlarsilinmis.csv')
df.dropna(inplace=True)

df.to_csv('3bossatirlarisilinmis.csv', index=False)
