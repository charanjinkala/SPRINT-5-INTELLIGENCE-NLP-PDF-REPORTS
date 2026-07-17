"""
Sprint 5 - Day 29

NLP Analysis Parser

Parses text-based CAGR metrics from analysis.xlsx
and converts them into a structured format.
"""

import re
from pathlib import Path

import pandas as pd


# --------------------------------------------------
# Project Paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "analysis.xlsx"
)

OUTPUT_DIR = PROJECT_ROOT / "output"

PARSED_FILE = OUTPUT_DIR / "analysis_parsed.csv"

FAILURE_FILE = OUTPUT_DIR / "parse_failures.csv"

# --------------------------------------------------
# Regex Patterns
# --------------------------------------------------

YEAR_PATTERN = re.compile(
    r"(\d+)\s*Years?:?\s*(-?[\d.]+)%"
)

LAST_YEAR_PATTERN = re.compile(
    r"Last\s+Year:?\s*(-?[\d.]+)%"
)

TTM_PATTERN = re.compile(
    r"TTM:?\s*(-?[\d.]+)%"
)

# --------------------------------------------------
# Fields to Parse
# --------------------------------------------------

FIELDS = {
    "compounded_sales_growth": "sales_cagr",
    "compounded_profit_growth": "profit_cagr",
    "stock_price_cagr": "stock_price_cagr",
    "roe": "roe",
}


# --------------------------------------------------
# Load Dataset
# --------------------------------------------------

def load_analysis():

    return pd.read_excel(
        INPUT_FILE,
        header=1
    )

def parse_text(text):

    if pd.isna(text):
        return None

    text = str(text).strip()

    # 1 Year / 3 Years / 5 Years / 10 Years
    match = YEAR_PATTERN.search(text)

    if match:
        return int(match.group(1)), float(match.group(2))

    # Last Year
    match = LAST_YEAR_PATTERN.search(text)

    if match:
        return 1, float(match.group(1))

    # TTM
    match = TTM_PATTERN.search(text)

    if match:
        return 0, float(match.group(1))

    return None

# --------------------------------------------------
# Main Parser
# --------------------------------------------------

def parse_analysis(df):

    parsed_rows = []

    failed_rows = []

    for _, row in df.iterrows():

        company = row["company_id"]

        for column, metric in FIELDS.items():

            result = parse_text(row[column])

            if result is None:

                failed_rows.append(
                    {
                        "company_id": company,
                        "column": column,
                        "text": row[column],
                    }
                )

                continue

            years, value = result

            parsed_rows.append(
                {
                    "company_id": company,
                    "metric_type": metric,
                    "period_years": years,
                    "value_pct": value,
                }
            )

    parsed_df = pd.DataFrame(parsed_rows)

    failure_df = pd.DataFrame(failed_rows)

    return parsed_df, failure_df


# --------------------------------------------------
# Save Outputs
# --------------------------------------------------

def save_outputs(parsed_df, failure_df):

    OUTPUT_DIR.mkdir(exist_ok=True)

    parsed_df.to_csv(
        PARSED_FILE,
        index=False,
    )

    failure_df.to_csv(
        FAILURE_FILE,
        index=False,
    )


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    print("=" * 60)
    print("Analysis Parser")
    print("=" * 60)

    analysis = load_analysis()

    parsed_df, failure_df = parse_analysis(
        analysis
    )

    save_outputs(
        parsed_df,
        failure_df,
    )

    print()

    print(f"Rows Parsed : {len(parsed_df)}")

    print(f"Failures    : {len(failure_df)}")

    print()

    print("Output Files")

    print(PARSED_FILE)

    print(FAILURE_FILE)


if __name__ == "__main__":
    main()