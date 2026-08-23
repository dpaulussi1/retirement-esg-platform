from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent

sys.path.append(str(ROOT_DIR))

import pandas as pd
import numpy as np

from config.settings import (
    BENCHMARK,
    RISK_FREE_RATE
)

BACKTEST_FILE = Path(
    "data/backtests/backtest_results.csv"
)

IBOV_FILE = Path(
    f"data/prices/{BENCHMARK}.csv"
)

backtest = pd.read_csv(
    BACKTEST_FILE
)

portfolio_return = float(
    backtest.loc[
        backtest["metric"] == "portfolio_return",
        "value"
    ].iloc[0]
)

portfolio_annual_return = float(
    backtest.loc[
        backtest["metric"] == "annual_return",
        "value"
    ].iloc[0]
)

portfolio_volatility = float(
    backtest.loc[
        backtest["metric"] == "volatility",
        "value"
    ].iloc[0]
)

portfolio_sharpe = float(
    backtest.loc[
        backtest["metric"] == "sharpe",
        "value"
    ].iloc[0]
)

portfolio_sortino = float(
    backtest.loc[
        backtest["metric"] == "sortino",
        "value"
    ].iloc[0]
)

portfolio_calmar = float(
    backtest.loc[
        backtest["metric"] == "calmar",
        "value"
    ].iloc[0]
)

portfolio_win_rate = float(
    backtest.loc[
        backtest["metric"] == "win_rate",
        "value"
    ].iloc[0]
)

ibov = pd.read_csv(
    IBOV_FILE,
    skiprows=3
)

retornos_diarios_ibov = (
    ibov.iloc[:, 1]
    .pct_change()
    .dropna()
)

curva_ibov = (
    1 + retornos_diarios_ibov
).cumprod()

curva_ibov_df = pd.DataFrame(
    {
        "ibov": curva_ibov
    }
)

curva_ibov_df.to_csv(
    "data/benchmark/ibov_curve.csv",
    index=False
)

retorno_carteira = float(
    backtest.iloc[0]["value"]
)

preco_inicial = float(
    ibov.iloc[0, 1]
)

preco_final = float(
    ibov.iloc[-1, 1]
)

retorno_ibov = (
    (preco_final / preco_inicial) - 1
) * 100

anos = 10

retorno_anualizado_ibov = (
    (
        (1 + retorno_ibov / 100)
        ** (1 / anos)
    )
    - 1
) * 100

volatilidade_ibov = (
    retornos_diarios_ibov.std()
    * np.sqrt(252)
    * 100
)

retornos_negativos_ibov = (
    retornos_diarios_ibov[
        retornos_diarios_ibov < 0
    ]
)

downside_volatility_ibov = (
    retornos_negativos_ibov.std()
    * np.sqrt(252)
    * 100
)

sortino_ibov = (
    (
        retorno_anualizado_ibov
        -
        (RISK_FREE_RATE * 100)
    )
    /
    downside_volatility_ibov
)

sharpe_ibov = (
    (
        retorno_anualizado_ibov
        -
        (RISK_FREE_RATE * 100)
    )
    /
    volatilidade_ibov
)

relatorio = pd.DataFrame(
    {
        "metric": [
            "return",
            "annual_return",
            "volatility",
            "sharpe",
            "sortino",
            "calmar",
            "win_rate"
        ],
        "portfolio": [
    portfolio_return,
    portfolio_annual_return,
    portfolio_volatility,
    portfolio_sharpe,
    portfolio_sortino,
    portfolio_calmar,
    portfolio_win_rate
        ],
        "ibov": [
            round(retorno_ibov, 2),
            round(retorno_anualizado_ibov, 2),
            round(volatilidade_ibov, 2),
            round(sharpe_ibov, 2),
            round(sortino_ibov, 2),
            np.nan,
            np.nan
        ]
    }
)

relatorio.to_csv(
    "data/benchmark/benchmark_report.csv",
    index=False
)

alpha = (
    retorno_carteira - retorno_ibov
)

print(
    f"Retorno Carteira: {retorno_carteira:.2f}%"
)

print(
    f"Retorno IBOV: {retorno_ibov:.2f}%"
)

print(
    f"Alpha: {alpha:.2f}%"
)
print(
    f"Retorno Anualizado IBOV: {retorno_anualizado_ibov:.2f}%"
)
print(
    f"Volatilidade IBOV: {volatilidade_ibov:.2f}%"
)
print(
    f"Sharpe IBOV: {sharpe_ibov:.2f}"
)
print(
    f"Sortino IBOV: {sortino_ibov:.2f}"
)
print(
    f"Sortino da Carteira: {portfolio_sortino:.2f}"
)
print(relatorio)
print(
    f"Calmar da Carteira: {portfolio_calmar:.2f}"
)
print(
    f"Win Rate da Carteira: {portfolio_win_rate:.2f}%"
)