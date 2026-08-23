import pandas as pd

df = pd.read_csv(
    "data/prices/PETR4.SA.csv",
    skiprows=3
)

df = pd.read_csv(
    "data/prices/PETR4.SA.csv",
    skiprows=2
)

print(df.columns)

df["Date"] = pd.to_datetime(
    df["Date"]
)

df_cortado = df[
    df.iloc[:, 0] <= "2018-07-01"
]

print(df_cortado.head())
print()
print(df_cortado.tail())
print()
print(len(df_cortado))