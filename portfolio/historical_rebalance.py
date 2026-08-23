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

        if arquivo.stem == "^BVSP":
            continue

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

        if df.empty:
            continue

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

        retornos_diarios = (
            df.iloc[:, 1]
            .pct_change()
            .dropna()
        )

        volatilidade = (
            retornos_diarios.std()
            * (252 ** 0.5)
            * 100
        )

        sharpe = (
            retorno / volatilidade
        )

        curva = (
            1 + retornos_diarios
        ).cumprod()

        maximos = curva.cummax()

        drawdowns = (
            (curva - maximos)
            / maximos
        ) * 100

        drawdown = drawdowns.min()

        resultados.append(
            {
                "ticker": arquivo.stem,
                "retorno": round(retorno, 2),
                "volatilidade": round(volatilidade, 2),
                "sharpe": round(sharpe, 2),
                "drawdown": round(drawdown, 2)
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

REGISTROS_HISTORICOS = []

for data in datas:

    print(
        f"\nRebalanceamento: {data.strftime('%Y-%m-%d')}"
    )

    fundamentals = (
        gerar_fundamentos_historicos(
            data
        )
    )

    print(
    "\nFundamentos Históricos"
    )

    print(fundamentals)

    if fundamentals.empty:
        continue

    fundamentals["score_retorno"] = (
        fundamentals["retorno"]
        .rank(pct=True)
    )

    fundamentals["score_sharpe"] = (
        fundamentals["sharpe"]
        .rank(pct=True)
    )

    fundamentals["score_drawdown"] = (
        fundamentals["drawdown"]
        .rank(pct=True)
    )

    fundamentals["retirement_score"] = (
        fundamentals["score_retorno"] * 0.4
        +
        fundamentals["score_sharpe"] * 0.4
        +
        fundamentals["score_drawdown"] * 0.2
    )

    ranking_historico = (
        fundamentals
        .sort_values(
            "retirement_score",
            ascending=False
        )
    )

    top6 = ranking_historico.head(6)

    for _, ativo in top6.iterrows():

        REGISTROS_HISTORICOS.append(
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

    historico_df = pd.DataFrame(
        REGISTROS_HISTORICOS
    )

    historico_df.to_csv(
        "data/backtests/historical_portfolios.csv",
        index=False
    )

print(
    "\nCarteiras Históricas"
)

print(
    historico_df.head(20)
)

print(
    "\nRanking Histórico"
)

print(
    ranking_historico[
        [
            "ticker",
            "retirement_score"
        ]
    ]
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