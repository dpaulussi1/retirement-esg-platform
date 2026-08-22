from pathlib import Path
import pandas as pd

RANKING_FILE = Path("data/scoring/ranking.csv")
ESG_FILE = Path("data/esg/esg_scores.csv")

ESG_FILE.parent.mkdir(parents=True, exist_ok=True)

if not ESG_FILE.exists():
    default_esg = pd.DataFrame(
        {
            "ticker": [
                "PETR4.SA",
                "WEGE3.SA",
                "VALE3.SA",
                "ITUB4.SA",
                "BBAS3.SA",
            ],
            "esg_score": [90.0, 82.0, 76.0, 68.0, 55.0],
        }
    )
    default_esg.to_csv(ESG_FILE, index=False)

ranking = pd.read_csv(RANKING_FILE)
esg = pd.read_csv(ESG_FILE)

portfolio = ranking.merge(esg, on="ticker", how="left")

portfolio["sustainability_score"] = (
    portfolio["retirement_score"] * 0.70
    +
    portfolio["esg_score"] * 0.30
).round(2)

print(esg)
print(
    portfolio[
        [
            "ticker",
            "retirement_score",
            "esg_score",
            "sustainability_score"
        ]
    ]
    .sort_values(
        "sustainability_score",
        ascending=False
    )
)