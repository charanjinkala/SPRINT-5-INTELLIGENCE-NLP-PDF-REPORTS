"""
Sprint 5
Portfolio Summary Report
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

REPORT_FOLDER = PROJECT_ROOT / "reports"

COMPANIES_FILE = RAW / "companies.xlsx"
RATIOS_FILE = RAW / "financial_ratios.xlsx"
SECTORS_FILE = RAW / "sectors.xlsx"

REPORT_FILE = REPORT_FOLDER / "portfolio_summary.pdf"

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

    companies = pd.read_excel(
        COMPANIES_FILE,
        header=1
    )

    companies.columns = companies.columns.str.strip()

    ratios = pd.read_excel(RATIOS_FILE)

    sectors = pd.read_excel(SECTORS_FILE)

    return companies, ratios, sectors


def latest_ratios(df):

    return (
        df.sort_values("year")
          .groupby("company_id")
          .tail(1)
    )


# ---------------------------------------------------------
# Generate Portfolio Summary PDF
# ---------------------------------------------------------

def generate_portfolio_pdf(companies, latest, sectors):

    print("Inside generate_portfolio_pdf()")

    doc = SimpleDocTemplate(
        str(REPORT_FILE),
        pagesize=(8.27 * inch, 11.69 * inch)
    )

    story = []

    # -------------------------------------------------
    # Title
    # -------------------------------------------------

    story.append(
        Paragraph(
            "<b>NIFTY 100 PORTFOLIO SUMMARY REPORT</b>",
            TITLE
        )
    )

    story.append(Spacer(1, 0.30 * inch))

    # -------------------------------------------------
    # Portfolio Statistics
    # -------------------------------------------------

    total_companies = len(companies)

    total_sectors = sectors["broad_sector"].nunique()

    avg_roe = latest["return_on_equity_pct"].mean()

    avg_npm = latest["net_profit_margin_pct"].mean()

    avg_de = latest["debt_to_equity"].mean()

    avg_interest = latest["interest_coverage"].mean()

    summary = [
        ["Metric", "Value"],
        ["Total Companies", str(total_companies)],
        ["Total Sectors", str(total_sectors)],
        ["Average ROE (%)", f"{avg_roe:.2f}"],
        ["Average Net Profit Margin (%)", f"{avg_npm:.2f}"],
        ["Average Debt / Equity", f"{avg_de:.2f}"],
        ["Average Interest Coverage", f"{avg_interest:.2f}"],
    ]

    table = Table(
        summary,
        colWidths=[3.8 * inch, 2.0 * inch]
    )

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
    ]))

    story.append(table)

    story.append(Spacer(1, 0.40 * inch))

        # -------------------------------------------------
    # Sector Distribution
    # -------------------------------------------------

    story.append(
        Paragraph(
            "<b>Sector Distribution</b>",
            HEADING
        )
    )

    story.append(Spacer(1, 0.15 * inch))

    sector_counts = (
        sectors.groupby("broad_sector")
        .size()
        .reset_index(name="Companies")
        .sort_values("Companies", ascending=False)
    )

    sector_table = [["Sector", "Companies"]]

    for _, row in sector_counts.iterrows():

        sector_table.append([
            row["broad_sector"],
            str(row["Companies"])
        ])

    table = Table(
        sector_table,
        colWidths=[4.5 * inch, 1.5 * inch]
    )

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.green),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
    ]))

    story.append(table)

    story.append(Spacer(1, 0.35 * inch))

        # -------------------------------------------------
    # Top 10 Companies by ROE
    # -------------------------------------------------

    story.append(
        Paragraph(
            "<b>Top 10 Companies by Return on Equity (ROE)</b>",
            HEADING
        )
    )

    story.append(Spacer(1, 0.15 * inch))

    top_roe = (
        latest.sort_values(
            "return_on_equity_pct",
            ascending=False
        )
        .head(10)
    )

    roe_table = [
        [
            "Company",
            "ROE (%)",
            "Net Profit Margin (%)"
        ]
    ]

    for _, row in top_roe.iterrows():

        roe_table.append([
            row["company_id"],
            f"{row['return_on_equity_pct']:.2f}",
            f"{row['net_profit_margin_pct']:.2f}"
        ])

    table = Table(
        roe_table,
        colWidths=[3.2 * inch, 1.3 * inch, 2.0 * inch]
    )

    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.darkred),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.5, colors.black),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("BACKGROUND", (0,1), (-1,-1), colors.beige),
        ("ALIGN", (1,1), (-1,-1), "CENTER"),
    ]))

    story.append(table)

    story.append(Spacer(1,0.35*inch))

        # -------------------------------------------------
    # Portfolio Insights
    # -------------------------------------------------

    story.append(
        Paragraph(
            "<b>Portfolio Insights</b>",
            HEADING
        )
    )

    story.append(Spacer(1,0.15*inch))

    insights = f"""
    <b>Total Companies:</b> {total_companies}<br/><br/>

    <b>Total Sectors:</b> {total_sectors}<br/><br/>

    <b>Average ROE:</b> {avg_roe:.2f}%<br/><br/>

    <b>Average Net Profit Margin:</b> {avg_npm:.2f}%<br/><br/>

    <b>Average Debt to Equity:</b> {avg_de:.2f}<br/><br/>

    This report summarizes the latest financial performance
    of companies in the portfolio based on the available
    financial ratios and sector classifications.
    """

    story.append(
        Paragraph(
            insights,
            BODY
        )
    )

    print("Building PDF...")
    print(REPORT_FILE)

    doc.build(story)

    print(f"✓ Portfolio Summary saved to\n{REPORT_FILE}")

def main():

    companies, ratios, sectors = load_data()

    latest = latest_ratios(ratios)

    print("="*60)
    print("Generating Portfolio Summary Report")
    print("="*60)

    generate_portfolio_pdf(
        companies,
        latest,
        sectors
    )

    print("="*60)
    print("✓ Portfolio Summary Report Generated Successfully")
    print("="*60)


if __name__ == "__main__":
    main()