import subprocess
import sys

from config.settings import REBALANCE_FREQUENCY

print(
    f"Frequência de rebalanceamento: {REBALANCE_FREQUENCY}"
)

scripts = [
    "prices/download_prices.py",
    "scoring/scoring_engine.py",
    "portfolio/portfolio_manager.py",
    "benchmark/benchmark_engine.py",
    "dashboard/dashboard.py",
    "portfolio/rebalancing_engine.py"
]

for script in scripts:

    print(f"\nExecutando: {script}")

    subprocess.run(
        [sys.executable, script],
        check=True
    )

print(
    "\n✅ Plataforma executada com sucesso!"
)