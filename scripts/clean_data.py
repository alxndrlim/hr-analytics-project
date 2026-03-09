"""
=============================================================
HR Analytics Project — Data Cleaning Script
=============================================================
This script takes the raw (messy) HR dataset and produces a
clean, analysis-ready version.

What this script fixes:
  1.  Standardise text columns (casing, variants → single value)
  2.  Parse and standardise all date columns
  3.  Clean salary columns (remove $, commas → numeric)
  4.  Clean percentage columns (remove % sign → numeric)
  5.  Clean performance ratings ("3/5" → 3)
  6.  Clean Yes/No columns (Y/y/yes/YES → Yes)
  7.  Handle missing values (blanks, "N/A", "-" → NaN or "None")
  8.  Fix data types (dates, numbers, strings)
  9.  Create calculated columns (Age, Tenure_Years, Annual figures)
  10. Final validation report

Input:   data/raw/hr_data_raw.csv
Output:  data/cleaned/hr_data_cleaned.csv

Author:  [Your Name]
=============================================================
"""

import pandas as pd
import numpy as np
import os
import re
from datetime import datetime

# ── File paths ────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_PATH    = os.path.join(BASE_DIR, "data", "raw",     "hr_data_raw.csv")
CLEAN_PATH  = os.path.join(BASE_DIR, "data", "cleaned", "hr_data_cleaned.csv")

# ── Reference date for calculating Age and Tenure ────────────
TODAY = datetime(2025, 1, 1)   # Fixed date so results are reproducible


# =============================================================
# STEP 1 — LOAD THE RAW DATA
# =============================================================

def load_data(path: str) -> pd.DataFrame:
    """
    Load the raw CSV file into a Pandas DataFrame.
    A DataFrame is like a spreadsheet table inside Python.
    """
    print("=" * 60)
    print("STEP 1 — Loading raw data")
    print("=" * 60)

    df = pd.read_csv(path)

    print(f"✅ Loaded: {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"\nColumn names:\n{list(df.columns)}\n")

    # Show a snapshot of data types (useful to spot problems early)
    print("Data types (before cleaning):")
    print(df.dtypes.to_string())

    return df


# =============================================================
# STEP 2 — STANDARDISE TEXT COLUMNS
# Fix casing, abbreviations, and free-text variants
# =============================================================

def clean_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardise all the messy text columns.
    Pattern: strip whitespace → apply a mapping of known variants → Title Case
    """
    print("\n" + "=" * 60)
    print("STEP 2 — Standardising text columns")
    print("=" * 60)

    # ── Full Name: proper Title Case ──────────────────────────
    df["Full_Name"] = df["Full_Name"].str.strip().str.title()
    print("✅ Full_Name → Title Case applied")

    # ── Gender: map all variants to standard values ───────────
    gender_map = {
        "male": "Male", "m": "Male", "MALE": "Male", "M": "Male",
        "female": "Female", "f": "Female", "FEMALE": "Female", "F": "Female",
        "non-binary": "Non-binary", "non binary": "Non-binary",
        "NB": "Non-binary", "nb": "Non-binary", "Non Binary": "Non-binary",
    }
    before = df["Gender"].nunique()
    df["Gender"] = df["Gender"].str.strip().replace(gender_map)
    after = df["Gender"].nunique()
    print(f"✅ Gender → standardised ({before} variants → {after} clean values)")
    print(f"   Values: {sorted(df['Gender'].unique())}")

    # ── Department: map all variants to standard values ───────
    dept_map = {
        "hr": "HR", "h.r.": "HR", "human resources": "HR", "hr dept": "HR",
        "it": "IT", "i.t.": "IT", "information technology": "IT", "tech": "IT",
        "finance": "Finance", "FINANCE": "Finance", "fin": "Finance",
        "legal": "Legal", "LEGAL": "Legal", "lgl": "Legal",
        "marketing": "Marketing", "MARKETING": "Marketing", "mktg": "Marketing",
        "delivery": "Delivery", "DELIVERY": "Delivery", "del": "Delivery",
        "sales": "Sales", "SALES": "Sales", "sls": "Sales",
    }
    before = df["Department"].nunique()
    df["Department"] = df["Department"].str.strip().str.lower().replace(dept_map)
    # Catch any remaining — apply Title Case as fallback
    # Fix specific acronyms that title() breaks
    df["Department"] = df["Department"].str.strip().str.title()
    df["Department"] = df["Department"].replace({"Hr": "HR", "It": "IT"})
    after = df["Department"].nunique()
    print(f"✅ Department → standardised ({before} variants → {after} clean values)")
    print(f"   Values: {sorted(df['Department'].unique())}")

    # ── Employment Type: map all variants ─────────────────────
    emptype_map = {
        "full time": "Full-time", "ft": "Full-time", "fulltime": "Full-time",
        "full-time": "Full-time",
        "contractor": "Contractor", "contract": "Contractor", "ctr": "Contractor",
        "intern": "Intern", "internship": "Intern", "INTERN": "Intern",
        "expat": "Expat", "expatriate": "Expat", "EXPAT": "Expat",
    }
    before = df["Employment_Type"].nunique()
    df["Employment_Type"] = df["Employment_Type"].str.strip().str.lower().replace(emptype_map)
    df["Employment_Type"] = df["Employment_Type"].str.strip().str.title()
    after = df["Employment_Type"].nunique()
    print(f"✅ Employment_Type → standardised ({before} variants → {after} clean values)")

    # ── Work Mode: clean casing ───────────────────────────────
    workmode_map = {
        "wfh": "Remote", "work from home": "Remote", "remote": "Remote",
        "onsite": "Onsite", "on-site": "Onsite", "office": "Onsite",
        "hybrid": "Hybrid",
    }
    df["Work_Mode"] = df["Work_Mode"].str.strip().str.lower().replace(workmode_map)
    df["Work_Mode"] = df["Work_Mode"].str.strip().str.title()
    print("✅ Work_Mode → standardised")

    # ── Recruitment Source: map variants ──────────────────────
    source_map = {
        "linkedin": "LinkedIn", "linked in": "LinkedIn", "LINKEDIN": "LinkedIn",
        "referral": "Referral", "REFERRAL": "Referral", "ref": "Referral",
        "agency": "Agency", "AGENCY": "Agency", "recruitment agency": "Agency",
        "job board": "Job Board", "JOB BOARD": "Job Board",
        "jobboard": "Job Board", "job board": "Job Board",
        "internal transfer": "Internal Transfer", "internal": "Internal Transfer",
        "INTERNAL": "Internal Transfer", "int transfer": "Internal Transfer",
    }
    before = df["Recruitment_Source"].nunique()
    df["Recruitment_Source"] = (df["Recruitment_Source"]
                                  .str.strip()
                                  .str.lower()
                                  .replace(source_map))
    df["Recruitment_Source"] = df["Recruitment_Source"].str.strip().str.title()
    after = df["Recruitment_Source"].nunique()
    print(f"✅ Recruitment_Source → standardised ({before} variants → {after} clean values)")

    return df


# =============================================================
# STEP 3 — CLEAN DATE COLUMNS
# Parse mixed formats into a single standard YYYY-MM-DD format
# =============================================================

def parse_date(value) -> pd.Timestamp:
    """
    Try to parse a date regardless of what format it's in.
    pd.to_datetime with dayfirst=True handles most cases.
    Returns NaT (Not a Time) if it can't be parsed.
    """
    if pd.isna(value) or str(value).strip() in ["", "N/A", "-", "nan"]:
        return pd.NaT
    try:
        return pd.to_datetime(str(value).strip(), dayfirst=True)
    except Exception:
        return pd.NaT


def clean_date_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardise all date columns to datetime type.
    This makes it possible to calculate age, tenure, etc.
    """
    print("\n" + "=" * 60)
    print("STEP 3 — Cleaning date columns")
    print("=" * 60)

    date_cols = ["Date_of_Birth", "Hire_Date", "Exit_Date", "Last_Training_Date"]

    for col in date_cols:
        before_nulls = df[col].isna().sum()
        df[col] = df[col].apply(parse_date)
        after_nulls = df[col].isna().sum()
        parsed = len(df) - after_nulls
        print(f"✅ {col:<25} {parsed} dates parsed | {after_nulls} blanks/NaT")

    return df


# =============================================================
# STEP 4 — CLEAN SALARY & NUMERIC COLUMNS
# Remove $, commas, % signs and convert to numbers
# =============================================================

def clean_numeric_value(value) -> float:
    """
    Remove any currency symbols, commas, or spaces from a value
    and return it as a float number.
    Example: "$5,000" → 5000.0   |   "N/A" → NaN
    """
    if pd.isna(value):
        return np.nan
    # Convert to string, remove $, commas, spaces
    cleaned = str(value).replace("$", "").replace(",", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return np.nan


def clean_pct_value(value) -> float:
    """
    Remove % sign and return as float.
    Example: "5.5%" → 5.5   |   "5.5" → 5.5
    """
    if pd.isna(value):
        return np.nan
    cleaned = str(value).replace("%", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return np.nan


def clean_rating_value(value) -> float:
    """
    Handle ratings like "3/5" or "3" → returns 3.0
    """
    if pd.isna(value):
        return np.nan
    value_str = str(value).strip()
    if "/" in value_str:
        # Take the numerator only: "3/5" → "3"
        value_str = value_str.split("/")[0].strip()
    try:
        return float(value_str)
    except ValueError:
        return np.nan


def clean_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean all columns that should be numeric but may contain
    string formatting like $, commas, % or fractional formats.
    """
    print("\n" + "=" * 60)
    print("STEP 4 — Cleaning numeric columns")
    print("=" * 60)

    # Salary columns (may have $ and commas)
    for col in ["Monthly_Salary_Local", "Monthly_CTC_Local"]:
        df[col] = df[col].apply(clean_numeric_value)
        print(f"✅ {col:<30} → numeric (removed $, commas)")

    # These were already numeric but ensure correct type
    for col in ["Monthly_Salary_USD", "Monthly_CTC_USD", "FX_Rate_to_USD"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        print(f"✅ {col:<30} → numeric type confirmed")

    # Performance rating (may be "3/5" format)
    df["Performance_Rating"] = df["Performance_Rating"].apply(clean_rating_value)
    print("✅ Performance_Rating              → numeric (handled '3/5' format)")

    # Percentage column (may have % sign)
    df["Last_Salary_Increase_Pct"] = df["Last_Salary_Increase_Pct"].apply(clean_pct_value)
    print("✅ Last_Salary_Increase_Pct        → numeric (removed % sign)")

    # Other numeric columns
    for col in ["Training_Hours_Year", "Courses_Completed",
                "LD_Budget_Used_Pct", "Time_to_Hire_Days", "Interviewer_Rating"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        print(f"✅ {col:<30} → numeric type confirmed")

    return df


# =============================================================
# STEP 5 — CLEAN YES/NO COLUMNS
# Standardise all Boolean-like columns to "Yes" / "No"
# =============================================================

def clean_yesno_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Map all variants of yes/no to a consistent "Yes" / "No".
    """
    print("\n" + "=" * 60)
    print("STEP 5 — Standardising Yes/No columns")
    print("=" * 60)

    yes_values = {"yes", "y", "1", "true", "Yes", "YES", "Y"}
    no_values  = {"no",  "n", "0", "false", "No",  "NO",  "N"}

    yesno_cols = ["Probation_Passed", "Bonus_Received", "Offer_Accepted"]

    for col in yesno_cols:
        def map_yesno(val):
            if pd.isna(val):
                return np.nan
            v = str(val).strip()
            if v in yes_values:
                return "Yes"
            elif v in no_values:
                return "No"
            return val   # leave unchanged if unrecognised

        df[col] = df[col].apply(map_yesno)
        print(f"✅ {col:<25} → {sorted(df[col].dropna().unique())}")

    return df


# =============================================================
# STEP 6 — HANDLE MISSING VALUES
# Decide what to do with each blank: fill, flag, or leave
# =============================================================

def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Different columns need different strategies for missing data:
    - Exit-related fields: blank = "Not Applicable" (employee is Active)
    - Numeric fields: leave as NaN (don't invent data)
    - Text fields: fill with "Unknown" where needed
    """
    print("\n" + "=" * 60)
    print("STEP 6 — Handling missing values")
    print("=" * 60)

    # Termination fields: blank means the employee is still active
    # Replace NaN with "Not Applicable" so it's clear in Tableau
    for col in ["Termination_Category", "Termination_Reason"]:
        before = df[col].isna().sum()
        df[col] = df[col].fillna("Not Applicable")
        print(f"✅ {col:<30} {before} blanks → 'Not Applicable'")

    # Exit Date: NaT for active employees is fine — leave as-is
    print(f"ℹ️  Exit_Date: NaT left for Active employees ({df['Exit_Date'].isna().sum()} rows)")

    # Numeric training/recruitment fields: leave as NaN
    # (NaN is honest — we don't want to make up values)
    numeric_na_cols = [
        "Training_Hours_Year", "Courses_Completed",
        "LD_Budget_Used_Pct", "Time_to_Hire_Days", "Interviewer_Rating"
    ]
    for col in numeric_na_cols:
        n = df[col].isna().sum()
        print(f"ℹ️  {col:<30} {n} NaN values kept (do not impute)")

    # Last Training Date: leave NaT for leavers — acceptable
    print(f"ℹ️  Last_Training_Date: {df['Last_Training_Date'].isna().sum()} NaT values kept")

    return df


# =============================================================
# STEP 7 — CREATE CALCULATED COLUMNS
# Build new fields from existing data (Age, Tenure, Annual $)
# =============================================================

def create_calculated_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create useful derived columns:
    - Age (years) from Date_of_Birth
    - Tenure_Years from Hire_Date (or Exit_Date for leavers)
    - Annual_Salary_USD = Monthly_Salary_USD × 12
    - Annual_CTC_USD    = Monthly_CTC_USD × 12
    - Attrition_Flag    = 1 if not Active, else 0 (useful for attrition rate)
    """
    print("\n" + "=" * 60)
    print("STEP 7 — Creating calculated columns")
    print("=" * 60)

    # Age in full years
    df["Age"] = df["Date_of_Birth"].apply(
        lambda dob: (TODAY - dob).days // 365 if pd.notna(dob) else np.nan
    )
    print(f"✅ Age created | Range: {int(df['Age'].min())}–{int(df['Age'].max())} years")

    # Tenure in years (use Exit_Date for leavers, TODAY for active)
    def calc_tenure(row):
        if pd.isna(row["Hire_Date"]):
            return np.nan
        end_date = row["Exit_Date"] if pd.notna(row["Exit_Date"]) else TODAY
        return round((end_date - row["Hire_Date"]).days / 365.25, 1)

    df["Tenure_Years"] = df.apply(calc_tenure, axis=1)
    print(f"✅ Tenure_Years created | Range: {df['Tenure_Years'].min()}–{df['Tenure_Years'].max()} years")

    # Annual salary figures (monthly × 12)
    df["Annual_Salary_USD"] = (df["Monthly_Salary_USD"] * 12).round(0)
    df["Annual_CTC_USD"]    = (df["Monthly_CTC_USD"]    * 12).round(0)
    print("✅ Annual_Salary_USD and Annual_CTC_USD created")

    # Attrition flag (1 = left the company, 0 = still active)
    # Useful for calculating attrition rate in Tableau
    df["Attrition_Flag"] = df["Employment_Status"].apply(
        lambda s: 1 if s in ["Resigned", "Terminated"] else 0
    )
    attrition_rate = df["Attrition_Flag"].mean() * 100
    print(f"✅ Attrition_Flag created | Overall attrition rate: {attrition_rate:.1f}%")

    return df


# =============================================================
# STEP 8 — FINAL DATA TYPE ENFORCEMENT
# Make sure every column has the right type before saving
# =============================================================

def enforce_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Explicitly set data types. This prevents silent bugs where
    Tableau or Python treats numbers as text or vice versa.
    """
    print("\n" + "=" * 60)
    print("STEP 8 — Enforcing data types")
    print("=" * 60)

    # Integer columns (no decimals needed)
    int_cols = [
        "Monthly_Salary_USD", "Monthly_CTC_USD",
        "Monthly_Salary_Local", "Monthly_CTC_Local",
        "Annual_Salary_USD", "Annual_CTC_USD",
        "Courses_Completed", "Time_to_Hire_Days",
        "Age", "Attrition_Flag",
    ]
    for col in int_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        # Use Int64 (capital I) which supports NaN in integer columns
        df[col] = df[col].astype("Int64")

    # Float columns (decimals needed)
    float_cols = [
        "FX_Rate_to_USD", "Performance_Rating",
        "Last_Salary_Increase_Pct", "Training_Hours_Year",
        "LD_Budget_Used_Pct", "Interviewer_Rating",
        "Tenure_Years",
    ]
    for col in float_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").round(2)

    # Date columns → string YYYY-MM-DD for clean CSV export
    date_cols = ["Date_of_Birth", "Hire_Date", "Exit_Date", "Last_Training_Date"]
    for col in date_cols:
        df[col] = df[col].dt.strftime("%Y-%m-%d").replace("NaT", "")

    print(f"✅ Data types enforced for {len(int_cols + float_cols + date_cols)} columns")

    return df


# =============================================================
# STEP 9 — VALIDATION REPORT
# Print a summary so we can verify cleaning worked
# =============================================================

def validation_report(df_raw: pd.DataFrame, df_clean: pd.DataFrame):
    """
    Print a before/after comparison to confirm cleaning succeeded.
    """
    print("\n" + "=" * 60)
    print("STEP 9 — Validation Report")
    print("=" * 60)

    print(f"\n{'Metric':<35} {'Before':>10} {'After':>10}")
    print("-" * 57)
    print(f"{'Total rows':<35} {len(df_raw):>10} {len(df_clean):>10}")
    print(f"{'Total columns':<35} {df_raw.shape[1]:>10} {df_clean.shape[1]:>10}")
    print(f"{'Unique Department values':<35} {df_raw['Department'].nunique():>10} {df_clean['Department'].nunique():>10}")
    print(f"{'Unique Gender values':<35} {df_raw['Gender'].nunique():>10} {df_clean['Gender'].nunique():>10}")
    print(f"{'Total missing values':<35} {df_raw.isnull().sum().sum():>10} {df_clean.isnull().sum().sum():>10}")

    print("\n📊 Clean Dataset Overview:")
    print(f"   Shape     : {df_clean.shape[0]} rows × {df_clean.shape[1]} columns")
    print(f"   Countries : {sorted(df_clean['Country'].unique())}")
    print(f"   Depts     : {sorted(df_clean['Department'].unique())}")
    print(f"   Status    : {df_clean['Employment_Status'].value_counts().to_dict()}")
    print(f"   Age range : {df_clean['Age'].min()}–{df_clean['Age'].max()} years")
    print(f"   Tenure    : {df_clean['Tenure_Years'].min()}–{df_clean['Tenure_Years'].max()} years")

    print("\n📋 Remaining null values (expected blanks only):")
    nulls = df_clean.isnull().sum()
    nulls = nulls[nulls > 0]
    if len(nulls) == 0:
        print("   ✅ No unexpected nulls!")
    else:
        for col, n in nulls.items():
            print(f"   {col:<35} {n} nulls")


# =============================================================
# MAIN — RUN ALL STEPS IN ORDER
# =============================================================

def main():
    print("\n🚀 HR Data Cleaning Pipeline — Starting\n")

    # Load
    df_raw   = load_data(RAW_PATH)
    df_clean = df_raw.copy()   # always work on a copy, never touch the raw file

    # Clean
    df_clean = clean_text_columns(df_clean)
    df_clean = clean_date_columns(df_clean)
    df_clean = clean_numeric_columns(df_clean)
    df_clean = clean_yesno_columns(df_clean)
    df_clean = handle_missing_values(df_clean)
    df_clean = create_calculated_columns(df_clean)
    df_clean = enforce_data_types(df_clean)

    # Validate
    validation_report(df_raw, df_clean)

    # Save
    df_clean.to_csv(CLEAN_PATH, index=False)
    print(f"\n✅ Clean dataset saved to: {CLEAN_PATH}")
    print("\n🎉 Cleaning complete! Ready for EDA and Tableau.\n")


if __name__ == "__main__":
    main()
