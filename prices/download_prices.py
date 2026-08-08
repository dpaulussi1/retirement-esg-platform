import yfinance as yf
from pathlib import Path

import pandas as pd

tickers_df = pd.read_csv("data/tickers.csv")

TICKERS = tickers_df["ticker"].tolist()

OUTPUT_DIR = Path("data/prices")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

for ticker in TICKERS:

    try:

        print(f"Baixando {ticker}...")

        df = yf.download(
            ticker,
            start="2015-01-01",
            auto_adjust=True,
            progress=False
        )

        if df.empty:
            print(f"Nenhum dado encontrado para {ticker}")
            continue

        arquivo = OUTPUT_DIR / f"{ticker}.csv"

        df.to_csv(arquivo)

        print(f"Salvo: {arquivo}")

    except Exception as e:

        print(
            f"Erro ao baixar {ticker}: {e}"
        )

print("Processo concluído.")