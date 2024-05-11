import pandas as pd

df = pd.read_csv("0ham_veri.csv")
df['FL_DATE'] = pd.to_datetime(df['FL_DATE'])
belirli_tarih = pd.to_datetime('2023-05-11')
filtre = df['FL_DATE'] >= belirli_tarih
filtrelenmis_df = df[filtre]
filtrelenmis_df.to_csv("1tarihduzenlenmis.csv", index=False)
