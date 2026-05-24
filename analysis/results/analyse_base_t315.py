import csv
from pathlib import Path

import matplotlib.pyplot as plt


data_dir = Path("snoopy-output/base_with_t315")
plot_dir = Path("analysis/results/output/base_t315")
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
ilk_protein_values = []
ilk_activity_values = []
pakt_values = []
pmtor_values = []

for name, file_name in conditions:
    file_path = data_dir / file_name

    with file_path.open() as file:
        rows = list(csv.DictReader(file))

    last_row = rows[-1]
    names.append(name)
    hif_values.append(float(last_row["S3_HIF"]))
    ilk_protein_values.append(float(last_row["ILK_protein"]))
    ilk_activity_values.append(float(last_row["ILK_activity"]))
    pakt_values.append(float(last_row["p_473S_Akt"]))
    pmtor_values.append(float(last_row["p_mTOR"]))

print("Base with T315 final values at time 10000")
print("Condition\tHIF\tILK_protein\tILK_activity\tpAkt\tp_mTOR")
for i in range(len(names)):
    print(
        f"{names[i]}\t"
        f"{hif_values[i]:.3f}\t"
        f"{ilk_protein_values[i]:.3f}\t"
        f"{ilk_activity_values[i]:.3f}\t"
        f"{pakt_values[i]:.3f}\t"
        f"{pmtor_values[i]:.3f}"
    )

doses = [0, 0.2, 0.6, 1.2]
dose_labels = ["0", "0.2", "0.6", "1.2"]

dose_ilk_activity = ilk_activity_values[1:]
dose_pakt = pakt_values[1:]
dose_pmtor = pmtor_values[1:]
dose_hif = hif_values[1:]
dose_ilk_protein = ilk_protein_values[1:]

plt.figure(figsize=(7, 4))
plt.plot(doses, dose_ilk_activity, marker="o", label="ILK_activity")
plt.plot(doses, dose_pakt, marker="o", label="p_473S_Akt")
plt.plot(doses, dose_pmtor, marker="o", label="p_mTOR")
plt.xlabel("T315 marking under hypoxia")
plt.ylabel("Final value")
plt.title("T315 dose response in ILK signaling")
plt.xticks(doses, dose_labels)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(plot_dir / "t315_dose_response_pathway.png", dpi=200)
plt.close()

plt.figure(figsize=(7, 4))
plt.bar(dose_labels, dose_hif, color="tab:red")
plt.xlabel("T315 marking under hypoxia")
plt.ylabel("Final S3_HIF")
plt.title("HIF response to T315 under hypoxia")
plt.tight_layout()
plt.savefig(plot_dir / "t315_dose_response_hif.png", dpi=200)
plt.close()

plt.figure(figsize=(7, 4))
plt.plot(doses, dose_ilk_protein, marker="o", label="ILK_protein")
plt.plot(doses, dose_ilk_activity, marker="o", label="ILK_activity")
plt.xlabel("T315 marking under hypoxia")
plt.ylabel("Final value")
plt.title("T315 changes ILK activity more than ILK protein")
plt.xticks(doses, dose_labels)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(plot_dir / "t315_ilk_protein_vs_activity.png", dpi=200)
plt.close()

print(f"Saved plots to {plot_dir}")
