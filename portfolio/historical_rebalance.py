from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent

sys.path.append(str(ROOT_DIR))

import pandas as pd

from config.settings import (
    START_DATE,
    END_DATE,
    REBALANCE_FREQUENCY
)

if REBALANCE_FREQUENCY == "semiannual":
    datas = pd.date_range(
        start=START_DATE,
        end=END_DATE,
        freq="6MS"
    )

DATA_TESTE = "2018-07-01"

print(
    f"Data teste: {DATA_TESTE}"
)

df = pd.read_csv(
    "data/prices/PETR4.SA.csv",
    skiprows=2
)

df["Date"] = pd.to_datetime(
    df["Date"]
)

df_cortado = df[
    df["Date"] <= DATA_TESTE
]

print(
    df_cortado.tail()
)

datas = pd.date_range(
    start=START_DATE,
    end=END_DATE,
    freq="6MS"
)

RANKING_FILE = "data/scoring/ranking.csv"

ranking = pd.read_csv(
    RANKING_FILE
)

REGISTROS = []

for data in datas:

    top6 = ranking.head(6)

    for _, ativo in top6.iterrows():

        REGISTROS.append(
            {
                "rebalance_date": data.strftime(
                    "%Y-%m-%d"
                ),
                "ticker": ativo["ticker"],
                "retirement_score": ativo[
                    "retirement_score"
                ]
            }
        )

historico = pd.DataFrame(
    REGISTROS
)

print(historico.head(20))