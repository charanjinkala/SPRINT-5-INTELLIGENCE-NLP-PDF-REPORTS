"""
Sprint 5 - Day 30

Pros & Cons Generator
"""

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RATIO_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "financial_ratios.xlsx"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "output"
    / "pros_cons.csv"
)

def load_ratios():

    return pd.read_excel(RATIO_FILE)

def generate_pros_cons(row):

    pros = []

    cons = []

    # ROE
    if row["return_on_equity_pct"] >= 20:
        pros.append("High Return on Equity")

    elif row["return_on_equity_pct"] < 10:
        cons.append("Low Return on Equity")

    # Debt
    if row["debt_to_equity"] <= 0.5:
        pros.append("Low Debt")

    elif row["debt_to_equity"] > 2:
        cons.append("High Debt")

    # Net Profit Margin
    if row["net_profit_margin_pct"] >= 15:
        pros.append("Healthy Net Profit Margin")

    elif row["net_profit_margin_pct"] < 5:
        cons.append("Low Net Profit Margin")

    # Operating Margin
    if row["operating_profit_margin_pct"] >= 20:
        pros.append("Strong Operating Margin")

    elif row["operating_profit_margin_pct"] < 10:
        cons.append("Weak Operating Margin")

    # Interest Coverage
    if row["interest_coverage"] >= 5:
        pros.append("Comfortable Interest Coverage")

    elif row["interest_coverage"] < 2:
        cons.append("Poor Interest Coverage")

    # Free Cash Flow
    if row["free_cash_flow_cr"] > 0:
        pros.append("Positive Free Cash Flow")

    else:
        cons.append("Negative Free Cash Flow")

    return pros, cons

def build_report(df):

    records = []

    for _, row in df.iterrows():

        pros, cons = generate_pros_cons(row)

        records.append(
            {
                "company_id": row["company_id"],
                "year": row["year"],
                "pros": "; ".join(pros),
                "cons": "; ".join(cons)
            }
        )

    return pd.DataFrame(records)


def main():

    ratios = load_ratios()

    report = build_report(ratios)

    report.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(report.head())

    print()

    print("Saved to")

    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()