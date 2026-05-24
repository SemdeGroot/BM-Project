import csv
from pathlib import Path

import matplotlib.pyplot as plt


base_dir = Path("snoopy-output/base")
plot_dir = Path("analysis/results/output/base")
plot_dir.mkdir(parents=True, exist_ok=True)

o2_values = []
hif_values = []
ilk_values = []
pakt_values = []
pmtor_values = []

for i in range(1, 10):
    o2 = i / 10
    file_path = base_dir / f"o2_0_{i}.csv"

    with file_path.open() as file:
        rows = list(csv.DictReader(file))

    last_row = rows[-1]
    o2_values.append(o2)
    hif_values.append(float(last_row["S3_HIF"]))
    ilk_values.append(float(last_row["ILK_protein"]))
    pakt_values.append(float(last_row["p_473S_Akt"]))
    pmtor_values.append(float(last_row["p_mTOR"]))

print("Base model final values at time 10000")
print("O2\tHIF\tILK\tpAkt\tp_mTOR")
for i in range(len(o2_values)):
    print(
        f"{o2_values[i]:.1f}\t"
        f"{hif_values[i]:.3f}\t"
        f"{ilk_values[i]:.3f}\t"
        f"{pakt_values[i]:.3f}\t"
        f"{pmtor_values[i]:.3f}"
    )

plt.figure(figsize=(7, 4))
plt.plot(o2_values, hif_values, marker="o", color="tab:red")
plt.xlabel("O2 marking")
plt.ylabel("Final S3_HIF")
plt.title("Base model HIF response to oxygen")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(plot_dir / "base_hif_o2_response.png", dpi=200)
plt.close()

plt.figure(figsize=(7, 4))
plt.plot(o2_values, ilk_values, marker="o", label="ILK_protein")
plt.plot(o2_values, pakt_values, marker="o", label="p_473S_Akt")
plt.plot(o2_values, pmtor_values, marker="o", label="p_mTOR")
plt.xlabel("O2 marking")
plt.ylabel("Final value")
plt.title("Base model ILK pathway response to oxygen")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(plot_dir / "base_pathway_o2_response.png", dpi=200)
plt.close()

print(f"Saved plots to {plot_dir}")
