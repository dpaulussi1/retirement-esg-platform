from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PORTFOLIO_CURVE = Path(
    "data/backtests/portfolio_curve.csv"
)

IBOV_CURVE = Path(
    "data/benchmark/ibov_curve.csv"
)

portfolio = pd.read_csv(
    PORTFOLIO_CURVE
)

ibov = pd.read_csv(
    IBOV_CURVE
)

tamanho = min(
    len(portfolio),
    len(ibov)
)

portfolio = portfolio.iloc[:tamanho]
ibov = ibov.iloc[:tamanho]

plt.figure(figsize=(12, 6))

plt.plot(
    portfolio["portfolio"],
    label="Portfolio ESG",
    linewidth=2
)

plt.plot(
    ibov["ibov"],
    label="IBOV",
    linewidth=2
)

plt.title(
    "Portfolio ESG vs IBOV"
)

plt.xlabel("Períodos")

plt.ylabel("Valor Acumulado")

plt.legend()

plt.grid(True)

plt.tight_layout()

output_file = Path(
    "data/benchmark/equity_curve.png"
)

plt.savefig(output_file)

print(
    f"Gráfico salvo em: {output_file}"
)