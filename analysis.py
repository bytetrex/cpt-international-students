# ------------------------------------------------------------
# CPT Rules and International Students — analysis
#
# What this file does:
#   1. Reads the numbers from the data/ folder
#   2. Works out a few percent changes
#   3. Saves 3 charts into the charts/ folder
#
# How to run it:   python analysis.py
# ------------------------------------------------------------

import pandas as pd               # pandas = reads spreadsheets (CSV files) into tables
import matplotlib.pyplot as plt   # matplotlib = draws charts

# ---------- Step 1: read the data ----------
enrollment = pd.read_csv("data/enrollment.csv")
training = pd.read_csv("data/work_training.csv")

print("Enrollment data:")
print(enrollment)
print()

# ---------- Step 2: work out some numbers ----------
# Percent change formula:  (new - old) / old * 100
peak_new = enrollment["new_students"].max()        # biggest year of new students
latest_new = enrollment["new_students"].iloc[-1]   # last row (2025-26)
drop_from_peak = (latest_new - peak_new) / peak_new * 100

last_year_new = enrollment["new_students"].iloc[-2]  # second-to-last row (2024-25)
one_year_change = (latest_new - last_year_new) / last_year_new * 100

print(f"New students, peak year:   {peak_new:,}")
print(f"New students, 2025-26:     {latest_new:,}")
print(f"Change in one year:        {one_year_change:.1f}%")
print(f"Change from the peak:      {drop_from_peak:.1f}%")
print()

# Rough estimate for fall 2026: IIE's snapshot survey said new students fell about 15%
fall_2026_estimate = latest_new * (1 - 0.15)
print(f"Rough fall 2026 estimate:  {fall_2026_estimate:,.0f}  (not an official number)")
print()

# Colors I use in every chart
BLUE = "#2f5d9e"
GRAY = "#9aa5b1"
RED = "#c0392b"

# ---------- Chart 1: new international students each year ----------
fig, ax = plt.subplots(figsize=(9, 5))

years = enrollment["year"]
new_thousands = enrollment["new_students"] / 1000   # show in thousands so the axis is easier to read

# dashed line from 2025-26 to the fall 2026 estimate (drawn first, so the blue line sits on top)
ax.plot(["2025-26", "Fall 2026\n(estimate)"],
        [latest_new / 1000, fall_2026_estimate / 1000],
        linestyle="--", marker="o", color=RED, linewidth=2, label="Fall 2026 estimate (survey: -15%)")

ax.plot(years, new_thousands, marker="o", color=BLUE, linewidth=2.5, label="New students (official)")

# notes on the chart
ax.annotate("COVID", xy=("2020-21", 145.5), xytext=("2020-21", 175),
            ha="center", color=GRAY, arrowprops=dict(arrowstyle="->", color=GRAY))
ax.annotate("CPT limits\n(Aug 2026)", xy=("Fall 2026\n(estimate)", fall_2026_estimate / 1000),
            xytext=("Fall 2026\n(estimate)", 255), ha="center", color=RED,
            arrowprops=dict(arrowstyle="->", color=RED))

ax.set_title(f"New international students fell {abs(one_year_change):.1f}% in 2025-26", fontsize=14, loc="left")
ax.set_ylabel("New students (thousands)")
ax.set_ylim(0, 330)
ax.spines[["top", "right"]].set_visible(False)   # remove the box lines on top and right
ax.legend(frameon=False, loc="lower left")
fig.text(0.01, 0.01, "Source: IIE Open Doors 2023-2026; Fall 2026 Snapshot. Estimate is mine.", fontsize=8, color=GRAY)
fig.tight_layout()
fig.savefig("charts/1_new_students.png", dpi=150)
print("Saved charts/1_new_students.png")

# ---------- Chart 2: total international students each year ----------
fig, ax = plt.subplots(figsize=(9, 5))
total_millions = enrollment["total_students"] / 1_000_000

ax.bar(years, total_millions, color=GRAY)
ax.bar(years.iloc[-1], total_millions.iloc[-1], color=BLUE)   # color the latest year blue

# write the number on top of each bar
for x, y in zip(years, total_millions):
    ax.text(x, y + 0.02, f"{y:.2f}M", ha="center", fontsize=9)

ax.set_title("Total international students (incl. OPT) dropped for the first time since COVID", fontsize=13, loc="left")
ax.set_ylabel("Students (millions)")
ax.set_ylim(0, 1.35)
ax.spines[["top", "right"]].set_visible(False)
fig.text(0.01, 0.01, "Source: IIE Open Doors; NAFSA", fontsize=8, color=GRAY)
fig.tight_layout()
fig.savefig("charts/2_total_students.png", dpi=150)
print("Saved charts/2_total_students.png")

# ---------- Chart 3: how students got work experience in 2024 ----------
row_2024 = training[training["year"] == 2024].iloc[0]
labels = ["OPT\n(after graduating)", "CPT\n(during school)", "STEM OPT\n(extension)"]
values = [row_2024["opt_working"], row_2024["cpt"], row_2024["stem_opt"]]
colors = [GRAY, RED, GRAY]

fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(labels, [v / 1000 for v in values], color=colors)
for i, v in enumerate(values):
    ax.text(i, v / 1000 + 3, f"{v:,.0f}", ha="center", fontsize=11)

ax.set_title("In 2024, 130,586 students were approved for CPT —\nthe program the 2026 rules now limit", fontsize=13, loc="left")
ax.set_ylabel("Students (thousands)")
ax.set_ylim(0, 230)
ax.spines[["top", "right"]].set_visible(False)
fig.text(0.01, 0.01, "Source: ICE, SEVIS by the Numbers 2024", fontsize=8, color=GRAY)
fig.tight_layout()
fig.savefig("charts/3_work_training_2024.png", dpi=150)
print("Saved charts/3_work_training_2024.png")

print("\nDone!")
