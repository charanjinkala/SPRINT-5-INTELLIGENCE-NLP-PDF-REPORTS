# 📊 Nifty 100 Financial Intelligence Platform

A Python-based financial analysis platform that automates the analysis of Nifty 100 companies by generating company tear sheets, sector reports, portfolio summaries, cash flow intelligence, and financial insights.

---

## 🚀 Features

- Parse financial analysis data
- Generate Pros & Cons using NLP
- Extract CAGR values from reports
- Cash Flow Intelligence Analysis
- Financial Distress Detection
- Company Tear Sheet PDFs
- Sector-wise Financial Reports
- Portfolio Summary Report
- Automated report generation

---

# 🛠 Technologies Used

- Python 3.x
- Pandas
- NumPy
- ReportLab
- OpenPyXL
- Matplotlib

---

# 📂 Project Structure

```
Nifty100_Financial_Intelligence_Platform/
│
├── data/
│   └── raw/
│       ├── companies.xlsx
│       ├── financial_ratios.xlsx
│       ├── sectors.xlsx
│       └── analysis.xlsx
│
├── output/
│   ├── analysis_parsed.csv
│   ├── pros_cons_generated.csv
│   ├── cashflow_intelligence.xlsx
│   └── distress_alerts.csv
│
├── reports/
│   ├── tearsheets/
│   │   ├── ABB.pdf
│   │   ├── INFY.pdf
│   │   └── ...
│   │
│   ├── sector/
│   │   ├── IT.pdf
│   │   ├── Banking.pdf
│   │   └── ...
│   │
│   └── portfolio_summary.pdf
│
├── src/
│   ├── nlp/
│   │   ├── parser.py
│   │   └── pros_cons_generator.py
│   │
│   └── reports/
│       ├── tearsheet.py
│       ├── sector_report.py
│       └── portfolio_summary.py
│
├── requirements.txt
└── README.md
```

---

# 📈 Generated Outputs

## Company Reports

- 92 Company Tear Sheet PDFs
- Financial Ratios
- Pros & Cons
- Cash Flow Analysis
- Key Metrics

---

## Sector Reports

- Sector Overview
- Average ROE
- Average Debt/Equity
- Top Companies
- Sector Statistics

---

## Portfolio Report

- Total Companies
- Sector Distribution
- Top ROE Companies
- Portfolio Statistics
- Financial Summary

---

## NLP Outputs

- Pros & Cons Extraction
- CAGR Parsing
- Structured Financial Data

---

## Cash Flow Intelligence

- CFO Quality
- CapEx Intensity
- Distress Flags
- Financial Health Indicators

---

# ▶️ How to Run

## Install dependencies

```bash
pip install -r requirements.txt
```

---

## Generate Company Tear Sheets

```bash
python src/reports/tearsheet.py
```

---

## Generate Sector Reports

```bash
python src/reports/sector_report.py
```

---

## Generate Portfolio Summary

```bash
python src/reports/portfolio_summary.py
```

---

## Generate NLP Outputs

```bash
python src/nlp/parser.py
python src/nlp/pros_cons_generator.py
```

---

# 📊 Outputs Generated

| Output | Status |
|----------|--------|
| Parsed Analysis | ✅ |
| Pros & Cons | ✅ |
| Cash Flow Intelligence | ✅ |
| Distress Alerts | ✅ |
| 92 Company Reports | ✅ |
| Sector Reports | ✅ |
| Portfolio Summary | ✅ |

---

# 🎯 Future Enhancements

- Streamlit Dashboard
- Interactive Charts
- Company Search
- PDF Export Improvements
- AI-based Investment Suggestions
- Real-time NSE/BSE Data Integration

---

# 👨‍💻 Author

Developed as a Financial Intelligence and Reporting Platform using Python.
