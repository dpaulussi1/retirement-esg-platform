from pathlib import Path
import pandas as pd
import numpy as np

PORTFOLIO_FILE = Path(
    "data/portfolio/portfolio.csv"
)

portfolio = pd.read_csv(PORTFOLIO_FILE)

print(portfolio)

retorno_carteira = 0
retornos_carteira = []
retornos_diarios_portfolio = None

for ticker in portfolio["ticker"]:

    print(f"Lendo preços de {ticker}")

    arquivo = f"data/prices/{ticker}.csv"

    df = pd.read_csv(
        arquivo,
        skiprows=3
    )
    retornos_diarios = (
        df.iloc[:, 1]
        .pct_change()
        .dropna()
    )

    print(df.head())

    preco_inicial = float(df.iloc[0, 1])

    preco_final = float(df.iloc[-1, 1])

    retorno = (
        (preco_final / preco_inicial) - 1
    ) * 100

    print(f"Retorno: {retorno:.2f}%")

    peso = portfolio.loc[
        portfolio["ticker"] == ticker,
        "peso"
    ].iloc[0]

    contribuicao = (
        retorno * peso
    ) / 100

    retornos_ponderados = (
        retornos_diarios * (peso / 100)
    )

    if retornos_diarios_portfolio is None:
        retornos_diarios_portfolio = retornos_ponderados
    else:
        retornos_diarios_portfolio = (
            retornos_diarios_portfolio
            + retornos_ponderados
        )

    retorno_carteira += contribuicao
    retornos_carteira.append(contribuicao)

    print(
        f"Contribuição: {contribuicao:.2f}%"
    )

anos = 10

retorno_anualizado = (
    (
        (1 + retorno_carteira / 100)
        ** (1 / anos)
    )
    - 1
) * 100

volatilidade_carteira = (
    retornos_diarios_portfolio.std()
    * np.sqrt(252)
    * 100
)

sharpe_carteira = (
    retorno_anualizado
    /
    volatilidade_carteira
)

curva_carteira = (
    1 + retornos_diarios_portfolio
).cumprod()

curva_df = pd.DataFrame(
    {
        "portfolio": curva_carteira
    }
)

curva_df.to_csv(
    "data/backtests/portfolio_curve.csv",
    index=False
)

maximos = curva_carteira.cummax()

drawdowns = (
    (curva_carteira - maximos)
    / maximos
) * 100

drawdown_carteira = drawdowns.min()

resultado = pd.DataFrame(
    {
        "metric": [
            "portfolio_return",
            "annual_return",
            "volatility",
            "sharpe",
            "drawdown"
        ],
        "value": [
            round(retorno_carteira, 2),
            round(retorno_anualizado, 2),
            round(volatilidade_carteira, 2),
            round(sharpe_carteira, 2),
            round(drawdown_carteira, 2)
        ]
    }
)

resultado.to_csv(
    "data/backtests/backtest_results.csv",
    index=False
)

print(
    f"Retorno da Carteira: {retorno_carteira:.2f}%"
)
print(
    f"Retorno Anualizado: {retorno_anualizado:.2f}%"
)
print(
    f"Volatilidade da Carteira: {volatilidade_carteira:.2f}%"
)
print(
    f"Sharpe da Carteira: {sharpe_carteira:.2f}"
)
print(
    f"Drawdown da Carteira: {drawdown_carteira:.2f}%"
)