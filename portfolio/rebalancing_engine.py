from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent

sys.path.append(str(ROOT_DIR))

from datetime import datetime
import pandas as pd

from config.settings import TOP_N_ASSETS
from config.settings import REBALANCE_FREQUENCY

print(
    f"Frequência de rebalanceamento: {REBALANCE_FREQUENCY}"
)

print(
    f"Quantidade de ativos: {TOP_N_ASSETS}"
)

RANKING_FILE = Path(
    "data/scoring/ranking.csv"
)

PORTFOLIO_FILE = Path(
    "data/portfolio/portfolio.csv"
)

ranking = pd.read_csv(
    RANKING_FILE
)

nova_carteira = ranking.head(
    TOP_N_ASSETS
)
print(
    f"Quantidade de ativos: {len(nova_carteira)}"
)
portfolio_original = pd.read_csv(
    PORTFOLIO_FILE
)

# Seleciona Top N definido no settings.py
nova_carteira = ranking.head(
    TOP_N_ASSETS
).copy()


# Calcula pesos
nova_carteira["peso"] = (
    nova_carteira["retirement_score"]
    /
    nova_carteira["retirement_score"].sum()
    * 100
).round(2)

# Salva carteira rebalanceada
nova_carteira.to_csv(
    "data/portfolio/rebalanced_portfolio.csv",
    index=False
)

# Cria registro histórico
historico = nova_carteira[
    [
        "ticker",
        "peso"
    ]
].copy()

historico["rebalance_id"] = (
    datetime.today().strftime("%Y%m%d")
)

historico["date"] = (
    datetime.today().strftime("%Y-%m-%d")
)

historico = historico[
    [
        "rebalance_id",
        "date",
        "ticker",
        "peso"
    ]
]

historico.to_csv(
    "data/rebalancing/rebalancing_history.csv",
    mode="a",
    header=False,
    index=False
)

print("\nCarteira Original")
print(
    portfolio_original[
        ["ticker", "peso"]
    ]
)

print("\nCarteira Rebalanceada")
print(
    nova_carteira[
        [
            "ticker",
            "retirement_score",
            "peso"
        ]
    ]
)

print("\nHistórico de Rebalanceamentos")

historico_csv = pd.read_csv(
    "data/rebalancing/rebalancing_history.csv"
)

print(historico_csv.tail())