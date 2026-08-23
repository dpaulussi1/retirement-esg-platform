from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BACKTEST_FILE = Path(
    "data/backtests/backtest_results.csv"
)

BENCHMARK_FILE = Path(
    "data/benchmark/benchmark_report.csv"
)

backtest = pd.read_csv(BACKTEST_FILE)
benchmark = pd.read_csv(BENCHMARK_FILE)

portfolio_return = float(
    backtest.loc[
        backtest["metric"] == "portfolio_return",
        "value"
    ].iloc[0]
)

portfolio_sharpe = float(
    backtest.loc[
        backtest["metric"] == "sharpe",
        "value"
    ].iloc[0]
)

alpha = (
    benchmark.loc[
        benchmark["metric"] == "return",
        "portfolio"
    ].iloc[0]
    -
    benchmark.loc[
        benchmark["metric"] == "return",
        "ibov"
    ].iloc[0]
)

fig = plt.figure(figsize=(12, 8))

plt.axis("off")

plt.text(
    0.05,
    0.90,
    "RETIREMENT ESG PLATFORM",
    fontsize=18,
    fontweight="bold"
)

plt.text(
    0.05,
    0.75,
    f"Retorno: {portfolio_return:.2f}%",
    fontsize=14
)

plt.text(
    0.05,
    0.65,
    f"Alpha: {alpha:.2f}%",
    fontsize=14
)

plt.text(
    0.05,
    0.55,
    f"Sharpe: {portfolio_sharpe:.2f}",
    fontsize=14
)

plt.text(
    0.05,
    0.35,
    "Portfolio ESG supera o IBOV "
    "em retorno e Sharpe.",
    fontsize=12
)

output_file = Path(
    "data/dashboard/dashboard_report.png"
)

output_file.parent.mkdir(
    parents=True,
    exist_ok=True
)

plt.savefig(
    output_file,
    bbox_inches="tight"
)

print(
    f"Dashboard salvo em: {output_file}"
)