"""
Sprint 5
Company Tearsheet Generator
"""

from pathlib import Path

import pandas as pd

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)

from reportlab.lib import colors
from reportlab.lib.units import inch

# ---------------------------------------------------------
# Project Paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW = PROJECT_ROOT / "data" / "raw"
OUTPUT = PROJECT_ROOT / "output"

COMPANIES_FILE = RAW / "companies.xlsx"
RATIOS_FILE = RAW / "financial_ratios.xlsx"
PROFIT_FILE = RAW / "profitandloss.xlsx"

ANALYSIS_FILE = OUTPUT / "analysis_parsed.csv"
PROS_FILE = OUTPUT / "pros_cons_generated.csv"
CASHFLOW_FILE = OUTPUT / "cashflow_intelligence.xlsx"

REPORT_FOLDER = PROJECT_ROOT / "reports" / "tearsheets"

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

    companies = pd.read_excel(
        COMPANIES_FILE,
        header=1
    )

    companies.columns = companies.columns.str.strip()

    ratios = pd.read_excel(
        RATIOS_FILE
    )

    profit = pd.read_excel(
        PROFIT_FILE,
        header=1
    )

    analysis = pd.read_csv(
        ANALYSIS_FILE
    )

    pros = pd.read_csv(
        PROS_FILE
    )

    cashflow = pd.read_excel(
        CASHFLOW_FILE
    )

    return (
        companies,
        ratios,
        profit,
        analysis,
        pros,
        cashflow
    )

# ---------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------

def latest(df):

    if df.empty:
        return None

    if "year" in df.columns:
        df = df.sort_values("year")

    return df.iloc[-1]


def company_ratios(
    ratios,
    company_id
):

    return latest(
        ratios[
            ratios["company_id"] == company_id
        ]
    )


def company_analysis(
    analysis,
    company_id
):

    return analysis[
        analysis["company_id"] == company_id
    ]


def company_pros(
    pros,
    company_id
):

    return latest(
        pros[
            pros["company_id"] == company_id
        ]
    )


def company_cashflow(
    cashflow,
    company_id
):

    return latest(
        cashflow[
            cashflow["company_id"] == company_id
        ]
    )

# ---------------------------------------------------------
# Generate Company PDF
# ---------------------------------------------------------

def generate_company_pdf(
    company,
    ratios,
    analysis,
    pros,
    cashflow
):

    company_id = company["id"]

    ratio = company_ratios(
        ratios,
        company_id
    )

    analysis_data = company_analysis(
        analysis,
        company_id
    )

    pros_data = company_pros(
        pros,
        company_id
    )

    cashflow_data = company_cashflow(
        cashflow,
        company_id
    )

    pdf_file = REPORT_FOLDER / f"{company_id}.pdf"

    doc = SimpleDocTemplate(str(pdf_file))

    story = []

    # -------------------------------------------------
    # Company Details
    # -------------------------------------------------

    story.append(
        Paragraph(
            company["company_name"],
            TITLE
        )
    )

    story.append(Spacer(1, 12))

    story.append(
        Paragraph(
            f"<b>Company ID :</b> {company_id}",
            BODY
        )
    )

    story.append(
        Paragraph(
            f"<b>Website :</b> {company['website']}",
            BODY
        )
    )

    story.append(
        Paragraph(
            f"<b>Book Value :</b> {company['book_value']}",
            BODY
        )
    )

    story.append(
        Paragraph(
            f"<b>ROCE :</b> {company['roce_percentage']} %",
            BODY
        )
    )

    story.append(
        Paragraph(
            f"<b>ROE :</b> {company['roe_percentage']} %",
            BODY
        )
    )

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "<b>About Company</b>",
            HEADING
        )
    )

    story.append(
        Paragraph(
            str(company["about_company"]),
            BODY
        )
    )

    story.append(Spacer(1, 20))

    # -------------------------------------------------
    # Financial Ratios
    # -------------------------------------------------

    story.append(
        Paragraph(
            "<b>Latest Financial Ratios</b>",
            HEADING
        )
    )

    if ratio is not None:

        ratio_table = [

            ["Metric", "Value"],

            ["Net Profit Margin (%)",
            f"{ratio['net_profit_margin_pct']:.2f}"],

            ["Operating Margin (%)",
            f"{ratio['operating_profit_margin_pct']:.2f}"],

            ["Return on Equity (%)",
            f"{ratio['return_on_equity_pct']:.2f}"],

            ["Debt to Equity",
            f"{ratio['debt_to_equity']:.2f}"],

            ["Interest Coverage",
            f"{ratio['interest_coverage']:.2f}"],

            ["Asset Turnover",
            f"{ratio['asset_turnover']:.2f}"]

        ]

        table = Table(
            ratio_table,
            colWidths=[4*inch,2*inch]
        )

        table.setStyle(

            TableStyle([

                ("BACKGROUND",(0,0),(-1,0),colors.darkblue),

                ("TEXTCOLOR",(0,0),(-1,0),colors.white),

                ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

                ("ALIGN",(0,0),(-1,-1),"CENTER"),

                ("GRID",(0,0),(-1,-1),0.5,colors.black),

                ("BACKGROUND",(0,1),(-1,-1),colors.beige),

                ("BOTTOMPADDING",(0,0),(-1,0),8)

            ])

        )

        story.append(table)

    else:

        story.append(
            Paragraph(
                "Financial ratios not available.",
                BODY
            )
        )

    story.append(Spacer(1,15))


    story.append(PageBreak())
    # -------------------------------------------------
    # CAGR Analysis
    # -------------------------------------------------

    story.append(
        Paragraph(
            "<b>CAGR Analysis</b>",
            HEADING
        )
    )

    if not analysis_data.empty:

        cagr_table = [["Metric", "Years", "Growth %"]]

        for _, row in analysis_data.iterrows():

            cagr_table.append([
                str(row["metric_type"]),
                str(row["period_years"]),
                f"{row['value_pct']:.2f}%"
            ])

        table = Table(
            cagr_table,
            colWidths=[3*inch,1*inch,2*inch]
        )

        table.setStyle(

            TableStyle([

                ("BACKGROUND",(0,0),(-1,0),colors.darkgreen),

                ("TEXTCOLOR",(0,0),(-1,0),colors.white),

                ("GRID",(0,0),(-1,-1),0.5,colors.black),

                ("BACKGROUND",(0,1),(-1,-1),colors.whitesmoke),

                ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

                ("ALIGN",(0,0),(-1,-1),"CENTER")

            ])

        )

        story.append(table)

    else:

        story.append(
            Paragraph(
                "No CAGR data available.",
                BODY
            )
        )

    story.append(Spacer(1,15))
    # -------------------------------------------------
    # Pros & Cons
    # -------------------------------------------------

    story.append(
        Paragraph(
            "<b>Pros & Cons</b>",
            HEADING
        )
    )

    if pros_data is not None:

        pros_text = str(pros_data["pros"]).replace("|", "<br/>• ")
        cons_text = str(pros_data["cons"]).replace("|", "<br/>• ")

        pros_cons_table = [

            [
                Paragraph("<b>Pros</b>", BODY),
                Paragraph("<b>Cons</b>", BODY)
            ],

            [
                Paragraph("• " + pros_text, BODY),
                Paragraph("• " + cons_text, BODY)
            ]

        ]

        table = Table(
            pros_cons_table,
            colWidths=[3.2*inch,3.2*inch]
        )

        table.setStyle(

            TableStyle([

                ("BACKGROUND",(0,0),(-1,0),colors.green),

                ("TEXTCOLOR",(0,0),(-1,0),colors.white),

                ("GRID",(0,0),(-1,-1),0.5,colors.black),

                ("BACKGROUND",(0,1),(0,1),colors.lightgreen),

                ("BACKGROUND",(1,1),(1,1),colors.pink),

                ("VALIGN",(0,0),(-1,-1),"TOP"),

                ("BOTTOMPADDING",(0,0),(-1,0),8)

            ])

        )

        story.append(table)

    else:

        story.append(
            Paragraph(
                "Pros & Cons not available.",
                BODY
            )
        )

    story.append(Spacer(1,15))
    # -------------------------------------------------
    # Cash Flow Intelligence
    # -------------------------------------------------

    story.append(
        Paragraph(
            "<b>Cash Flow Intelligence</b>",
            HEADING
        )
    )

    if cashflow_data is not None:

        cash_table = [

            ["Metric","Value"],

            ["Free Cash Flow",
            str(cashflow_data.get("free_cash_flow","-"))],

            ["CFO / PAT Ratio",
            str(cashflow_data.get("cfo_pat_ratio","-"))],

            ["CFO Quality",
            str(cashflow_data.get("cfo_quality","-"))],

            ["CapEx Intensity %",
            str(cashflow_data.get("capex_intensity_pct","-"))],

            ["CapEx Type",
            str(cashflow_data.get("capex_type","-"))],

            ["FCF Conversion %",
            str(cashflow_data.get("fcf_conversion_pct","-"))],

            ["Capital Allocation",
            str(cashflow_data.get("capital_allocation","-"))],

            ["Distress Flag",
            str(cashflow_data.get("distress_flag","-"))]

        ]

        table = Table(
            cash_table,
            colWidths=[3.8*inch,2.2*inch]
        )

        table.setStyle(

            TableStyle([

                ("BACKGROUND",(0,0),(-1,0),colors.darkred),

                ("TEXTCOLOR",(0,0),(-1,0),colors.white),

                ("GRID",(0,0),(-1,-1),0.5,colors.black),

                ("BACKGROUND",(0,1),(-1,-1),colors.beige),

                ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

                ("ALIGN",(0,0),(-1,-1),"CENTER")

            ])

        )

        story.append(table)

    else:

        story.append(
            Paragraph(
                "Cash Flow data not available.",
                BODY
            )
        )

    story.append(Spacer(1,20))


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():

    (
        companies,
        ratios,
        profit,
        analysis,
        pros,
        cashflow
    ) = load_data()

    total = len(companies)

    print("=" * 60)
    print(f"Generating {total} Company Tearsheets")
    print("=" * 60)

    for index, (_, company) in enumerate(companies.iterrows(), start=1):

        print(f"[{index}/{total}] {company['company_name']}")

        generate_company_pdf(
            company,
            ratios,
            analysis,
            pros,
            cashflow
        )

    print("=" * 60)
    print("✓ All Company Tearsheets Generated Successfully")
    print("=" * 60)


if __name__ == "__main__":
    main()