"""
=============================================================
HR Analytics Project — Exploratory Data Analysis (EDA)
=============================================================
This script answers 8 key HR business questions using the
cleaned dataset. Each question produces a chart saved to
reports/figures/ for use in the README and Tableau prep.

Business Questions:
  Q1.  What does our workforce look like? (headcount snapshot)
  Q2.  What is our attrition rate by department?
  Q3.  What are the top reasons employees leave?
  Q4.  How does tenure differ across grade levels?
  Q5.  Which recruitment source is fastest & most used?
  Q6.  Does training investment correlate with performance?
  Q7.  How does salary vary by country and grade?
  Q8.  What is our grade & gender distribution by department?

Author:  [Your Name]
=============================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import os
import warnings
warnings.filterwarnings("ignore")

# ── Paths ─────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH  = os.path.join(BASE_DIR, "data", "cleaned", "hr_data_cleaned.csv")
FIG_DIR    = os.path.join(BASE_DIR, "reports", "figures")
os.makedirs(FIG_DIR, exist_ok=True)

# ── Global chart style ────────────────────────────────────────
# A clean, professional look suitable for a portfolio project
BRAND_COLORS = {
    "primary":    "#2C3E7A",   # Deep navy
    "secondary":  "#3AAFB9",   # Teal
    "accent":     "#F4A261",   # Warm amber
    "danger":     "#E63946",   # Red (attrition)
    "success":    "#2A9D8F",   # Green (active)
    "light_grey": "#F0F2F5",
    "mid_grey":   "#ADB5BD",
}

PALETTE_DEPT = ["#2C3E7A","#3AAFB9","#F4A261","#E63946","#2A9D8F","#E9C46A","#A8DADC"]

sns.set_theme(style="whitegrid", font="DejaVu Sans")
plt.rcParams.update({
    "figure.facecolor":  "white",
    "axes.facecolor":    "white",
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.titlesize":    14,
    "axes.titleweight":  "bold",
    "axes.labelsize":    11,
    "xtick.labelsize":   10,
    "ytick.labelsize":   10,
    "legend.fontsize":   10,
    "figure.titlesize":  16,
    "figure.titleweight":"bold",
})

def save_fig(name: str):
    path = os.path.join(FIG_DIR, name)
    plt.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"   💾 Saved → reports/figures/{name}")


# =============================================================
# LOAD DATA
# =============================================================

print("=" * 60)
print("Loading cleaned dataset...")
print("=" * 60)

df = pd.read_csv(DATA_PATH)

# Quick sanity check
print(f"✅ Loaded: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"\n--- describe() for key numeric columns ---")
print(df[["Age","Tenure_Years","Annual_Salary_USD",
          "Performance_Rating","Training_Hours_Year"]].describe().round(1).to_string())


# =============================================================
# Q1 — WORKFORCE SNAPSHOT
# What does our overall workforce look like?
# =============================================================

print("\n" + "=" * 60)
print("Q1 — Workforce Snapshot")
print("=" * 60)

total        = len(df)
active       = (df["Employment_Status"] == "Active").sum()
attrition_n  = (df["Attrition_Flag"] == 1).sum()
attrition_rt = round(attrition_n / total * 100, 1)
avg_age      = round(df["Age"].mean(), 1)
avg_tenure   = round(df["Tenure_Years"].mean(), 1)
avg_sal_usd  = round(df["Annual_Salary_USD"].mean())

print(f"  Total headcount  : {total}")
print(f"  Active employees : {active}")
print(f"  Attrition rate   : {attrition_rt}%")
print(f"  Avg age          : {avg_age} years")
print(f"  Avg tenure       : {avg_tenure} years")
print(f"  Avg annual salary: USD {avg_sal_usd:,}")

# Chart: Headcount by Country (horizontal bar)
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("Q1 — Workforce Snapshot", y=1.02)

# Left: headcount by country
country_hc = df.groupby("Country").size().sort_values(ascending=True)
bars = axes[0].barh(country_hc.index, country_hc.values,
                    color=BRAND_COLORS["primary"], edgecolor="white", height=0.6)
axes[0].set_title("Headcount by Country")
axes[0].set_xlabel("Number of Employees")
for bar, val in zip(bars, country_hc.values):
    axes[0].text(val + 1, bar.get_y() + bar.get_height()/2,
                 str(val), va="center", fontsize=9)

# Right: headcount by department
dept_hc = df.groupby("Department").size().sort_values(ascending=False)
bars2 = axes[1].bar(dept_hc.index, dept_hc.values,
                    color=PALETTE_DEPT[:len(dept_hc)], edgecolor="white")
axes[1].set_title("Headcount by Department")
axes[1].set_ylabel("Number of Employees")
axes[1].tick_params(axis="x", rotation=30)
for bar, val in zip(bars2, dept_hc.values):
    axes[1].text(bar.get_x() + bar.get_width()/2, val + 1,
                 str(val), ha="center", fontsize=9)

plt.tight_layout()
save_fig("q1_workforce_snapshot.png")


# =============================================================
# Q2 — ATTRITION RATE BY DEPARTMENT
# Where are we losing the most people?
# =============================================================

print("\n" + "=" * 60)
print("Q2 — Attrition Rate by Department")
print("=" * 60)

dept_attr = (df.groupby("Department")
               .agg(Total=("Employee_ID","count"),
                    Left=("Attrition_Flag","sum"))
               .assign(Attrition_Rate=lambda x: (x["Left"]/x["Total"]*100).round(1))
               .sort_values("Attrition_Rate", ascending=False))

print(dept_attr.to_string())

fig, ax = plt.subplots(figsize=(10, 5))
colors = [BRAND_COLORS["danger"] if r > attrition_rt else BRAND_COLORS["secondary"]
          for r in dept_attr["Attrition_Rate"]]
bars = ax.bar(dept_attr.index, dept_attr["Attrition_Rate"],
              color=colors, edgecolor="white", width=0.6)
ax.axhline(attrition_rt, color=BRAND_COLORS["accent"],
           linestyle="--", linewidth=1.5, label=f"Company avg: {attrition_rt}%")
ax.set_title("Q2 — Attrition Rate by Department\n(red = above company average)")
ax.set_ylabel("Attrition Rate (%)")
ax.set_xlabel("Department")
ax.legend()
for bar, val in zip(bars, dept_attr["Attrition_Rate"]):
    ax.text(bar.get_x() + bar.get_width()/2, val + 0.3,
            f"{val}%", ha="center", fontsize=10, fontweight="bold")
plt.tight_layout()
save_fig("q2_attrition_by_department.png")


# =============================================================
# Q3 — WHY ARE EMPLOYEES LEAVING?
# Top termination reasons (voluntary vs involuntary)
# =============================================================

print("\n" + "=" * 60)
print("Q3 — Termination Reasons")
print("=" * 60)

leavers = df[df["Employment_Status"].isin(["Resigned","Terminated"])].copy()
reason_counts = leavers.groupby(["Termination_Category","Termination_Reason"]).size().reset_index(name="Count")
reason_counts = reason_counts.sort_values("Count", ascending=True)
print(reason_counts.to_string(index=False))

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Q3 — Why Are Employees Leaving?")

# Left: stacked reasons
vol   = reason_counts[reason_counts["Termination_Category"]=="Voluntary"]
invol = reason_counts[reason_counts["Termination_Category"]=="Involuntary"]

axes[0].barh(vol["Termination_Reason"],   vol["Count"],
             color=BRAND_COLORS["accent"], label="Voluntary",   height=0.5)
axes[0].barh(invol["Termination_Reason"], invol["Count"],
             color=BRAND_COLORS["danger"], label="Involuntary", height=0.5)
axes[0].set_title("Termination Reasons")
axes[0].set_xlabel("Number of Employees")
axes[0].legend()

# Right: Voluntary vs Involuntary pie
cat_counts = leavers["Termination_Category"].value_counts()
axes[1].pie(cat_counts.values,
            labels=cat_counts.index,
            colors=[BRAND_COLORS["accent"], BRAND_COLORS["danger"]],
            autopct="%1.0f%%", startangle=90,
            wedgeprops={"edgecolor":"white","linewidth":2})
axes[1].set_title("Voluntary vs Involuntary Split")

plt.tight_layout()
save_fig("q3_termination_reasons.png")


# =============================================================
# Q4 — TENURE BY GRADE LEVEL
# Do senior employees stay longer?
# =============================================================

print("\n" + "=" * 60)
print("Q4 — Tenure by Grade Level")
print("=" * 60)

tenure_grade = df.groupby("Grade_Level")["Tenure_Years"].agg(["mean","median","count"]).round(1)
print(tenure_grade.to_string())

fig, ax = plt.subplots(figsize=(10, 5))
grade_order = ["G1","G2","G3","G4","G5","G6"]
grade_colors = sns.color_palette("Blues_d", 6)

bp = ax.boxplot([df[df["Grade_Level"]==g]["Tenure_Years"].dropna().values
                 for g in grade_order],
                labels=grade_order, patch_artist=True,
                medianprops={"color":"white","linewidth":2.5})

for patch, color in zip(bp["boxes"], grade_colors):
    patch.set_facecolor(color)

# Overlay mean dots
means = [df[df["Grade_Level"]==g]["Tenure_Years"].mean() for g in grade_order]
ax.plot(range(1, 7), means, "D", color=BRAND_COLORS["accent"],
        markersize=8, zorder=5, label="Mean tenure")
ax.set_title("Q4 — Tenure Distribution by Grade Level\n(diamond = mean)")
ax.set_xlabel("Grade Level")
ax.set_ylabel("Tenure (Years)")
ax.legend()
plt.tight_layout()
save_fig("q4_tenure_by_grade.png")


# =============================================================
# Q5 — RECRUITMENT SOURCES
# Which source is fastest and most popular?
# =============================================================

print("\n" + "=" * 60)
print("Q5 — Recruitment Source Analysis")
print("=" * 60)

rec = (df.groupby("Recruitment_Source")
         .agg(Count=("Employee_ID","count"),
              Avg_Days=("Time_to_Hire_Days","mean"))
         .assign(Avg_Days=lambda x: x["Avg_Days"].round(1))
         .sort_values("Count", ascending=False))
print(rec.to_string())

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Q5 — Recruitment Source Analysis")

# Left: volume
colors5 = sns.color_palette("Set2", len(rec))
bars = axes[0].bar(rec.index, rec["Count"], color=colors5, edgecolor="white")
axes[0].set_title("Hires by Recruitment Source")
axes[0].set_ylabel("Number of Hires")
axes[0].tick_params(axis="x", rotation=20)
for bar, val in zip(bars, rec["Count"]):
    axes[0].text(bar.get_x()+bar.get_width()/2, val+1,
                 str(val), ha="center", fontsize=9)

# Right: avg time to hire
rec_sorted = rec.sort_values("Avg_Days")
bar_colors = [BRAND_COLORS["success"] if d == rec_sorted["Avg_Days"].min()
              else BRAND_COLORS["primary"] for d in rec_sorted["Avg_Days"]]
bars2 = axes[1].barh(rec_sorted.index, rec_sorted["Avg_Days"],
                     color=bar_colors, edgecolor="white", height=0.5)
axes[1].set_title("Avg Time-to-Hire by Source\n(green = fastest)")
axes[1].set_xlabel("Average Days to Hire")
for bar, val in zip(bars2, rec_sorted["Avg_Days"]):
    axes[1].text(val+0.3, bar.get_y()+bar.get_height()/2,
                 f"{val}d", va="center", fontsize=9)
plt.tight_layout()
save_fig("q5_recruitment_sources.png")


# =============================================================
# Q6 — TRAINING vs PERFORMANCE
# Does more training lead to higher performance ratings?
# =============================================================

print("\n" + "=" * 60)
print("Q6 — Training Hours vs Performance Rating")
print("=" * 60)

train_perf = (df.groupby("Performance_Rating")["Training_Hours_Year"]
                .agg(["mean","median","count"])
                .round(1))
print(train_perf.to_string())

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Q6 — Does Training Investment Drive Performance?")

# Left: avg training hours per performance band
rating_labels = {1:"1 - Poor", 2:"2 - Below Avg",
                 3:"3 - Meets", 4:"4 - Exceeds", 5:"5 - Outstanding"}
tp = df.dropna(subset=["Performance_Rating","Training_Hours_Year"]).copy()
tp["Rating_Label"] = tp["Performance_Rating"].map(rating_labels)
avg_train = (tp.groupby("Performance_Rating")["Training_Hours_Year"]
               .mean().round(1).reset_index())

bar_colors = sns.color_palette("YlGn", 5)
bars = axes[0].bar(avg_train["Performance_Rating"].map(rating_labels),
                   avg_train["Training_Hours_Year"],
                   color=bar_colors, edgecolor="white")
axes[0].set_title("Avg Training Hours by Performance Rating")
axes[0].set_ylabel("Avg Training Hours / Year")
axes[0].tick_params(axis="x", rotation=15)
for bar, val in zip(bars, avg_train["Training_Hours_Year"]):
    axes[0].text(bar.get_x()+bar.get_width()/2, val+0.5,
                 f"{val}h", ha="center", fontsize=9)

# Right: scatter plot
sample = tp.sample(min(400, len(tp)), random_state=42)
scatter_colors = [bar_colors[int(r)-1] for r in sample["Performance_Rating"]]
axes[1].scatter(sample["Training_Hours_Year"], sample["Performance_Rating"],
                c=scatter_colors, alpha=0.5, edgecolors="white", s=40)
# Trend line
z = np.polyfit(sample["Training_Hours_Year"], sample["Performance_Rating"], 1)
p = np.poly1d(z)
x_line = np.linspace(sample["Training_Hours_Year"].min(),
                     sample["Training_Hours_Year"].max(), 100)
axes[1].plot(x_line, p(x_line), color=BRAND_COLORS["danger"],
             linewidth=2, linestyle="--", label="Trend")
axes[1].set_title("Training Hours vs Performance (scatter)")
axes[1].set_xlabel("Training Hours / Year")
axes[1].set_ylabel("Performance Rating")
axes[1].legend()
plt.tight_layout()
save_fig("q6_training_vs_performance.png")


# =============================================================
# Q7 — SALARY DISTRIBUTION BY COUNTRY & GRADE
# How does compensation vary across markets?
# =============================================================

print("\n" + "=" * 60)
print("Q7 — Salary by Country and Grade")
print("=" * 60)

sal_country = (df.groupby("Country")["Annual_Salary_USD"]
                 .agg(["mean","median"])
                 .round(0)
                 .sort_values("mean", ascending=True))
print(sal_country.to_string())

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("Q7 — Annual Salary (USD) Distribution")

# Left: avg salary by country
bars = axes[0].barh(sal_country.index, sal_country["mean"]/1000,
                    color=BRAND_COLORS["primary"], edgecolor="white", height=0.6)
axes[0].set_title("Avg Annual Salary by Country (USD '000)")
axes[0].set_xlabel("Avg Annual Salary (USD '000)")
for bar, val in zip(bars, sal_country["mean"]/1000):
    axes[0].text(val+0.2, bar.get_y()+bar.get_height()/2,
                 f"${val:.0f}k", va="center", fontsize=8)

# Right: salary box by grade
grade_order = ["G1","G2","G3","G4","G5","G6"]
grade_data  = [df[df["Grade_Level"]==g]["Annual_Salary_USD"].dropna()/1000
               for g in grade_order]
bp = axes[1].boxplot(grade_data, labels=grade_order, patch_artist=True,
                     medianprops={"color":"white","linewidth":2})
grade_blues = sns.color_palette("Blues_d", 6)
for patch, color in zip(bp["boxes"], grade_blues):
    patch.set_facecolor(color)
axes[1].set_title("Salary Distribution by Grade Level (USD '000)")
axes[1].set_xlabel("Grade Level")
axes[1].set_ylabel("Annual Salary (USD '000)")
plt.tight_layout()
save_fig("q7_salary_distribution.png")


# =============================================================
# Q8 — GRADE & GENDER DISTRIBUTION BY DEPARTMENT
# Is our workforce balanced at senior levels?
# =============================================================

print("\n" + "=" * 60)
print("Q8 — Grade & Gender Distribution by Department")
print("=" * 60)

# Gender split by department
gender_dept = (df.groupby(["Department","Gender"])
                 .size()
                 .unstack(fill_value=0))
print("\nGender by Department:")
print(gender_dept.to_string())

# Senior ratio (G5+G6) by department
senior = (df[df["Grade_Level"].isin(["G5","G6"])]
            .groupby("Department").size()
            .div(df.groupby("Department").size())
            .mul(100).round(1)
            .sort_values(ascending=False))
print("\nSenior (G5/G6) ratio by Department:")
print(senior.to_string())

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Q8 — Workforce Composition by Department")

# Left: stacked gender bar
gender_pct = gender_dept.div(gender_dept.sum(axis=1), axis=0) * 100
gender_colors = [BRAND_COLORS["primary"], BRAND_COLORS["secondary"],
                 BRAND_COLORS["accent"]]
bottom = np.zeros(len(gender_pct))
for i, gender in enumerate(gender_pct.columns):
    axes[0].bar(gender_pct.index, gender_pct[gender],
                bottom=bottom, label=gender,
                color=gender_colors[i % len(gender_colors)],
                edgecolor="white")
    bottom += gender_pct[gender].values
axes[0].set_title("Gender Mix by Department (%)")
axes[0].set_ylabel("Percentage (%)")
axes[0].tick_params(axis="x", rotation=30)
axes[0].legend(loc="upper right")

# Right: senior ratio
colors_s = [BRAND_COLORS["danger"] if v > senior.mean()
            else BRAND_COLORS["secondary"] for v in senior.values]
bars = axes[1].bar(senior.index, senior.values,
                   color=colors_s, edgecolor="white")
axes[1].axhline(senior.mean(), color=BRAND_COLORS["accent"],
                linestyle="--", linewidth=1.5,
                label=f"Avg: {senior.mean():.1f}%")
axes[1].set_title("Senior Staff Ratio (G5/G6) by Department\n(red = above average)")
axes[1].set_ylabel("Senior Staff (%)")
axes[1].tick_params(axis="x", rotation=30)
axes[1].legend()
for bar, val in zip(bars, senior.values):
    axes[1].text(bar.get_x()+bar.get_width()/2, val+0.2,
                 f"{val}%", ha="center", fontsize=9)
plt.tight_layout()
save_fig("q8_grade_gender_distribution.png")


# =============================================================
# SUMMARY TABLE — all insights in one place
# =============================================================

print("\n" + "=" * 60)
print("EDA COMPLETE — Key Insights Summary")
print("=" * 60)

print(f"""
┌─────────────────────────────────────────────────────┐
│           HR ANALYTICS — KEY FINDINGS               │
├─────────────────────────────────────────────────────┤
│ Total headcount          : {total}                      │
│ Active employees         : {active} ({active/total*100:.0f}%)               │
│ Overall attrition rate   : {attrition_rt}%                    │
│ Average age              : {avg_age} years                  │
│ Average tenure           : {avg_tenure} years                   │
│ Average annual salary    : USD {avg_sal_usd:,}            │
├─────────────────────────────────────────────────────┤
│ Highest attrition dept   : {dept_attr.index[0]} ({dept_attr['Attrition_Rate'].iloc[0]}%)         │
│ Most common exit reason  : {leavers['Termination_Reason'].value_counts().index[0]}          │
│ Fastest hire source      : {rec.sort_values('Avg_Days')['Avg_Days'].index[0]} ({rec.sort_values('Avg_Days')['Avg_Days'].iloc[0]:.0f} days) │
│ Highest salary country   : {sal_country['mean'].idxmax()} (USD {sal_country['mean'].max()/1000:.0f}k/yr)  │
└─────────────────────────────────────────────────────┘
""")
print("📊 8 charts saved to reports/figures/")
print("✅ EDA complete — ready for Tableau!\n")
