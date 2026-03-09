"""
=============================================================
HR Analytics Project — Synthetic Dataset Generator
=============================================================
This script generates a realistic but fully synthetic HR dataset
for a multinational Technology/Software company operating across
the Asia Pacific region.

IMPORTANT: All data is fictional and does not represent any real
employees or organisation. It is designed to reflect real-world
HR metrics and patterns based on professional HR experience.

Dataset: 1,000 employees × 34 columns
Author:  [Your Name]
=============================================================
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# ── Reproducibility ───────────────────────────────────────────
# Setting a seed means anyone who runs this script gets the
# exact same dataset — important for reproducibility.
np.random.seed(42)
random.seed(42)

# =============================================================
# SECTION 1 — REFERENCE DATA
# All the lookup lists we'll sample from when building the data
# =============================================================

# ── Countries & headcount distribution (tiered) ───────────────
COUNTRY_CONFIG = {
    # Large markets
    "Singapore":   {"code": "SG", "currency": "SGD", "fx": 1.35,  "count": 150},
    "Australia":   {"code": "AU", "currency": "AUD", "fx": 1.53,  "count": 130},
    "India":       {"code": "IN", "currency": "INR", "fx": 83.0,  "count": 120},
    # Mid markets (SEA)
    "Malaysia":    {"code": "MY", "currency": "MYR", "fx": 4.70,  "count": 80},
    "Thailand":    {"code": "TH", "currency": "THB", "fx": 36.0,  "count": 70},
    "Indonesia":   {"code": "ID", "currency": "IDR", "fx": 15600, "count": 65},
    "Philippines": {"code": "PH", "currency": "PHP", "fx": 56.0,  "count": 60},
    "Vietnam":     {"code": "VN", "currency": "VND", "fx": 24500, "count": 55},
    # Smaller markets
    "China":       {"code": "CN", "currency": "CNY", "fx": 7.25,  "count": 70},
    "Hong Kong":   {"code": "HK", "currency": "HKD", "fx": 7.82,  "count": 50},
    "Taiwan":      {"code": "TW", "currency": "TWD", "fx": 31.5,  "count": 50},
    "Korea":       {"code": "KR", "currency": "KRW", "fx": 1330,  "count": 55},
    "Japan":       {"code": "JP", "currency": "JPY", "fx": 149.0, "count": 45},
}
# Total = 1,000 ✅

# ── Office locations per country ──────────────────────────────
OFFICE_LOCATIONS = {
    "Singapore":   ["Singapore"],
    "Australia":   ["Sydney", "Melbourne"],
    "India":       ["Mumbai", "Bangalore", "Delhi"],
    "Malaysia":    ["Kuala Lumpur"],
    "Thailand":    ["Bangkok"],
    "Indonesia":   ["Jakarta"],
    "Philippines": ["Manila"],
    "Vietnam":     ["Ho Chi Minh City", "Hanoi"],
    "China":       ["Shanghai", "Beijing"],
    "Hong Kong":   ["Hong Kong"],
    "Taiwan":      ["Taipei"],
    "Korea":       ["Seoul"],
    "Japan":       ["Tokyo"],
}

# ── Monthly salary ranges per country (local currency) ───────
SALARY_RANGES = {
    "Singapore":   (3500,  18000),
    "Australia":   (5000,  22000),
    "India":       (50000, 500000),
    "Malaysia":    (4000,  25000),
    "Thailand":    (30000, 180000),
    "Indonesia":   (8000000, 80000000),
    "Philippines": (25000, 150000),
    "Vietnam":     (15000000, 80000000),
    "China":       (8000,  60000),
    "Hong Kong":   (18000, 120000),
    "Taiwan":      (40000, 250000),
    "Korea":       (3000000, 15000000),
    "Japan":       (250000, 1200000),
}

# ── Departments & typical job titles per grade ────────────────
DEPARTMENTS = ["HR", "Finance", "Legal", "IT", "Marketing", "Delivery", "Sales"]

JOB_TITLES = {
    "HR":        ["HR Assistant", "HR Executive", "HR Specialist", "HR Business Partner",
                  "Senior HR Business Partner", "HR Manager", "HR Director"],
    "Finance":   ["Finance Assistant", "Finance Analyst", "Senior Finance Analyst",
                  "Finance Manager", "Senior Finance Manager", "Finance Director", "CFO"],
    "Legal":     ["Legal Assistant", "Legal Executive", "Legal Counsel",
                  "Senior Legal Counsel", "Legal Manager", "Legal Director", "General Counsel"],
    "IT":        ["IT Support", "Software Engineer", "Senior Software Engineer",
                  "Tech Lead", "Engineering Manager", "Senior Engineering Manager", "CTO"],
    "Marketing": ["Marketing Assistant", "Marketing Executive", "Marketing Specialist",
                  "Senior Marketing Specialist", "Marketing Manager", "Senior Marketing Manager",
                  "Marketing Director"],
    "Delivery":  ["Delivery Coordinator", "Project Analyst", "Project Manager",
                  "Senior Project Manager", "Delivery Manager", "Senior Delivery Manager",
                  "Delivery Director"],
    "Sales":     ["Sales Executive", "Account Executive", "Senior Account Executive",
                  "Sales Manager", "Senior Sales Manager", "Regional Sales Manager",
                  "Sales Director"],
}

# Grade maps to index in job title list above
GRADE_TITLE_MAP = {"G1": 0, "G2": 1, "G3": 2, "G4": 3, "G5": 4, "G6": 5}

# Grade distribution (more junior/mid than senior — realistic bell curve)
GRADE_WEIGHTS = {"G1": 0.15, "G2": 0.25, "G3": 0.25, "G4": 0.20, "G5": 0.10, "G6": 0.05}

# ── Names pool (diverse, multi-national) ─────────────────────
FIRST_NAMES = [
    "Wei", "Li", "Priya", "Arjun", "Siti", "Ahmad", "Nguyen", "Tran",
    "James", "Sarah", "David", "Emma", "Raj", "Ananya", "Min", "Ji",
    "Somchai", "Nattaporn", "Budi", "Dewi", "Maria", "Jose", "Chen",
    "Fang", "Haruto", "Yuki", "Seo", "Jin", "Thomas", "Sophie",
    "Michael", "Jessica", "Kevin", "Amanda", "Chris", "Michelle",
    "Arun", "Kavya", "Suresh", "Lakshmi", "Tan", "Lee", "Wong",
    "Ong", "Lim", "Chan", "Ng", "Koh", "Ravi", "Meera",
]

LAST_NAMES = [
    "Kumar", "Singh", "Sharma", "Patel", "Wang", "Zhang", "Li", "Chen",
    "Tan", "Lim", "Lee", "Wong", "Ng", "Chan", "Ong", "Koh",
    "Nguyen", "Tran", "Le", "Pham", "Suwannarat", "Charoenwong",
    "Santoso", "Wijaya", "Dela Cruz", "Santos", "Reyes",
    "Smith", "Johnson", "Williams", "Brown", "Jones",
    "Müller", "Kim", "Park", "Choi", "Yamamoto", "Tanaka", "Suzuki",
    "Liu", "Yang", "Huang", "Guo", "Lin", "Wu",
]

NATIONALITIES = [
    "Singaporean", "Australian", "Indian", "Malaysian", "Thai",
    "Indonesian", "Filipino", "Vietnamese", "Chinese", "Hong Konger",
    "Taiwanese", "Korean", "Japanese", "British", "American",
]

# ── Termination reasons ───────────────────────────────────────
TERMINATION_MAP = {
    "Voluntary":   ["Personal Reason", "Better Opportunity",
                    "Relocation", "Further Studies", "Health Reasons"],
    "Involuntary": ["Contract Ended", "Performance",
                    "Redundancy", "Misconduct"],
}

# ── Recruitment sources ───────────────────────────────────────
RECRUITMENT_SOURCES = ["LinkedIn", "Referral", "Agency", "Job Board", "Internal Transfer"]

# =============================================================
# SECTION 2 — HELPER FUNCTIONS
# =============================================================

def random_date(start_year: int, end_year: int) -> datetime:
    """Return a random date between start_year and end_year."""
    start = datetime(start_year, 1, 1)
    end   = datetime(end_year, 12, 31)
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))


def format_date_messy(dt: datetime) -> str:
    """
    Intentional mess: return the date in one of three formats.
    This simulates real-world HR data where different people
    enter dates differently.
    """
    fmt = random.choice(["iso", "dmy", "long"])
    if fmt == "iso":
        return dt.strftime("%Y-%m-%d")          # e.g. 2021-03-15
    elif fmt == "dmy":
        return dt.strftime("%d/%m/%Y")           # e.g. 15/03/2021
    else:
        return dt.strftime("%B %d %Y")           # e.g. March 15 2021


def messy_text(value: str, variants: list) -> str:
    """
    Randomly return a 'messy' version of a clean value.
    20% chance of mess — keeping it realistic (not every row is dirty).
    """
    if random.random() < 0.20:
        return random.choice(variants)
    return value


def messy_gender(gender: str) -> str:
    variants = {
        "Male":       ["male", "MALE", "M", "m"],
        "Female":     ["female", "FEMALE", "F", "f"],
        "Non-binary": ["non-binary", "Non Binary", "NB"],
    }
    if random.random() < 0.20:
        return random.choice(variants.get(gender, [gender]))
    return gender


def messy_department(dept: str) -> str:
    variants = {
        "HR":       ["hr", "H.R.", "Human Resources", "HR Dept"],
        "IT":       ["it", "I.T.", "Information Technology", "Tech"],
        "Finance":  ["finance", "FINANCE", "Fin"],
        "Legal":    ["legal", "LEGAL", "Lgl"],
        "Marketing":["marketing", "MARKETING", "Mktg"],
        "Delivery": ["delivery", "DELIVERY", "Del"],
        "Sales":    ["sales", "SALES", "Sls"],
    }
    if random.random() < 0.20:
        return random.choice(variants.get(dept, [dept]))
    return dept


def messy_employment_type(et: str) -> str:
    variants = {
        "Full-time":  ["full time", "Full Time", "FT", "fulltime"],
        "Contractor": ["contractor", "Contract", "contract", "CTR"],
        "Intern":     ["intern", "INTERN", "Internship"],
        "Expat":      ["expat", "EXPAT", "Expatriate"],
    }
    if random.random() < 0.20:
        return random.choice(variants.get(et, [et]))
    return et


def messy_yes_no(value: str) -> str:
    if random.random() < 0.20:
        return random.choice(["yes", "YES", "Y", "y", "no", "NO", "N", "n"]
                             if value == "Yes" else ["no", "NO", "N", "n"])
    return value


def messy_source(source: str) -> str:
    variants = {
        "LinkedIn": ["linkedin", "LINKEDIN", "Linked In", "linked in"],
        "Referral": ["referral", "REFERRAL", "Ref"],
        "Agency":   ["agency", "AGENCY", "Recruitment Agency"],
        "Job Board":["job board", "JOB BOARD", "Jobboard", "Job board"],
        "Internal Transfer": ["internal", "Internal", "INTERNAL", "Int Transfer"],
    }
    if random.random() < 0.20:
        return random.choice(variants.get(source, [source]))
    return source


def messy_salary(value: float) -> str:
    """Some salaries stored with $ sign and commas — messy!"""
    if random.random() < 0.15:
        return f"${value:,.0f}"
    elif random.random() < 0.15:
        return f"{value:,.0f}"
    return str(round(value))


def messy_rating(rating: int) -> str:
    """Some ratings stored as '3/5' instead of '3'."""
    if random.random() < 0.20:
        return f"{rating}/5"
    return str(rating)


def messy_pct(value: float) -> str:
    """Some percentages stored with % sign."""
    if random.random() < 0.20:
        return f"{value}%"
    return str(value)


# =============================================================
# SECTION 3 — BUILD EACH EMPLOYEE ROW
# =============================================================

def build_employee(emp_id: int, country: str, config: dict) -> dict:
    """
    Generate one employee row with realistic, correlated values.
    All the 'mess' is injected here by the helper functions above.
    """

    # ── Basic identity ─────────────────────────────────────────
    first = random.choice(FIRST_NAMES)
    last  = random.choice(LAST_NAMES)
    full_name_clean = f"{first} {last}"

    # Intentional mess: ~20% chance of ALL CAPS or all lowercase name
    name_style = random.random()
    if name_style < 0.10:
        full_name = full_name_clean.upper()
    elif name_style < 0.20:
        full_name = full_name_clean.lower()
    else:
        full_name = full_name_clean

    gender      = random.choice(["Male", "Male", "Female", "Female", "Non-binary"])
    dob         = random_date(1970, 2001)  # Age range ~23–54
    nationality = random.choice(NATIONALITIES)

    # ── Organisation ──────────────────────────────────────────
    department  = random.choice(DEPARTMENTS)
    grade       = random.choices(
        list(GRADE_WEIGHTS.keys()),
        weights=list(GRADE_WEIGHTS.values())
    )[0]
    title_index = GRADE_TITLE_MAP.get(grade, 0)
    job_title   = JOB_TITLES[department][title_index]
    office      = random.choice(OFFICE_LOCATIONS[country])
    work_mode   = random.choices(
        ["Hybrid", "Onsite", "Remote"],
        weights=[0.50, 0.30, 0.20]
    )[0]
    region = "Asia Pacific"

    # ── Employment lifecycle ───────────────────────────────────
    # Senior staff tend to have longer tenures
    if grade in ["G5", "G6"]:
        hire_date = random_date(2015, 2020)
    elif grade in ["G3", "G4"]:
        hire_date = random_date(2017, 2022)
    else:
        hire_date = random_date(2019, 2024)

    # Employment type — Expats skew senior; Interns are G1
    if grade == "G1":
        emp_type_clean = random.choices(
            ["Full-time", "Intern", "Contractor"],
            weights=[0.50, 0.35, 0.15]
        )[0]
    elif grade in ["G5", "G6"]:
        emp_type_clean = random.choices(
            ["Full-time", "Expat", "Contractor"],
            weights=[0.70, 0.20, 0.10]
        )[0]
    else:
        emp_type_clean = random.choices(
            ["Full-time", "Contractor", "Intern"],
            weights=[0.75, 0.20, 0.05]
        )[0]

    # Employment status — ~80% active, ~20% separated
    status = random.choices(
        ["Active", "Resigned", "Terminated"],
        weights=[0.80, 0.13, 0.07]
    )[0]

    # Exit date only for separated employees
    if status in ["Resigned", "Terminated"]:
        exit_date_dt  = hire_date + timedelta(days=random.randint(180, 2500))
        exit_date_dt  = min(exit_date_dt, datetime(2024, 12, 31))

        # Termination category and reason
        if status == "Resigned":
            term_cat    = "Voluntary"
            term_reason = random.choice(TERMINATION_MAP["Voluntary"])
        else:
            term_cat    = "Involuntary"
            term_reason = random.choice(TERMINATION_MAP["Involuntary"])

        # Messy exit date: some rows use "N/A" or "-" instead of blank
        exit_date_mess = random.choice([
            format_date_messy(exit_date_dt),
            format_date_messy(exit_date_dt),  # majority get a date
            "N/A", "-"
        ])
    else:
        exit_date_dt  = None
        exit_date_mess = ""   # blank for active employees
        term_cat      = ""
        term_reason   = ""

    # Probation passed — Interns and new joiners may still be in probation
    if status == "Active" and (datetime.now() - hire_date).days < 180:
        prob_passed = random.choices(["Yes", "No"], weights=[0.70, 0.30])[0]
    elif status != "Active":
        prob_passed = random.choices(["Yes", "No"], weights=[0.85, 0.15])[0]
    else:
        prob_passed = "Yes"

    # ── Compensation ──────────────────────────────────────────
    currency = config["currency"]
    fx_rate  = config["fx"]
    sal_min, sal_max = SALARY_RANGES[country]

    # Grade influences salary — higher grade = higher salary percentile
    grade_pct = {"G1": 0.10, "G2": 0.25, "G3": 0.45, "G4": 0.65, "G5": 0.82, "G6": 0.95}
    pct       = grade_pct[grade]
    sal_local = round(sal_min + (sal_max - sal_min) * (pct + random.uniform(-0.08, 0.08)))
    sal_local = max(sal_min, min(sal_max, sal_local))

    ctc_local     = round(sal_local * 1.15)
    sal_usd       = round(sal_local / fx_rate)
    ctc_usd       = round(ctc_local / fx_rate)

    perf_rating   = random.choices([1, 2, 3, 4, 5], weights=[0.05, 0.10, 0.35, 0.35, 0.15])[0]
    sal_increase  = round(random.uniform(0, 15), 1)
    bonus         = random.choices(["Yes", "No"], weights=[0.65, 0.35])[0]

    # ── Learning & Development ────────────────────────────────
    # Active employees get more training
    if status == "Active":
        training_hrs  = round(random.uniform(4, 80), 1)
        courses       = random.randint(1, 12)
        last_train_dt = random_date(2022, 2024)
        ld_budget_pct = round(random.uniform(10, 100))
    else:
        # Some leavers have blank training data
        training_hrs  = round(random.uniform(0, 60), 1) if random.random() > 0.20 else None
        courses       = random.randint(0, 8)             if random.random() > 0.20 else None
        last_train_dt = random_date(2021, 2023)          if random.random() > 0.20 else None
        ld_budget_pct = round(random.uniform(0, 80))     if random.random() > 0.20 else None

    # ── Recruitment ───────────────────────────────────────────
    rec_source_clean = random.choice(RECRUITMENT_SOURCES)
    time_to_hire     = random.randint(15, 95) if random.random() > 0.05 else None  # 5% blank
    offer_accepted   = random.choices(["Yes", "No"], weights=[0.88, 0.12])[0]
    int_rating       = random.choices([1, 2, 3, 4, 5],
                                       weights=[0.03, 0.07, 0.30, 0.40, 0.20])[0] \
                       if random.random() > 0.05 else None  # 5% blank

    # ==========================================================
    # SECTION 4 — APPLY INTENTIONAL MESS
    # All the clean values above get run through mess functions
    # so that ~20% of values have formatting inconsistencies.
    # This simulates real-world dirty HR data.
    # ==========================================================

    row = {
        # Employee Identity
        "Employee_ID":              f"EMP{str(emp_id).zfill(4)}",
        "Full_Name":                full_name,                           # ← messy case
        "Gender":                   messy_gender(gender),                # ← messy format
        "Date_of_Birth":            format_date_messy(dob),              # ← messy date
        "Nationality":              nationality,

        # Organisation
        "Region":                   region,
        "Country":                  country,
        "Office_Location":          office,
        "Department":               messy_department(department),        # ← messy case
        "Job_Title":                job_title,
        "Grade_Level":              grade,
        "Work_Mode":                work_mode,

        # Lifecycle
        "Hire_Date":                format_date_messy(hire_date),        # ← messy date
        "Exit_Date":                exit_date_mess,                      # ← messy / blank
        "Employment_Status":        status,
        "Employment_Type":          messy_employment_type(emp_type_clean), # ← messy
        "Probation_Passed":         messy_yes_no(prob_passed),           # ← messy
        "Termination_Category":     term_cat,
        "Termination_Reason":       term_reason,

        # Compensation
        "Currency":                 currency,
        "FX_Rate_to_USD":           fx_rate,
        "Monthly_Salary_Local":     messy_salary(sal_local),             # ← messy $,
        "Monthly_CTC_Local":        messy_salary(ctc_local),             # ← messy $,
        "Monthly_Salary_USD":       sal_usd,
        "Monthly_CTC_USD":          ctc_usd,
        "Performance_Rating":       messy_rating(perf_rating),           # ← "3/5" mess
        "Last_Salary_Increase_Pct": messy_pct(sal_increase),            # ← "5%" mess
        "Bonus_Received":           messy_yes_no(bonus),                 # ← messy

        # Learning & Development
        "Training_Hours_Year":      training_hrs,                        # ← some None
        "Courses_Completed":        courses,                             # ← some None
        "Last_Training_Date":       format_date_messy(last_train_dt)
                                    if last_train_dt else None,          # ← messy / blank
        "LD_Budget_Used_Pct":       ld_budget_pct,                       # ← some None

        # Recruitment
        "Recruitment_Source":       messy_source(rec_source_clean),      # ← messy
        "Time_to_Hire_Days":        time_to_hire,                        # ← some None
        "Offer_Accepted":           messy_yes_no(offer_accepted),        # ← messy
        "Interviewer_Rating":       int_rating,                          # ← some None
    }

    return row


# =============================================================
# SECTION 5 — GENERATE ALL 1,000 ROWS
# =============================================================

def generate_dataset() -> pd.DataFrame:
    print("🚀 Generating synthetic HR dataset...")
    rows   = []
    emp_id = 1

    for country, config in COUNTRY_CONFIG.items():
        count = config["count"]
        print(f"   ├─ {country:<15} {count} employees")
        for _ in range(count):
            row = build_employee(emp_id, country, config)
            rows.append(row)
            emp_id += 1

    df = pd.DataFrame(rows)
    print(f"\n✅ Dataset generated: {len(df)} rows × {len(df.columns)} columns")
    return df


# =============================================================
# SECTION 6 — SAVE TO FILE
# =============================================================

if __name__ == "__main__":
    df = generate_dataset()

    # Save raw (messy) dataset
    output_path = os.path.join(
        os.path.dirname(__file__), "..", "data", "raw", "hr_data_raw.csv"
    )
    output_path = os.path.normpath(output_path)
    df.to_csv(output_path, index=False)

    print(f"\n📁 Raw dataset saved to: {output_path}")
    print("\n📊 Quick preview:")
    print(df[["Employee_ID", "Full_Name", "Country", "Department",
              "Grade_Level", "Employment_Status", "Monthly_Salary_USD"]].head(10).to_string())
    print("\n📋 Column list:")
    for i, col in enumerate(df.columns, 1):
        print(f"   {i:>2}. {col}")
