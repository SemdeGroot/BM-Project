import csv
from pathlib import Path

import matplotlib.pyplot as plt


data_dir = Path("snoopy-output/main")
plot_dir = Path("analysis/results/output/main")
plot_dir.mkdir(parents=True, exist_ok=True)


def read_rows(file_name):
    with (data_dir / file_name).open() as file:
        return list(csv.DictReader(file))


def final_value(file_name, column):
    rows = read_rows(file_name)
    return float(rows[-1][column])


def relative(values):
    first = values[0]
    if first == 0:
        return values
    return [value / first for value in values]


oxygen_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
oxygen_files = [
    "main_o2_0_1_t315_0_il6_1_0.csv",
    "main_o2_0_2_t315_0_il6_1_0.csv",
    "main_o2_0_3_t315_0_il6_1_0.csv",
    "main_o2_0_4_t315_0_il6_1_0.csv",
    "main_o2_0_5_t315_0_il6_1_0.csv",
    "main_o2_0_6_t315_0_il6_1_0.csv",
    "main_o2_0_7_t315_0_il6_1_0.csv",
    "main_o2_0_8_t315_0_il6_1_0.csv",
    "main_o2_0_9_t315_0_il6_1_0.csv",
]

t315_values = [0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2]
t315_files = [
    "main_o2_0_1_t315_0_il6_1_0.csv",
    "main_o2_0_1_t315_0_2_il6_1_0.csv",
    "main_o2_0_1_t315_0_4_il6_1_0.csv",
    "main_o2_0_1_t315_0_6_il6_1_0.csv",
    "main_o2_0_1_t315_0_8_il6_1_0.csv",
    "main_o2_0_1_t315_1_0_il6_1_0.csv",
    "main_o2_0_1_t315_1_2_il6_1_0.csv",
]

il6_values = [0, 0.1, 0.5, 1.0, 1.5, 2.0]
il6_files = [
    "main_o2_0_1_t315_0_il6_0.csv",
    "main_o2_0_1_t315_0_il6_0_1.csv",
    "main_o2_0_1_t315_0_il6_0_5.csv",
    "main_o2_0_1_t315_0_il6_1_0.csv",
    "main_o2_0_1_t315_0_il6_1_5.csv",
    "main_o2_0_1_t315_0_il6_2_0.csv",
]


print("Final model values at time 10000")
print("Condition\tHIF\tILK_activity\tpAkt\tNFkB\tIL6\tpStat3\tE2F1\tSnail\tE_cadherin\tvimentin")
summary_files = [
    ("Normoxia", "main_o2_0_9_t315_0_il6_1_0.csv"),
    ("Hypoxia", "main_o2_0_1_t315_0_il6_1_0.csv"),
    ("T315 0.6", "main_o2_0_1_t315_0_6_il6_1_0.csv"),
    ("T315 1.2", "main_o2_0_1_t315_1_2_il6_1_0.csv"),
]
for name, file_name in summary_files:
    print(
        f"{name}\t"
        f"{final_value(file_name, 'S3_HIF'):.3f}\t"
        f"{final_value(file_name, 'ILK_activity'):.3f}\t"
        f"{final_value(file_name, 'p_473S_Akt'):.3f}\t"
        f"{final_value(file_name, 'NFkB_activity'):.3f}\t"
        f"{final_value(file_name, 'IL6'):.3f}\t"
        f"{final_value(file_name, 'p_Stat3'):.3f}\t"
        f"{final_value(file_name, 'E2F1'):.3f}\t"
        f"{final_value(file_name, 'Snail'):.3f}\t"
        f"{final_value(file_name, 'E_cadherin'):.3f}\t"
        f"{final_value(file_name, 'vimentin'):.3f}"
    )


plt.figure(figsize=(7, 4))
for column, label in [
    ("S3_HIF", "HIF"),
    ("ILK_activity", "ILK activity"),
    ("p_473S_Akt", "p-Akt"),
    ("p_mTOR", "p-mTOR"),
    ("NFkB_activity", "NF-kB"),
    ("IL6", "IL6"),
]:
    values = [final_value(file_name, column) for file_name in oxygen_files]
    plt.plot(oxygen_values, relative(values), marker="o", label=label)
plt.xlabel("O2 marking")
plt.ylabel("Final value relative to O2 0.1")
plt.title("Final model oxygen response")
plt.grid(True, alpha=0.3)
plt.legend(ncol=2)
plt.tight_layout()
plt.savefig(plot_dir / "main_oxygen_response.png", dpi=300)
plt.close()


plt.figure(figsize=(7, 4))
for column, label in [
    ("Snail", "Snail"),
    ("E_cadherin", "E-cadherin"),
    ("vimentin", "vimentin"),
]:
    values = [final_value(file_name, column) for file_name in oxygen_files]
    plt.plot(oxygen_values, relative(values), marker="o", label=label)
plt.xlabel("O2 marking")
plt.ylabel("Final value relative to O2 0.1")
plt.title("Oxygen response of EMT outputs")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(plot_dir / "main_oxygen_emt_response.png", dpi=300)
plt.close()


plt.figure(figsize=(7, 4))
for column, label in [
    ("ILK_activity", "ILK activity"),
    ("p_473S_Akt", "p-Akt"),
    ("p_mTOR", "p-mTOR"),
    ("NFkB_activity", "NF-kB"),
    ("IL6", "IL6"),
    ("p_Stat3", "p-Stat3"),
    ("E2F1", "E2F1"),
]:
    values = [final_value(file_name, column) for file_name in t315_files]
    plt.plot(t315_values, relative(values), marker="o", label=label)
plt.axvline(0.6, color="tab:gray", linestyle="--", linewidth=1)
plt.xlabel("T315 marking under hypoxia")
plt.ylabel("Final value relative to T315 0")
plt.title("T315 lowers ILK signaling and the IL6/NF-kB loop")
plt.grid(True, alpha=0.3)
plt.legend(ncol=2)
plt.tight_layout()
plt.savefig(plot_dir / "main_t315_signaling_response.png", dpi=300)
plt.close()


heatmap_labels = [
    "HIF",
    "ILK protein",
    "ILK activity",
    "p-Akt",
    "p-mTOR",
    "p-Stat3",
    "E2F1",
    "NF-kB",
    "IL6",
    "YB-1",
    "Foxo3a",
    "Snail",
    "Zeb1",
    "E-cadherin",
    "vimentin",
]
heatmap_columns = [
    "S3_HIF",
    "ILK_protein",
    "ILK_activity",
    "p_473S_Akt",
    "p_mTOR",
    "p_Stat3",
    "E2F1",
    "NFkB_activity",
    "IL6",
    "YB_1",
    "Foxo3a",
    "Snail",
    "Zeb1",
    "E_cadherin",
    "vimentin",
]
heatmap_values = []
for column in heatmap_columns:
    values = [final_value(file_name, column) for file_name in t315_files]
    heatmap_values.append(relative(values))

plt.figure(figsize=(8, 6))
plt.imshow(heatmap_values, aspect="auto", cmap="RdYlBu_r", vmin=0, vmax=1.4)
plt.colorbar(label="Final value relative to T315 0")
plt.xticks(range(len(t315_values)), [str(value) for value in t315_values])
plt.yticks(range(len(heatmap_labels)), heatmap_labels)
plt.xlabel("T315 marking under hypoxia")
plt.title("Full model T315 response")
for row in range(len(heatmap_values)):
    for col in range(len(heatmap_values[row])):
        plt.text(col, row, f"{heatmap_values[row][col]:.2f}", ha="center", va="center", fontsize=7)
plt.tight_layout()
plt.savefig(plot_dir / "main_t315_heatmap.png", dpi=300)
plt.close()


plt.figure(figsize=(7, 4))
for column, label in [
    ("YB_1", "YB-1"),
    ("Foxo3a", "Foxo3a"),
    ("Snail", "Snail"),
    ("Zeb1", "Zeb1"),
    ("E_cadherin", "E-cadherin"),
    ("vimentin", "vimentin"),
]:
    values = [final_value(file_name, column) for file_name in t315_files]
    plt.plot(t315_values, relative(values), marker="o", label=label)
plt.axvline(0.6, color="tab:gray", linestyle="--", linewidth=1)
plt.xlabel("T315 marking under hypoxia")
plt.ylabel("Final value relative to T315 0")
plt.title("T315 response of EMT outputs")
plt.grid(True, alpha=0.3)
plt.legend(ncol=2)
plt.tight_layout()
plt.savefig(plot_dir / "main_t315_emt_response.png", dpi=300)
plt.close()


plt.figure(figsize=(7, 4))
for column, label in [
    ("p_Stat3", "p-Stat3"),
    ("E2F1", "E2F1"),
    ("ILK_protein", "ILK protein"),
    ("ILK_activity", "ILK activity"),
    ("p_473S_Akt", "p-Akt"),
    ("NFkB_activity", "NF-kB"),
    ("IL6", "IL6"),
]:
    values = [final_value(file_name, column) for file_name in il6_files]
    plt.plot(il6_values, relative(values), marker="o", label=label)
plt.xlabel("Initial IL6 marking")
plt.ylabel("Final value relative to IL6 0")
plt.title("Final response to initial IL6")
plt.grid(True, alpha=0.3)
plt.legend(ncol=2)
plt.tight_layout()
plt.savefig(plot_dir / "main_il6_stimulation_response.png", dpi=300)
plt.close()


plt.figure(figsize=(7, 4))
for file_name, label in [
    ("main_o2_0_1_t315_0_il6_0.csv", "IL6 0"),
    ("main_o2_0_1_t315_0_il6_0_5.csv", "IL6 0.5"),
    ("main_o2_0_1_t315_0_il6_1_0.csv", "IL6 1.0"),
    ("main_o2_0_1_t315_0_il6_2_0.csv", "IL6 2.0"),
]:
    rows = read_rows(file_name)
    times = [float(row["Time"]) for row in rows if float(row["Time"]) <= 200]
    values = [float(row["p_Stat3"]) for row in rows if float(row["Time"]) <= 200]
    plt.plot(times, values, label=label)
plt.xlabel("Time")
plt.ylabel("p-Stat3")
plt.title("Transient p-Stat3 response to initial IL6")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(plot_dir / "main_il6_transient_response.png", dpi=300)
plt.close()


time_files = [
    ("Normoxia", "main_o2_0_9_t315_0_il6_1_0.csv"),
    ("Hypoxia", "main_o2_0_1_t315_0_il6_1_0.csv"),
    ("Hypoxia + T315 0.6", "main_o2_0_1_t315_0_6_il6_1_0.csv"),
    ("Hypoxia + T315 1.2", "main_o2_0_1_t315_1_2_il6_1_0.csv"),
]
time_columns = [
    ("S3_HIF", "HIF"),
    ("ILK_activity", "ILK activity"),
    ("NFkB_activity", "NF-kB"),
    ("Snail", "Snail"),
]

fig, axes = plt.subplots(2, 2, figsize=(9, 6))
axes = axes.flatten()
for plot_index, (column, title) in enumerate(time_columns):
    axis = axes[plot_index]
    for label, file_name in time_files:
        rows = read_rows(file_name)
        times = [float(row["Time"]) for row in rows]
        values = [float(row[column]) for row in rows]
        axis.plot(times, values, label=label)
    axis.set_title(title)
    axis.set_xlabel("Time")
    axis.set_ylabel(column)
    axis.grid(True, alpha=0.3)
axes[0].legend(fontsize=8)
plt.tight_layout()
plt.savefig(plot_dir / "main_time_course_comparison.png", dpi=300)
plt.close()


print(f"Saved plots to {plot_dir}")
