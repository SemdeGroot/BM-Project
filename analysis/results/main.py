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


def scaled_to_max(values):
    top = max(values)
    if top == 0:
        return values
    return [value / top for value in values]


# Group A: oxygen sweep, T315 = 0, IL6 = 1.0 (dynamic)
oxygen_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
oxygen_files = [f"main_o2_0_{i}_t315_0_il6_1_0.csv" for i in range(1, 10)]

# Group B: T315 dose response under hypoxia (O2 = 0.1, IL6 = 1.0 dynamic)
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

# Group C: IL6 stimulation, IL6 held FIXED (sustained stimulus), O2 = 0.1
il6_values = [0, 0.1, 0.5, 1.0, 1.5, 2.0]
il6_files = [
    "main_o2_0_1_t315_0_il6_0_fix.csv",
    "main_o2_0_1_t315_0_il6_0_1_fix.csv",
    "main_o2_0_1_t315_0_il6_0_5_fix.csv",
    "main_o2_0_1_t315_0_il6_1_0_fix.csv",
    "main_o2_0_1_t315_0_il6_1_5_fix.csv",
    "main_o2_0_1_t315_0_il6_2_0_fix.csv",
]

# Group D: T315 dose under IL6 stimulation (IL6 fixed = 1.0). T315 = 0 reuses C.
t315_loop_values = [0, 0.6, 1.2]
t315_loop_files = [
    "main_o2_0_1_t315_0_il6_1_0_fix.csv",
    "main_o2_0_1_t315_0_6_il6_1_0_fix.csv",
    "main_o2_0_1_t315_1_2_il6_1_0_fix.csv",
]


print("Final values at time 10000 (hypoxia/normoxia and T315)")
print("cond\tHIF\tILK_act\tp_Akt\tNFkB\tSnail\tE_cad\tFoxo3a")
for name, file_name in [
    ("Normoxia", "main_o2_0_9_t315_0_il6_1_0.csv"),
    ("Hypoxia", "main_o2_0_1_t315_0_il6_1_0.csv"),
    ("Hyp+T315 0.6", "main_o2_0_1_t315_0_6_il6_1_0.csv"),
    ("Hyp+T315 1.2", "main_o2_0_1_t315_1_2_il6_1_0.csv"),
]:
    print(
        f"{name}\t"
        f"{final_value(file_name, 'S3_HIF'):.2f}\t"
        f"{final_value(file_name, 'ILK_activity'):.3f}\t"
        f"{final_value(file_name, 'p_473S_Akt'):.3f}\t"
        f"{final_value(file_name, 'NFkB_activity'):.3f}\t"
        f"{final_value(file_name, 'Snail'):.2f}\t"
        f"{final_value(file_name, 'E_cadherin'):.3f}\t"
        f"{final_value(file_name, 'Foxo3a'):.3f}"
    )


# F1 - HIF-ILK oxygen switch (foundation, Chou Fig 1 hypoxia effect)
hif = [final_value(f, "S3_HIF") for f in oxygen_files]
ilk = [final_value(f, "ILK_activity") for f in oxygen_files]
fig, ax1 = plt.subplots(figsize=(7, 4))
ax1.plot(oxygen_values, hif, "o-", color="tab:blue", label="HIF")
ax1.set_xlabel("O2 marking")
ax1.set_ylabel("HIF (final value)", color="tab:blue")
ax1.tick_params(axis="y", labelcolor="tab:blue")
ax2 = ax1.twinx()
ax2.plot(oxygen_values, ilk, "s-", color="tab:red", label="ILK activity")
ax2.set_ylabel("ILK activity (final value)", color="tab:red")
ax2.tick_params(axis="y", labelcolor="tab:red")
ax1.set_title("HIF-ILK oxygen switch")
ax1.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(plot_dir / "main_oxygen_switch.png", dpi=300)
plt.close()


# F2 - EMT markers across oxygen (Chou Fig 1A-B). Each marker scaled to its own
# maximum so up- and down-regulated markers fit one panel.
plt.figure(figsize=(7, 4))
for column, label in [
    ("Snail", "Snail"),
    ("Zeb1", "Zeb1"),
    ("vimentin", "vimentin"),
    ("E_cadherin", "E-cadherin"),
    ("Foxo3a", "Foxo3a"),
]:
    values = [final_value(f, column) for f in oxygen_files]
    plt.plot(oxygen_values, scaled_to_max(values), marker="o", label=label)
plt.xlabel("O2 marking")
plt.ylabel("Final value scaled to marker maximum")
plt.title("EMT markers across oxygen (hypoxia drives EMT)")
plt.grid(True, alpha=0.3)
plt.legend(ncol=2)
plt.tight_layout()
plt.savefig(plot_dir / "main_oxygen_emt.png", dpi=300)
plt.close()


# F3 - T315 dose response of the ILK signaling axis (Chou Fig 3A, Lee IC50)
plt.figure(figsize=(7, 4))
for column, label in [
    ("ILK_activity", "ILK activity"),
    ("p_473S_Akt", "p-Akt"),
    ("p_mTOR", "p-mTOR"),
    ("p_GSK3beta", "p-GSK3beta"),
]:
    values = [final_value(f, column) for f in t315_files]
    plt.plot(t315_values, relative(values), marker="o", label=label)
plt.axvline(0.6, color="tab:gray", linestyle="--", linewidth=1, label="IC50 = 0.6")
plt.xlabel("T315 marking under hypoxia")
plt.ylabel("Final value relative to T315 = 0")
plt.title("T315 inhibits the ILK signaling axis")
plt.grid(True, alpha=0.3)
plt.legend(ncol=2)
plt.tight_layout()
plt.savefig(plot_dir / "main_t315_signaling.png", dpi=300)
plt.close()


# F4 - T315 reverses EMT (Chou Fig 3A, Fig 7B-C)
plt.figure(figsize=(7, 4))
for column, label in [
    ("YB_1", "YB-1"),
    ("Snail", "Snail"),
    ("Zeb1", "Zeb1"),
    ("vimentin", "vimentin"),
    ("Foxo3a", "Foxo3a"),
    ("E_cadherin", "E-cadherin"),
]:
    values = [final_value(f, column) for f in t315_files]
    plt.plot(t315_values, relative(values), marker="o", label=label)
plt.axvline(0.6, color="tab:gray", linestyle="--", linewidth=1)
plt.xlabel("T315 marking under hypoxia")
plt.ylabel("Final value relative to T315 = 0")
plt.title("T315 reverses EMT toward the epithelial state")
plt.grid(True, alpha=0.3)
plt.legend(ncol=2)
plt.tight_layout()
plt.savefig(plot_dir / "main_t315_emt.png", dpi=300)
plt.close()


# F5 - IL6 stimulation activates the Hsu loop (Hsu Fig 1B, 2, 3). IL6 fixed.
# Each readout scaled to its value at IL6 = 2.0 so the rise from IL6 = 0 is visible.
plt.figure(figsize=(7, 4))
for column, label in [
    ("p_Stat3", "p-Stat3"),
    ("E2F1", "E2F1"),
    ("ILK_protein", "ILK protein"),
    ("ILK_activity", "ILK activity"),
    ("p_473S_Akt", "p-Akt"),
    ("NFkB_activity", "NF-kB"),
]:
    values = [final_value(f, column) for f in il6_files]
    plt.plot(il6_values, scaled_to_max(values), marker="o", label=label)
plt.xlabel("Sustained IL6 marking (fixed)")
plt.ylabel("Final value scaled to IL6 = 2.0")
plt.title("IL6 activates the E2F1-ILK-NF-kB loop")
plt.grid(True, alpha=0.3)
plt.legend(ncol=2)
plt.tight_layout()
plt.savefig(plot_dir / "main_il6_stimulation.png", dpi=300)
plt.close()


# F6 - T315 suppresses the IL6/NF-kB loop (Hsu Fig 4E). IL6 fixed = 1.0.
loop_columns = [("p_Stat3", "p-Stat3"), ("E2F1", "E2F1"),
                ("ILK_activity", "ILK activity"), ("NFkB_activity", "NF-kB")]
plt.figure(figsize=(7, 4))
width = 0.2
for index, (column, label) in enumerate(loop_columns):
    values = [final_value(f, column) for f in t315_loop_files]
    rel = relative(values)
    positions = [x + index * width for x in range(len(t315_loop_values))]
    plt.bar(positions, rel, width=width, label=label)
plt.xticks([x + 1.5 * width for x in range(len(t315_loop_values))],
           [f"T315 = {v}" for v in t315_loop_values])
plt.ylabel("Final value relative to T315 = 0")
plt.title("T315 suppresses the IL6/NF-kB loop (IL6 fixed = 1.0)")
plt.grid(True, axis="y", alpha=0.3)
plt.legend(ncol=2)
plt.tight_layout()
plt.savefig(plot_dir / "main_t315_il6_loop.png", dpi=300)
plt.close()


# F7 - integrative heatmap: every marker across the T315 dose under hypoxia
heatmap_labels = ["HIF", "ILK protein", "ILK activity", "p-Akt", "p-mTOR",
                  "p-GSK3beta", "p-Stat3", "E2F1", "NF-kB", "IL6", "YB-1",
                  "Foxo3a", "Snail", "Zeb1", "E-cadherin", "vimentin"]
heatmap_columns = ["S3_HIF", "ILK_protein", "ILK_activity", "p_473S_Akt", "p_mTOR",
                   "p_GSK3beta", "p_Stat3", "E2F1", "NFkB_activity", "IL6", "YB_1",
                   "Foxo3a", "Snail", "Zeb1", "E_cadherin", "vimentin"]
heatmap_values = [relative([final_value(f, c) for f in t315_files]) for c in heatmap_columns]

plt.figure(figsize=(8, 6))
plt.imshow(heatmap_values, aspect="auto", cmap="RdYlBu_r", vmin=0, vmax=2)
plt.colorbar(label="Final value relative to T315 = 0")
plt.xticks(range(len(t315_values)), [str(v) for v in t315_values])
plt.yticks(range(len(heatmap_labels)), heatmap_labels)
plt.xlabel("T315 marking under hypoxia")
plt.title("Full model response to T315")
for row in range(len(heatmap_values)):
    for col in range(len(heatmap_values[row])):
        plt.text(col, row, f"{heatmap_values[row][col]:.2f}", ha="center", va="center", fontsize=7)
plt.tight_layout()
plt.savefig(plot_dir / "main_t315_heatmap.png", dpi=300)
plt.close()


# F8 - time course of four conditions (dynamics and steady state)
time_files = [
    ("Normoxia", "main_o2_0_9_t315_0_il6_1_0.csv"),
    ("Hypoxia", "main_o2_0_1_t315_0_il6_1_0.csv"),
    ("Hypoxia + T315 0.6", "main_o2_0_1_t315_0_6_il6_1_0.csv"),
    ("Hypoxia + T315 1.2", "main_o2_0_1_t315_1_2_il6_1_0.csv"),
]
fig, axes = plt.subplots(2, 2, figsize=(9, 6))
axes = axes.flatten()
for plot_index, (column, title) in enumerate(
    [("S3_HIF", "HIF"), ("ILK_activity", "ILK activity"),
     ("NFkB_activity", "NF-kB"), ("Snail", "Snail")]
):
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
plt.savefig(plot_dir / "main_time_course.png", dpi=300)
plt.close()


print(f"Saved plots to {plot_dir}")
