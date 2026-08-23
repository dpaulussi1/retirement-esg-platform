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

if REBALANCE_FREQUENCY == "semiannual":
    datas = pd.date_range(
        start=START_DATE,
        end=END_DATE,
        freq="6MS"
    )

for data in datas:
    print(
        data.strftime("%Y-%m-%d")
    )

print()

print(
    f"Total de rebalanceamentos: {len(datas)}"
)