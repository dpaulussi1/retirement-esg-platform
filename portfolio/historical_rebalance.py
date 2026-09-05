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

REGISTROS_HISTORICOS = []

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

        if len(df) < 2:
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

        if volatilidade == 0:
            sharpe = 0
        else:
            sharpe = retorno / volatilidade

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

    #print(
    #"\nFundamentos Históricos"
    #)

    #print(fundamentals)

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

#print(
#    "\nRanking Histórico"
#)

#print(
#    ranking_historico[
#        [
#            "ticker",
#            "retirement_score"
#        ]
#    ]
#)

datas = pd.date_range(
    start=START_DATE,
    end=END_DATE,
    freq="6MS"
)

# =====================================
# RETORNOS HISTÓRICOS
# =====================================

historico = pd.read_csv(
    "data/backtests/historical_portfolios.csv"
)

RETORNOS = []

for i in range(len(datas) - 1):

    data_inicio = (
        datas[i]
        .strftime("%Y-%m-%d")
    )

    data_fim = (
        datas[i + 1]
        .strftime("%Y-%m-%d")
    )

    carteira = historico[
        historico["rebalance_date"]
        == data_inicio
    ]

    if carteira.empty:
        continue

    retornos = []

    print(
        f"\nPeríodo: {data_inicio} -> {data_fim}"
    )

    for ticker in carteira["ticker"]:

        arquivo = (
            Path("data/prices")
            / f"{ticker}.csv"
        )

        if not arquivo.exists():
            continue

        df = pd.read_csv(
            arquivo,
            skiprows=2
        )

        df["Date"] = pd.to_datetime(
            df["Date"]
        )

        df_inicio = df[
            df["Date"] <= data_inicio
        ]

        df_fim = df[
            df["Date"] <= data_fim
        ]

        if (
            df_inicio.empty
            or
            df_fim.empty
        ):
            continue

        preco_inicio = float(
            df_inicio.iloc[-1, 1]
        )

        preco_fim = float(
            df_fim.iloc[-1, 1]
        )

        retorno = (
            preco_fim
            / preco_inicio
        ) - 1

        retornos.append(
            retorno
        )

        print(
            f"{ticker}: {retorno:.2%}"
        )

    if len(retornos) == 0:
        continue

    retorno_carteira = (
        sum(retornos)
        /
        len(retornos)
    )

    print(
        f"Retorno da Carteira: "
        f"{retorno_carteira:.2%}"
    )

    RETORNOS.append(
        {
            "data_inicio": data_inicio,
            "data_fim": data_fim,
            "retorno": round(
                retorno_carteira,
                4
            )
        }
    )

retornos_df = pd.DataFrame(
    RETORNOS
)

retornos_df.to_csv(
    "data/backtests/historical_returns.csv",
    index=False
)

print(
    "\nRetornos Históricos"
)

print(
    retornos_df.head()
)

# =====================================
# CURVA PATRIMONIAL
# =====================================

capital = 100.0

PATRIMONIO = []

for _, row in retornos_df.iterrows():

    capital *= (
        1 + row["retorno"]
    )

    PATRIMONIO.append(
        {
            "data": row["data_fim"],
            "capital": round(
                capital,
                2
            )
        }
    )

patrimonio_df = pd.DataFrame(
    PATRIMONIO
)

patrimonio_df.to_csv(
    "data/backtests/equity_curve.csv",
    index=False
)

print(
    "\nCurva Patrimonial"
)

print(
    patrimonio_df.head()
)

print(
    "\nCapital Final"
)

print(
    f"R$ {capital:.2f}"
)

capital_final = patrimonio_df.iloc[-1]["capital"]

print(
    f"\nCapital Final: {capital_final:.2f}"
)

anos = (
    len(retornos_df) * 0.5
)

cagr = (
    (capital_final / 100)
    ** (1 / anos)
    - 1
)

print(
    f"CAGR: {cagr:.2%}"
)

serie = patrimonio_df["capital"]

maximos = serie.cummax()

drawdowns = (
    serie - maximos
) / maximos

max_drawdown = drawdowns.min()

print(
    f"Max Drawdown: {max_drawdown:.2%}"
)

patrimonio_df["maximo"] = (
    patrimonio_df["capital"]
    .cummax()
)

patrimonio_df["drawdown"] = (
    patrimonio_df["capital"]
    /
    patrimonio_df["maximo"]
    - 1
)

max_drawdown = (
    patrimonio_df["drawdown"]
    .min()
)

print(
    f"Max Drawdown: {max_drawdown:.2%}"
)

capital_inicial = 100

retorno_total = (
    capital_final / capital_inicial
) - 1

print(
    f"Retorno Total: {retorno_total:.2%}"
)