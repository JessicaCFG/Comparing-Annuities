# 📊 Annuity Comparison Tool

A Python command-line tool for comparing **Fixed**, **MYGA**, and **Fixed Indexed Annuity (FIA)** products side by side — built for financial professionals.

Built by [CAER Financial Group](https://caerfinancialgroup.com) | Faith · Family · Financial Freedom

---

## Features

- **Side-by-side summary** comparing any number of annuity products
- **Year-by-year projection** with interest, fees, surrender values, and income benefit base
- **FIA modeling** with participation rate, cap rate, and floor rate
- **Income rider tracking** with compounding benefit base roll-up
- **CSV export** for use in Excel or Google Sheets
- **JSON config files** for saving and reusing client scenarios
- Surrender charge schedules with automatic lookups per year

---

## Installation

```bash
git clone https://github.com/JessicaCFG/annuity-comparator.git
cd annuity-comparator
pip install tabulate
```

---

## Usage

### Run the built-in demo (Fixed vs. MYGA vs. FIA)
```bash
python annuity_comparator.py
```

### Run with a custom scenario file
```bash
python annuity_comparator.py --config example_scenario.json
```

### Set owner's current age
```bash
python annuity_comparator.py --age 62
```

### Show year-by-year detail for a specific product
```bash
python annuity_comparator.py --detail "MYGA – Athene"
```

### Export all projections to CSV
```bash
python annuity_comparator.py --export results.csv
```

### Combine options
```bash
python annuity_comparator.py --config example_scenario.json --age 58 --export client_report.csv
```

---

## JSON Config Format

Create your own scenario files to save client-specific comparisons:

```json
{
  "owner_age": 60,
  "products": [
    {
      "name": "MYGA – Athene 5-Year",
      "annuity_type": "MYGA",
      "premium": 100000,
      "term_years": 5,
      "interest_rate": 0.055,
      "annual_fee": 0.0,
      "surrender_schedule": [0.09, 0.08, 0.07, 0.06, 0.05],
      "carrier": "Athene Annuity",
      "am_best_rating": "A"
    }
  ]
}
```

**Supported `annuity_type` values:** `"Fixed"`, `"MYGA"`, `"FIA"`

**FIA-specific fields:**
| Field | Description | Example |
|---|---|---|
| `participation_rate` | % of index gain credited | `0.85` (85%) |
| `cap_rate` | Maximum annual credit | `0.10` (10%) |
| `floor_rate` | Minimum annual credit | `0.0` (0%, no loss) |
| `income_rider_rate` | Annual benefit base roll-up | `0.07` (7%) |

---

## Example Output

```
════════════════════════════════════════════════════════════
  CAER FINANCIAL GROUP  |  Annuity Comparison Report
════════════════════════════════════════════════════════════
  Client Age: 60

╭──────────────────────────────┬──────┬──────────┬─────────╮
│ Product                      │ Type │ Premium  │ End Val │
├──────────────────────────────┼──────┼──────────┼─────────┤
│ Fixed Annuity – Carrier A    │Fixed │ $100,000 │$136,857 │
│ MYGA – Athene                │ MYGA │ $100,000 │$130,696 │
│ FIA w/ Income Rider – AmNat  │  FIA │ $100,000 │$195,423 │
╰──────────────────────────────┴──────┴──────────┴─────────╯
```

---

## Disclaimer

> Projections are illustrations only and are not a guarantee of future performance. For personalized guidance, contact CAER Financial Group.

---

## License

MIT License — free to use, fork, and build on.
