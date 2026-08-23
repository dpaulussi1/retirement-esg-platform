from pathlib import Path
import pandas as pd

resultados = []

DATA_DIR = Path("data/prices")

for arquivo in DATA_DIR.glob("*.csv"):

    print(f"Processando: {arquivo.name}")

    df = pd.read_csv(
        arquivo,
        skiprows=3
    )

    # Converte a coluna de preços para número
    df.iloc[:, 1] = pd.to_numeric(
        df.iloc[:, 1],
        errors="coerce"
    )

    # Remove linhas inválidas
    preco_coluna = df.columns[1]

    df = (
        df.dropna(subset=[preco_coluna])
        .reset_index(drop=True)
    )

    # Preços inicial e final
    preco_inicial = float(df.iloc[0, 1])
    preco_final = float(df.iloc[-1, 1])

    # Retorno acumulado
    retorno = (
        (preco_final / preco_inicial) - 1
    ) * 100

    # Retornos diários
    retornos_diarios = (
        df.iloc[:, 1]
        .pct_change()
        .dropna()
    )

    # Volatilidade anualizada
    volatilidade = (
        retornos_diarios.std()
        * (252 ** 0.5)
        * 100
    )

    # Sharpe simplificado
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
        "drawdown": round(max_drawdown, 2)
    })

print(
    arquivo.stem,
    retorno,
    volatilidade,
    sharpe,
    drawdowns
)
print("\nTotal de ativos processados:")
print(len(resultados))

print("\nAtivos processados:")
for ativo in resultados:
    print(ativo["ticker"])

fundamentals = pd.DataFrame(resultados)

print(fundamentals)

fundamentals.to_csv(
    "data/fundamentals/fundamentals.csv",
    index=False
)