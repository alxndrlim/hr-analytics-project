# 🧑‍💼 HR Analytics: Workforce Intelligence Dashboard

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Cleaning-lightblue)
![Tableau](https://img.shields.io/badge/Tableau-Public-orange?logo=tableau)
![Excel](https://img.shields.io/badge/Excel-Data%20Review-green?logo=microsoft-excel)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

---

## 📊 Live Dashboard

🔗 **[View on Tableau Public → HR Analytics: Workforce Intelligence Dashboard](https://public.tableau.com/app/profile/alex.lim2876/viz/HRAnalytics-WorkforceIntelligenceDashboard/WorkforceOverviewDashboard)**

> 4 interactive tabs · 1,000 employees · APAC Tech Company (Synthetic Data)

---

## 📌 Project Overview

This is an end-to-end beginner Data Analytics portfolio project combining **Python (Pandas)**, **Excel**, and **Tableau Public** to analyse a synthetic HR dataset modelled on real-world HR operations across the APAC region.

The project covers the full data analytics workflow:
- Synthetic dataset generation with intentional data quality issues
- Data cleaning and preparation in Python and Excel
- Exploratory Data Analysis (EDA) with business insights
- Interactive dashboard published on Tableau Public

---

## 🎯 Business Objectives

The dashboard answers key HR questions that matter to senior leadership:

| # | Business Question | Dashboard Tab |
|---|------------------|---------------|
| 1 | What does our workforce look like across APAC? | Workforce Overview |
| 2 | Which departments have the highest attrition risk? | Attrition Analysis |
| 3 | Which recruitment sources are most effective? | Recruitment Analytics |
| 4 | Is training investment linked to performance? | L&D and Compensation |
| 5 | How does salary vary across countries and grades? | L&D and Compensation |

---

## 📂 Project Structure

```
hr-analytics-project/
│
├── data/
│   ├── raw/
│   │   └── hr_data_raw.csv          # Original synthetic dataset (messy)
│   └── cleaned/
│       └── hr_data_cleaned.csv      # Cleaned dataset used for Tableau
│
├── notebooks/
│   ├── 01_data_cleaning.ipynb       # Step-by-step data cleaning walkthrough
│   └── 02_eda.ipynb                 # Exploratory Data Analysis with charts
│
├── scripts/
│   ├── generate_dataset.py          # Generates the synthetic HR dataset
│   ├── clean_data.py                # Full data cleaning pipeline
│   └── eda_analysis.py              # EDA analysis and chart generation
│
├── reports/
│   └── figures/                     # EDA charts exported as PNG files
│       ├── q1_headcount_by_country.png
│       ├── q2_attrition_by_dept.png
│       ├── q3_exit_reasons.png
│       ├── q4_tenure_by_grade.png
│       ├── q5_recruitment_sources.png
│       ├── q6_training_vs_performance.png
│       ├── q7_salary_distribution.png
│       └── q8_diversity_senior_levels.png
│
└── README.md
```

---

## 🗃️ Dataset Description

> This project uses a **synthetic HR dataset** designed to reflect real-world HR metrics and patterns based on professional experience in HR management across the APAC region. All data is fictional and does not represent any real employees or organisation.

### Dataset Specifications

| Property | Detail |
|----------|--------|
| **Rows** | 1,000 employees |
| **Columns** | 41 features |
| **Region** | APAC (13 countries) |
| **Time Period** | 2015–2025 |
| **Generated using** | Python (Faker, NumPy, Pandas) |

### Key Columns

| Column | Description |
|--------|-------------|
| `Employee_ID` | Unique identifier |
| `Full_Name` | Employee full name |
| `Gender` | Male / Female / Non-binary |
| `Country` | One of 13 APAC countries |
| `Department` | One of 7 departments |
| `Grade_Level` | G1 (entry) to G6 (senior) |
| `Employment_Status` | Active / Resigned / Terminated |
| `Annual_Salary_USD` | Salary in USD |
| `Training_Hours_Year` | Annual training hours |
| `Performance_Rating` | 1–5 scale |
| `Time_to_Hire_Days` | Days from application to offer |
| `Tenure_Years` | Years at company (calculated) |
| `Attrition_Flag` | 1 = leaver, 0 = active (calculated) |

### Intentional Data Quality Issues (Raw Dataset)

The raw dataset was intentionally created with real-world data quality problems to practise cleaning:

- Mixed date formats (DD/MM/YYYY, MM-DD-YYYY, YYYY/MM/DD)
- Inconsistent text casing (MALE, male, Male)
- Salary stored as text with symbols ($75,000)
- Performance ratings stored as fractions (3/5)
- Missing values in termination-related fields
- Inconsistent department name spellings

---

## 🛠️ Tools & Technologies

| Tool | Purpose |
|------|---------|
| **Python 3.x** | Dataset generation, data cleaning, EDA |
| **Pandas** | Data manipulation and transformation |
| **Matplotlib / Seaborn** | EDA visualisations |
| **Faker** | Realistic synthetic data generation |
| **Excel** | Initial data review, spot checks |
| **Tableau Public** | Interactive dashboard |
| **Jupyter Notebook** | Documented analysis walkthrough |
| **GitHub** | Version control and project documentation |

---

## 🧹 Data Cleaning Process

### What Was Done in Excel
- Initial visual inspection of raw data
- Identifying inconsistency patterns (date formats, casing)
- Spot-checking row counts and column types
- Documenting data quality issues before Python cleaning

### What Was Done in Python (Pandas)

| Step | Action | Example |
|------|--------|---------|
| 1 | Standardise text columns | `"MALE"` → `"Male"` |
| 2 | Parse mixed date formats | `"01-13-2020"` → `2020-01-13` |
| 3 | Clean numeric fields | `"$75,000"` → `75000.0` |
| 4 | Standardise rating format | `"3/5"` → `3.0` |
| 5 | Handle missing values | Termination fields → `"Not Applicable"` |
| 6 | Create calculated columns | `Tenure_Years`, `Age`, `Attrition_Flag` |
| 7 | Validate and export | Save as `hr_data_cleaned.csv` |

**Why Python over Excel for cleaning?**
Python was chosen for the main cleaning pipeline because it is reproducible, scalable to larger datasets, and every transformation step is documented in code. Excel was used for initial visual inspection only.

---

## 🔍 Exploratory Data Analysis

Eight business questions were explored during EDA:

| Question | Key Finding |
|----------|-------------|
| Q1 — Workforce snapshot | 1,000 employees across 13 APAC countries; India largest office (120) |
| Q2 — Attrition by department | Delivery highest at 26.2%; IT lowest at 15.6% |
| Q3 — Exit reasons | Personal reasons top voluntary exit; Misconduct top involuntary |
| Q4 — Tenure at exit | Most leavers had 2–5 years tenure; Legal has longest-tenured leavers |
| Q5 — Recruitment sources | Referral highest volume (217); Internal Transfer fastest at 52 days |
| Q6 — Training vs performance | Positive correlation — higher training hours linked to higher ratings |
| Q7 — Salary distribution | Australia highest avg USD100K; Philippines lowest at USD17K |
| Q8 — Diversity | Gender broadly balanced; slight male skew at G5/G6 senior levels |

---

## 📊 Tableau Dashboard

🔗 **[View Live Dashboard](https://public.tableau.com/app/profile/alex.lim2876/viz/HRAnalytics-WorkforceIntelligenceDashboard/WorkforceOverviewDashboard)**

The dashboard consists of 4 interactive tabs:

### Tab 1 — Workforce Overview
- Total headcount, active employees, gender breakdown KPIs
- Average tenure and age KPIs
- Headcount by country (map)
- Grade level distribution (bar chart)
- Gender mix by country (stacked bar)

### Tab 2 — Attrition Analysis
- Overall attrition rate KPI (20.4%)
- Attrition rate by department with company average reference line
- Exit reasons by category (voluntary vs involuntary)
- Tenure at exit by department (box plot)

### Tab 3 — Recruitment Analytics
- Hires by recruitment source
- Average time-to-hire by source with overall average reference line
- Monthly hiring trend (2015–2025)

### Tab 4 — L&D and Compensation
- Average training hours by department
- Training hours vs performance rating (scatter plot with trend line)
- Annual salary by country
- Salary distribution by grade level (box plot)

---

## ▶️ How to Reproduce This Analysis

### Prerequisites
```bash
pip install pandas numpy faker matplotlib seaborn jupyter
```

### Steps

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/hr-analytics-project.git
cd hr-analytics-project
```

**2. Generate the raw dataset**
```bash
python scripts/generate_dataset.py
```
This creates `data/raw/hr_data_raw.csv` with 1,000 rows and intentional data quality issues.

**3. Run the data cleaning script**
```bash
python scripts/clean_data.py
```
This creates `data/cleaned/hr_data_cleaned.csv` with 41 columns.

**4. Run the EDA script**
```bash
python scripts/eda_analysis.py
```
This generates 8 charts saved to `reports/figures/`.

**5. Open the Jupyter notebooks** (optional — for detailed walkthrough)
```bash
jupyter notebook
```
Open `notebooks/01_data_cleaning.ipynb` then `notebooks/02_eda.ipynb`.

**6. View the Tableau dashboard**
Open `data/cleaned/hr_data_cleaned.csv` in Tableau Public to reproduce the dashboard, or view the published version at the link above.

---

## 💡 Key Insights Summary

1. **Delivery department needs urgent attention** — attrition at 26.2%, significantly above company average of 20.4%
2. **Internal transfers are the most efficient hiring channel** — fastest time-to-hire at 52 days vs LinkedIn at 57 days
3. **Training investment pays off** — positive correlation between training hours and performance ratings across all departments
4. **Significant salary variance across APAC** — Australia (USD100K) earns 6x more than Philippines (USD17K) at similar grade levels
5. **Workforce is growing** — hiring peaked in 2020, recent trend shows stabilisation

---

## 👤 Author

**Alex Lim**
- Tableau Public: [View Profile](https://public.tableau.com/app/profile/alex.lim2876)
- GitHub: https://github.com/alxndrlim/hr-analytics-project
- LinkedIn: https://www.linkedin.com/in/alxndrlim/

---

## 📄 Disclaimer

This project uses a synthetic dataset generated for portfolio and learning purposes. All employee names, salaries, and organisational data are entirely fictional and do not represent any real individuals or companies.
