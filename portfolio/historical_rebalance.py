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

def gerar_fundamentos_historicos(
    data_referencia
):

    resultados = []

    DATA_DIR = Path("data/prices")

    for arquivo in DATA_DIR.glob("*.csv"):

        df = pd.read_csv(
            arquivo,
            skiprows=2
        )

        df["Date"] = pd.to_datetime(
            df["Date"]
        )

        df = df[
            df["Date"] <= data_referencia
        ]

        preco_inicial = float(
            df.iloc[0, 1]
        )

        preco_final = float(
            df.iloc[-1, 1]
        )

        retorno = (
            (preco_final / preco_inicial)
            - 1
        ) * 100

        resultados.append(
            {
                "ticker": arquivo.stem,
                "retorno": round(
                    retorno,
                    2
                )
            }
        )

    return pd.DataFrame(
        resultados
    )

if REBALANCE_FREQUENCY == "semiannual":
    datas = pd.date_range(
        start=START_DATE,
        end=END_DATE,
        freq="6MS"
    )

DATA_TESTE = "2018-07-01"

fundamentals = (
    gerar_fundamentos_historicos(
        DATA_TESTE
    )
)

print(
    "\nFundamentos Históricos"
)

print(fundamentals)

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