import pandas as pd

def detect_churn():
    # -------------------------
    # LOAD DATA
    # -------------------------
    customers = pd.read_csv("../data/customers.csv")
    jobs = pd.read_csv("../data/job_changes.csv")
    schools = pd.read_csv("../data/schools.csv")

    # -------------------------
    # MERGE JOB + SCHOOL DATA
    # -------------------------
    merged = jobs.merge(
        schools,
        left_on="new_school",
        right_on="school_name",
        how="left"
    )

    # -------------------------
    # HANDLE MISSING VALUES
    # -------------------------
    merged["is_toddle_customer"] = merged["is_toddle_customer"].fillna("No")

    # -------------------------
    # ADD STATUS COLUMN
    # -------------------------
    merged["status"] = merged["is_toddle_customer"].apply(
        lambda x: "Churn (Non-Toddle)" if x == "No" else "Retained (Toddle)"
    )

    # -------------------------
    # OPTIONAL: MERGE CUSTOMER INFO
    # -------------------------
    merged = merged.merge(
        customers,
        on="person_id",
        how="left"
    )

    # -------------------------
    # SELECT CLEAN COLUMNS
    # -------------------------
    final_df = merged[
        [
            "person_id",
            "name",
            "old_school",
            "new_school",
            "is_toddle_customer",
            "status",
            "change_date"
        ]
    ]

    return final_df