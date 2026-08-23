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

for ticker in portfolio["ticker"]:

    print(f"Lendo preços de {ticker}")

    arquivo = f"data/prices/{ticker}.csv"

    df = pd.read_csv(
        arquivo,
        skiprows=3
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

    retorno_carteira += contribuicao
    retornos_carteira.append(contribuicao)

    print(
        f"Contribuição: {contribuicao:.2f}%"
    )

resultado = pd.DataFrame(
    {
        "metric": ["portfolio_return"],
        "value": [round(retorno_carteira, 2)]
    }
)

resultado.to_csv(
    "data/backtests/backtest_results.csv",
    index=False
)

anos = 10

retorno_anualizado = (
    (
        (1 + retorno_carteira / 100)
        ** (1 / anos)
    )
    - 1
) * 100

volatilidade_carteira = np.std(
    retornos_carteira
)

sharpe_carteira = (
    retorno_anualizado
    /
    volatilidade_carteira
)

maior_contribuicao = max(retornos_carteira)

menor_contribuicao = min(retornos_carteira)

drawdown_carteira = (
    (menor_contribuicao - maior_contribuicao)
    / maior_contribuicao
) * 100

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