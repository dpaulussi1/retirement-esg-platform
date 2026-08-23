from pathlib import Path
import pandas as pd

RANKING_FILE = Path("data/scoring/ranking.csv")

ranking = pd.read_csv(RANKING_FILE)
print(ranking)

portfolio = ranking.head(6)
portfolio["peso"] = (
    portfolio["retirement_score"]
    /
    portfolio["retirement_score"].sum()
    * 100
).round(2)

OUTPUT_FILE = Path("data/portfolio/portfolio.csv")
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
portfolio.to_csv(OUTPUT_FILE, index=False)

print(
    portfolio[
        [
            "ticker",
            "retirement_score",
            "peso"
        ]
    ]
)