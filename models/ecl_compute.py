import pandas as pd

def calculate_ecl(df, pd_model):
    X = df.drop(columns=["loan_status"])
    df["PD"] = pd_model.predict(X)
    df["LGD"] = 0.45
    df["EAD"] = df["loan_amnt"]
    df["ECL"] = df["PD"] * df["LGD"] * df["EAD"]
    return df

# Load dataset
df = pd.read_csv("app/data/bank_loan_data.csv")

# Compute ECL
df_ecl = calculate_ecl(df)

# Group by segment (e.g., loan_intent)
df_segment = df_ecl.groupby("loan_intent").agg({
    "ECL": "mean",
    "PD": "mean",
    "loan_amnt": "mean"
}).reset_index().rename(columns={"loan_intent": "segment"})

# Save for FastAPI routes
df_segment.to_csv("app/data/ecl_segment_data.csv", index=False)
print("✅ ECL segment data saved at app/data/ecl_segment_data.csv")