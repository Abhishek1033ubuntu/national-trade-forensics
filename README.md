# National Trade Forensics Pipeline

> **Note**: This repository provides a **tested and validated forensic model** designed to help researchers, economists, and technical auditors investigate national trade data for anomalies, tariff code misclassifications, and potential trade misinvoicing (under-invoicing / over-invoicing).

The pipeline operates on line-item trade statistics using dual statistical techniques:
1. **Median Absolute Deviation ($Z_{\text{MAD}}$)** on unit values ($\text{USD}/\text{kg}$) to detect non-Gaussian price outliers without parametric distribution assumptions.
2. **Benford's Law Chi-Square ($\chi^2$) Goodness-of-Fit Test** on leading digits to identify aggregate data manipulation or reporting irregularities.

---

## Repository Structure

```text
national-trade-forensics/
├── README.md
├── requirements.txt
├── LICENSE
├── data/
│   └── sample_trade_data.csv       # Standardized line-item trade schema
├── src/
│   ├── __init__.py
│   ├── ingestion.py                 # Flexible CSV/JSON data loader
│   ├── forensic_engine.py           # MAD Z-Score & Benford Chi-Square algorithms
│   └── visualization.py            # Log-scale boxplots & digit distribution charts
├── notebooks/
│   └── National_Trade_Audit.ipynb  # Interactive demonstration notebook
└── reports/
    └── .gitkeep                     # Output target for generated reports

```

---

## Core Analytical Engine

### 1. Robust Unit Value Dispersion ($Z_{\text{MAD}}$)

Standard $Z$-scores rely on mean and standard deviation, which are skewed by massive trade values. The engine computes robust Z-scores using the median and Median Absolute Deviation ($\text{MAD}$):

$$\text{MAD} = \text{median}(|x_i - \tilde{x}|)$$

$$Z_{\text{MAD}} = \frac{x_i - \tilde{x}}{1.4826 \times \text{MAD}}$$

Records with $|Z_{\text{MAD}}| > 2.5$ within their respective HS commodity group are flagged as structural price anomalies.

### 2. Benford's Law Chi-Square Test ($\chi^2$)

First-digit frequencies $P(d) = \log_{10}\left(1 + \frac{1}{d}\right)$ are tested against observed leading digits:

$$\chi^2 = \sum_{d=1}^{9} \frac{(O_d - E_d)^2}{E_d}$$

A calculated statistic exceeding the $95\%$ confidence critical threshold ($\chi^2 > 15.507$, $df = 8$) indicates systemic deviation from naturally occurring numerical distributions.

---

## Quick Start

1. Clone or download this repository.
2. Install dependencies:
```bash
pip install -r requirements.txt

```


3. Place your national customs CSV dataset inside `data/` adhering to the standardized schema.
4. Execute the pipeline in Python or open `notebooks/National_Trade_Audit.ipynb` in Google Colab or Jupyter.

---

## Data Schema Requirements

Input datasets must contain the following core attributes:

| Column Name | Description | Example |
| --- | --- | --- |
| `cmd_code` | Harmonized System (HS) code (2/4/6-digit) | `847130` |
| `trade_value_usd` | Total transaction value in USD | `450000.00` |
| `net_weight_kg` | Net physical weight in kilograms | `12500.0` |
| `partner_country` | Trading partner territory | `USA` |

---

## License

Distributed under the MIT License. See `LICENSE` for details.

```

---
