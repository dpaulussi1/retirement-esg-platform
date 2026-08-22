from pathlib import Path
import pandas as pd

FUNDAMENTALS_FILE = Path(
    "data/fundamentals/fundamentals.csv"
)

fundamentals = pd.read_csv(
    FUNDAMENTALS_FILE
)

print(fundamentals)
fundamentals["retorno_score"] = (
    fundamentals["retorno"]
    .rank(pct=True)
    * 100
).round(2)

fundamentals["volatilidade_score"] = (
    fundamentals["volatilidade"]
    .rank(pct=True, ascending=False)
    * 100
).round(2)

fundamentals["drawdown_score"] = (
    fundamentals["drawdown"]
    .rank(pct=True, ascending=False)
    * 100
).round(2)

fundamentals["score"] = (
    fundamentals["sharpe"]
    .rank(pct=True)
    * 100
).round(2)

fundamentals["retirement_score"] = (
    fundamentals["retorno_score"] * 0.30
    +
    fundamentals["score"] * 0.40
    +
    fundamentals["volatilidade_score"] * 0.15
    +
    fundamentals["drawdown_score"] * 0.15
).round(2)

ranking = (
    fundamentals[
        [
            "ticker",
            "retirement_score"
        ]
    ]
    .sort_values(
        "retirement_score",
        ascending=False
    )
    .reset_index(drop=True)
)

OUTPUT_FILE = Path("data/scoring/ranking.csv")
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
ranking.to_csv(OUTPUT_FILE, index=False)
print(ranking)