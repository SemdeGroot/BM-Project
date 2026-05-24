import csv
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Patch


data_dir = Path("snoopy-output/hsu_extended")
plot_dir = Path("analysis/results/output/hsu_extended")
plot_dir.mkdir(parents=True, exist_ok=True)

conditions = [
    ("Hypoxia", "hsu_o2_0_1_t315_0_il6_1_0.csv"),
    ("Normoxia", "hsu_o2_0_9_t315_0_il6_1_0.csv"),
    ("T315 0.2", "hsu_o2_0_1_t315_0_2_il6_1_0.csv"),
    ("T315 0.6", "hsu_o2_0_1_t315_0_6_il6_1_0.csv"),
    ("T315 1.2", "hsu_o2_0_1_t315_1_2_il6_1_0.csv"),
    ("Low IL6", "hsu_o2_0_1_t315_0_il6_0_1.csv"),
]

all_rows = {}
for name, file_name in conditions:
    file_path = data_dir / file_name

    with file_path.open() as file:
        all_rows[name] = list(csv.DictReader(file))

names = []
hif_values = []
ilk_activity_values = []
pakt_values = []
pmtor_values = []
il6_values = []
pstat3_values = []
e2f1_values = []
nfkb_values = []
yb1_values = []
foxo3a_values = []
snail_values = []
zeb1_values = []
ecadherin_values = []
vimentin_values = []

for name, _ in conditions:
    last_row = all_rows[name][-1]
    names.append(name)
    hif_values.append(float(last_row["S3_HIF"]))
    ilk_activity_values.append(float(last_row["ILK_activity"]))
    pakt_values.append(float(last_row["p_473S_Akt"]))
    pmtor_values.append(float(last_row["p_mTOR"]))
    il6_values.append(float(last_row["IL6"]))
    pstat3_values.append(float(last_row["p_Stat3"]))
    e2f1_values.append(float(last_row["E2F1"]))
    nfkb_values.append(float(last_row["NFkB_activity"]))
    yb1_values.append(float(last_row["YB_1"]))
    foxo3a_values.append(float(last_row["Foxo3a"]))
    snail_values.append(float(last_row["Snail"]))
    zeb1_values.append(float(last_row["Zeb1"]))
    ecadherin_values.append(float(last_row["E_cadherin"]))
    vimentin_values.append(float(last_row["vimentin"]))

print("Hsu extended final values at time 10000")
print("Condition\tHIF\tILK_activity\tpAkt\tp_mTOR\tIL6\tpStat3\tE2F1\tNFkB\tYB_1\tFoxo3a\tSnail\tZeb1\tE_cadherin\tvimentin")
for i in range(len(names)):
    print(
        f"{names[i]}\t"
        f"{hif_values[i]:.3f}\t"
        f"{ilk_activity_values[i]:.3f}\t"
        f"{pakt_values[i]:.3f}\t"
        f"{pmtor_values[i]:.3f}\t"
        f"{il6_values[i]:.3f}\t"
        f"{pstat3_values[i]:.3f}\t"
        f"{e2f1_values[i]:.3f}\t"
        f"{nfkb_values[i]:.3f}\t"
        f"{yb1_values[i]:.3f}\t"
        f"{foxo3a_values[i]:.3f}\t"
        f"{snail_values[i]:.3f}\t"
        f"{zeb1_values[i]:.3f}\t"
        f"{ecadherin_values[i]:.3f}\t"
        f"{vimentin_values[i]:.3f}"
    )

doses = [0, 0.2, 0.6, 1.2]
dose_labels = ["0", "0.2", "0.6", "1.2"]

dose_hif = [hif_values[0], hif_values[2], hif_values[3], hif_values[4]]
dose_ilk_activity = [ilk_activity_values[0], ilk_activity_values[2], ilk_activity_values[3], ilk_activity_values[4]]
dose_pakt = [pakt_values[0], pakt_values[2], pakt_values[3], pakt_values[4]]
dose_pmtor = [pmtor_values[0], pmtor_values[2], pmtor_values[3], pmtor_values[4]]
dose_nfkb = [nfkb_values[0], nfkb_values[2], nfkb_values[3], nfkb_values[4]]
dose_il6 = [il6_values[0], il6_values[2], il6_values[3], il6_values[4]]
dose_yb1 = [yb1_values[0], yb1_values[2], yb1_values[3], yb1_values[4]]
dose_foxo3a = [foxo3a_values[0], foxo3a_values[2], foxo3a_values[3], foxo3a_values[4]]
dose_snail = [snail_values[0], snail_values[2], snail_values[3], snail_values[4]]
dose_zeb1 = [zeb1_values[0], zeb1_values[2], zeb1_values[3], zeb1_values[4]]
dose_ecadherin = [ecadherin_values[0], ecadherin_values[2], ecadherin_values[3], ecadherin_values[4]]
dose_vimentin = [vimentin_values[0], vimentin_values[2], vimentin_values[3], vimentin_values[4]]

plt.figure(figsize=(7, 4))
plt.plot(doses, [value / dose_hif[0] for value in dose_hif], marker="o", label="HIF")
plt.plot(doses, [value / dose_ilk_activity[0] for value in dose_ilk_activity], marker="o", label="ILK signaling")
plt.plot(doses, [value / dose_nfkb[0] for value in dose_nfkb], marker="o", linestyle="--", label="Hsu loop")
plt.axvline(0.6, color="tab:gray", linestyle="--", linewidth=1)
plt.axhline(0.5, color="tab:gray", linestyle=":", linewidth=1)
plt.xlabel("T315 marking under hypoxia")
plt.ylabel("Final value relative to T315 0")
plt.title("T315 lowers ILK signaling and the Hsu loop")
plt.xticks(doses, dose_labels)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig(plot_dir / "report_t315_signaling_response.png", dpi=300)
plt.close()

heatmap_labels = [
    "HIF",
    "ILK activity",
    "p-Akt",
    "p-mTOR",
    "NF-kappaB",
    "IL6",
    "YB-1",
    "Foxo3a",
    "Snail",
    "Zeb1",
    "E-cadherin",
    "vimentin",
]
heatmap_values = [
    [value / dose_hif[0] for value in dose_hif],
    [value / dose_ilk_activity[0] for value in dose_ilk_activity],
    [value / dose_pakt[0] for value in dose_pakt],
    [value / dose_pmtor[0] for value in dose_pmtor],
    [value / dose_nfkb[0] for value in dose_nfkb],
    [value / dose_il6[0] for value in dose_il6],
    [value / dose_yb1[0] for value in dose_yb1],
    [value / dose_foxo3a[0] for value in dose_foxo3a],
    [value / dose_snail[0] for value in dose_snail],
    [value / dose_zeb1[0] for value in dose_zeb1],
    [value / dose_ecadherin[0] for value in dose_ecadherin],
    [value / dose_vimentin[0] for value in dose_vimentin],
]

plt.figure(figsize=(7, 5))
plt.imshow(heatmap_values, aspect="auto", cmap="RdYlBu_r", vmin=0.4, vmax=2.0)
plt.colorbar(label="Final value relative to T315 0")
plt.xticks(range(len(dose_labels)), dose_labels)
plt.yticks(range(len(heatmap_labels)), heatmap_labels)
plt.xlabel("T315 marking under hypoxia")
plt.title("Full model T315 response")

for row in range(len(heatmap_values)):
    for col in range(len(heatmap_values[row])):
        plt.text(col, row, f"{heatmap_values[row][col]:.2f}", ha="center", va="center", fontsize=7)

plt.tight_layout()
plt.savefig(plot_dir / "report_t315_full_model_heatmap.png", dpi=300)
plt.close()

plt.figure(figsize=(7, 4))
plt.plot(doses, [value / dose_yb1[0] for value in dose_yb1], marker="o", label="YB-1")
plt.plot(doses, [value / dose_snail[0] for value in dose_snail], marker="o", label="Snail")
plt.plot(doses, [value / dose_zeb1[0] for value in dose_zeb1], marker="o", label="Zeb1")
plt.plot(doses, [value / dose_vimentin[0] for value in dose_vimentin], marker="o", label="vimentin")
plt.plot(doses, [value / dose_foxo3a[0] for value in dose_foxo3a], marker="o", linestyle="--", label="Foxo3a")
plt.plot(doses, [value / dose_ecadherin[0] for value in dose_ecadherin], marker="o", linestyle="--", label="E-cadherin")
plt.xlabel("T315 marking under hypoxia")
plt.ylabel("Final value relative to T315 0")
plt.title("T315 shifts the EMT outputs")
plt.xticks(doses, dose_labels)
plt.grid(True, alpha=0.3)
plt.legend(ncol=2)
plt.tight_layout()
plt.savefig(plot_dir / "report_t315_emt_response.png", dpi=300)
plt.close()

comparison_labels = [
    "HIF",
    "ILK activity",
    "p-Akt",
    "p-mTOR",
    "IL6",
    "NF-kappaB",
    "YB-1",
    "Snail",
    "E-cadherin",
    "vimentin",
]
hypoxia_values = [
    hif_values[0],
    ilk_activity_values[0],
    pakt_values[0],
    pmtor_values[0],
    il6_values[0],
    nfkb_values[0],
    yb1_values[0],
    snail_values[0],
    ecadherin_values[0],
    vimentin_values[0],
]
normoxia_values = [
    hif_values[1],
    ilk_activity_values[1],
    pakt_values[1],
    pmtor_values[1],
    il6_values[1],
    nfkb_values[1],
    yb1_values[1],
    snail_values[1],
    ecadherin_values[1],
    vimentin_values[1],
]
normoxia_relative = []
bar_colors = []
for i in range(len(comparison_labels)):
    value = normoxia_values[i] / hypoxia_values[i]
    normoxia_relative.append(value)

    if value < 1:
        bar_colors.append("tab:blue")
    else:
        bar_colors.append("tab:orange")

plt.figure(figsize=(8, 4.5))
plt.barh(comparison_labels, normoxia_relative, color=bar_colors)
plt.axvline(1, color="tab:gray", linestyle="--")
plt.xlabel("Normoxia / hypoxia final value")
plt.title("Hypoxia mainly increases HIF and EMT markers")
plt.legend(
    handles=[
        Patch(color="tab:blue", label="Lower in normoxia"),
        Patch(color="tab:orange", label="Higher in normoxia"),
    ],
    loc="lower right",
)
plt.tight_layout()
plt.savefig(plot_dir / "report_normoxia_hypoxia_response.png", dpi=300)
plt.close()

time_rows = all_rows["Hypoxia"]
time_values = []
early_il6 = []
early_pstat3 = []
early_e2f1 = []
early_ilk_activity = []
early_pakt = []
early_nfkb = []

for row in time_rows:
    time = float(row["Time"])
    if time <= 300:
        time_values.append(time)
        early_il6.append(float(row["IL6"]))
        early_pstat3.append(float(row["p_Stat3"]))
        early_e2f1.append(float(row["E2F1"]))
        early_ilk_activity.append(float(row["ILK_activity"]))
        early_pakt.append(float(row["p_473S_Akt"]))
        early_nfkb.append(float(row["NFkB_activity"]))

fig, axes = plt.subplots(2, 1, figsize=(7, 5), sharex=True)

axes[0].plot(time_values, [value / max(early_il6) for value in early_il6], label="IL6")
axes[0].plot(time_values, [value / max(early_pstat3) for value in early_pstat3], label="p-Stat3")
axes[0].plot(time_values, [value / max(early_e2f1) for value in early_e2f1], label="E2F1")
axes[0].set_ylabel("Relative value")
axes[0].set_title("Early Hsu activation under hypoxia")
axes[0].grid(True, alpha=0.3)
axes[0].legend()

axes[1].plot(time_values, [value / max(early_ilk_activity) for value in early_ilk_activity], label="ILK activity")
axes[1].plot(time_values, [value / max(early_pakt) for value in early_pakt], label="p-Akt")
axes[1].plot(time_values, [value / max(early_nfkb) for value in early_nfkb], label="NF-kappaB")
axes[1].set_xlabel("Time")
axes[1].set_ylabel("Relative value")
axes[1].grid(True, alpha=0.3)
axes[1].legend()

plt.tight_layout()
plt.savefig(plot_dir / "report_hsu_early_activation.png", dpi=300)
plt.close()

low_il6_labels = ["IL6", "NF-kappaB", "HIF", "Snail"]
low_initial = [
    il6_values[5] / il6_values[0],
    nfkb_values[5] / nfkb_values[0],
    hif_values[5] / hif_values[0],
    snail_values[5] / snail_values[0],
]

plt.figure(figsize=(6.5, 3.5))
plt.bar(low_il6_labels, low_initial, color="tab:purple")
plt.axhline(1, color="tab:gray", linestyle="--")
plt.ylabel("Low initial IL6 / high initial IL6")
plt.title("Initial IL6 does not change the long-term state")
plt.tight_layout()
plt.savefig(plot_dir / "report_il6_initial_condition_check.png", dpi=300)
plt.close()

print("Suggested report figures:")
print("1. report_normoxia_hypoxia_response.png")
print("2. report_t315_signaling_response.png")
print("3. report_t315_full_model_heatmap.png")
print("4. report_t315_emt_response.png")
print("5. report_il6_initial_condition_check.png")
print("Use report_hsu_early_activation.png only if you discuss the transient IL6 response.")
print(f"Saved plots to {plot_dir}")
