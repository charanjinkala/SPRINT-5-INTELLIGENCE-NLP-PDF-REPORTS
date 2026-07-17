"""
Sprint 5
Sector Report Generator
"""

from pathlib import Path

import pandas as pd

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

# ---------------------------------------------------------
# Project Paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW = PROJECT_ROOT / "data" / "raw"
OUTPUT = PROJECT_ROOT / "output"

COMPANIES_FILE = RAW / "companies.xlsx"
RATIOS_FILE = RAW / "financial_ratios.xlsx"
SECTORS_FILE = RAW / "sectors.xlsx"

REPORT_FOLDER = PROJECT_ROOT / "reports" / "sector"

REPORT_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)

# ---------------------------------------------------------
# Styles
# ---------------------------------------------------------

styles = getSampleStyleSheet()

TITLE = styles["Heading1"]
TITLE.alignment = TA_CENTER

HEADING = styles["Heading2"]

BODY = styles["BodyText"]

# ---------------------------------------------------------
# Load Data
# ---------------------------------------------------------

def load_data():

    # Companies
    companies = pd.read_excel(
        COMPANIES_FILE,
        header=1
    )
    companies.columns = companies.columns.str.strip()

    # Financial Ratios
    ratios = pd.read_excel(RATIOS_FILE)

    # Sector Mapping
    sectors = pd.read_excel(SECTORS_FILE)

    return companies, ratios, sectors

# ---------------------------------------------------------
# Latest Year Helper
# ---------------------------------------------------------

def latest_ratios(ratios):

    ratios = ratios.sort_values("year")

    return ratios.groupby("company_id").tail(1)


# ---------------------------------------------------------
# Generate Sector PDF
# ---------------------------------------------------------

def generate_sector_pdf(sector_name, sector_df):

    filename = sector_name.replace(" ", "_") + ".pdf"

    pdf_path = REPORT_FOLDER / filename

    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=(8.27 * inch, 11.69 * inch)
    )

    story = []

    # -------------------------------------------------
    # Title
    # -------------------------------------------------

    story.append(
        Paragraph(
            f"<b>{sector_name} Sector Report</b>",
            TITLE
        )
    )

    story.append(Spacer(1, 0.30 * inch))

    # -------------------------------------------------
    # Summary Statistics
    # -------------------------------------------------

    total_companies = len(sector_df)

    avg_roe = sector_df["return_on_equity_pct"].mean()

    avg_npm = sector_df["net_profit_margin_pct"].mean()

    avg_de = sector_df["debt_to_equity"].mean()

    summary = [
        ["Metric", "Value"],
        ["Total Companies", str(total_companies)],
        ["Average ROE (%)", f"{avg_roe:.2f}"],
        ["Average Net Profit Margin (%)", f"{avg_npm:.2f}"],
        ["Average Debt / Equity", f"{avg_de:.2f}"],
    ]

    table = Table(summary, colWidths=[3.5 * inch, 2 * inch])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
    ]))

    story.append(table)

    story.append(Spacer(1, 0.35 * inch))

        # -------------------------------------------------
    # Company List
    # -------------------------------------------------

    story.append(
        Paragraph(
            "<b>Companies in this Sector</b>",
            HEADING
        )
    )

    story.append(Spacer(1, 0.15 * inch))

    company_table = [
        [
            "Company",
            "ROE",
            "NPM",
            "Debt/Equity"
        ]
    ]

    for _, row in sector_df.iterrows():

        company_table.append([
            str(row["company_id"]),
            f"{row['return_on_equity_pct']:.2f}",
            f"{row['net_profit_margin_pct']:.2f}",
            f"{row['debt_to_equity']:.2f}",
        ])

    table = Table(
        company_table,
        colWidths=[
            2.8 * inch,
            1.1 * inch,
            1.3 * inch,
            1.3 * inch
        ]
    )

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.green),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
    ]))

    story.append(table)

    doc.build(story)

    print(f"✓ Generated {filename}")


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    companies, ratios, sectors = load_data()

    print("=" * 60)
    print("Sector Report Generator")
    print("=" * 60)

    latest = latest_ratios(ratios)

    # Merge latest financial ratios with sector mapping
    sector_data = latest.merge(
        sectors,
        on="company_id",
        how="left"
    )

    print(f"Companies Loaded        : {len(companies)}")
    print(f"Latest Ratio Records    : {len(latest)}")
    print(f"Sector Mapping Records  : {len(sectors)}")

    sector_list = sorted(
        sector_data["broad_sector"]
        .dropna()
        .unique()
    )

    print(f"\nGenerating {len(sector_list)} Sector Reports...\n")

    for sector in sector_list:

        sector_df = (
            sector_data[
                sector_data["broad_sector"] == sector
            ]
            .sort_values("company_id")
            .reset_index(drop=True)
        )

        generate_sector_pdf(
            sector_name=sector,
            sector_df=sector_df
        )

    print("\n" + "=" * 60)
    print("✓ All Sector Reports Generated Successfully")
    print(f"Location : {REPORT_FOLDER}")
    print("=" * 60)


if __name__ == "__main__":
    main()