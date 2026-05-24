import csv
from pathlib import Path

import matplotlib.pyplot as plt

data_dir = Path("snoopy-output/chou_extended")
plot_dir = Path("analysis/results/output/chou_extended")
plot_dir.mkdir(parents=True, exist_ok=True)

conditions = [
    ("Normoxia", "normoxia_t315_0.csv"),
    ("Hypoxia", "hypoxia_t315_0.csv"),
    ("T315 0.2", "hypoxia_t315_0_2.csv"),
    ("T315 0.6", "hypoxia_t315_0_6.csv"),
    ("T315 1.2", "hypoxia_t315_1_2.csv"),
]

names = []
hif_values = []
ilk_activity_values = []
yb1_values = []
foxo3a_values = []
snail_values = []
zeb1_values = []
ecadherin_values = []
vimentin_values = []

for name, file_name in conditions:
    file_path = data_dir / file_name

    with file_path.open() as file:
        rows = list(csv.DictReader(file))

    last_row = rows[-1]
    names.append(name)
    hif_values.append(float(last_row["S3_HIF"]))
    ilk_activity_values.append(float(last_row["ILK_activity"]))
    yb1_values.append(float(last_row["YB_1"]))
    foxo3a_values.append(float(last_row["Foxo3a"]))
    snail_values.append(float(last_row["Snail"]))
    zeb1_values.append(float(last_row["Zeb1"]))
    ecadherin_values.append(float(last_row["E_cadherin"]))
    vimentin_values.append(float(last_row["vimentin"]))

print("Chou extended final values at time 10000")
print("Condition\tHIF\tILK_activity\tYB_1\tFoxo3a\tSnail\tZeb1\tE_cadherin\tvimentin")
for i in range(len(names)):
    print(
        f"{names[i]}\t"
        f"{hif_values[i]:.3f}\t"
        f"{ilk_activity_values[i]:.3f}\t"
        f"{yb1_values[i]:.3f}\t"
        f"{foxo3a_values[i]:.3f}\t"
        f"{snail_values[i]:.3f}\t"
        f"{zeb1_values[i]:.3f}\t"
        f"{ecadherin_values[i]:.3f}\t"
        f"{vimentin_values[i]:.3f}"
    )

doses = [0, 0.2, 0.6, 1.2]
dose_labels = ["0", "0.2", "0.6", "1.2"]

dose_yb1 = yb1_values[1:]
dose_foxo3a = foxo3a_values[1:]
dose_snail = snail_values[1:]
dose_zeb1 = zeb1_values[1:]
dose_ecadherin = ecadherin_values[1:]
dose_vimentin = vimentin_values[1:]

plt.figure(figsize=(7, 4))
plt.plot(doses, dose_yb1, marker="o", label="YB_1")
plt.plot(doses, dose_foxo3a, marker="o", label="Foxo3a")
plt.xlabel("T315 marking under hypoxia")
plt.ylabel("Final value")
plt.title("T315 changes YB-1 and Foxo3a")
plt.xticks(doses, dose_labels)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(plot_dir / "chou_t315_yb1_foxo3a.png", dpi=200)
plt.close()

plt.figure(figsize=(7, 4))
plt.plot(doses, dose_snail, marker="o", label="Snail")
plt.plot(doses, dose_zeb1, marker="o", label="Zeb1")
plt.plot(doses, dose_vimentin, marker="o", label="vimentin")
plt.xlabel("T315 marking under hypoxia")
plt.ylabel("Final value")
plt.title("T315 lowers mesenchymal EMT markers")
plt.xticks(doses, dose_labels)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(plot_dir / "chou_t315_mesenchymal_markers.png", dpi=200)
plt.close()

plt.figure(figsize=(7, 4))
plt.plot(doses, dose_ecadherin, marker="o", color="tab:green")
plt.axhline(ecadherin_values[0], color="tab:gray", linestyle="--", label="Normoxia")
plt.xlabel("T315 marking under hypoxia")
plt.ylabel("Final E_cadherin")
plt.title("T315 partly restores E-cadherin under hypoxia")
plt.xticks(doses, dose_labels)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(plot_dir / "chou_t315_ecadherin.png", dpi=200)
plt.close()

print(f"Saved plots to {plot_dir}")