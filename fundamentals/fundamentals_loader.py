from pathlib import Path
import pandas as pd

resultados = []

DATA_DIR = Path("data/prices")

for arquivo in DATA_DIR.glob("*.csv"):
    print(arquivo.stem)

    df = pd.read_csv(arquivo, skiprows=3)

    # Ensure the price column is numeric (coerce non-numeric to NaN)
    df.iloc[:, 1] = pd.to_numeric(df.iloc[:, 1], errors="coerce")

    # Drop rows where the price is NaN after coercion
    price_col = df.columns[1]
    df = df.dropna(subset=[price_col]).reset_index(drop=True)

    # Use the first and last numeric prices
    preco_inicial = float(df.iloc[0, 1])
    preco_final = float(df.iloc[-1, 1])

    retorno = ((preco_final / preco_inicial) - 1) * 100

    # Daily returns from the numeric price column
    retornos_diarios = df.iloc[:, 1].pct_change().dropna()
    volatilidade = retornos_diarios.std() * (252 ** 0.5) * 100
    sharpe = retorno / volatilidade
    maximos = df.iloc[:, 1].cummax()

    drawdowns = (
        (df.iloc[:, 1] - maximos)
        / maximos
    ) * 100

    max_drawdown = drawdowns.min()

    resultados.append({
        "ticker": arquivo.stem,
        "retorno": round(retorno, 2),
        "volatilidade": round(volatilidade, 2),
        "sharpe": round(sharpe, 2),
        "drawdown": round(max_drawdown, 2),
    })

fundamentals = pd.DataFrame(resultados)

print(fundamentals)

print(type(fundamentals))

print("CHEGUEI AQUI")

fundamentals.to_csv(
    "data/fundamentals/fundamentals.csv",
    index=False
)