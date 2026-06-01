# 📊 Annuity Comparison Tool

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code style: PEP 8](https://img.shields.io/badge/Code%20style-PEP%208-blueviolet.svg)](https://pep8.org/)
[![Open Source](https://img.shields.io/badge/Open%20Source-%E2%9C%93-brightgreen.svg)](#license)

A Python command-line tool for comparing **Fixed**, **MYGA**, and **Fixed Indexed Annuity (FIA)** products side by side — built for financial professionals.

Built by [CAER Financial Group](https://caerfinancialgroup.com) | Faith · Family · Financial Freedom

**Tags:** `#annuity` `#financial-planning` `#retirement-planning` `#fixed-indexed-annuity` `#financial-advisor` `#investment-tool` `#python-cli` `#financial-calculator` `#wealth-management` `#insurance` `#MYGA` `#FIA` `#income-rider` `#fintech` `#open-source`

---

## 📑 Table of Contents

- [Quick Start](#quick-start)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Product Comparison](#product-comparison)
- [JSON Config Format](#json-config-format)
- [Example Output](#example-output)
- [Contributing](#contributing)
- [Support](#support)
- [Disclaimer](#disclaimer)
- [License](#license)

---

## 🚀 Quick Start

Get up and running in **3 steps**:

```bash
# 1. Clone the repository
git clone https://github.com/JessicaCFG/Comparing-Annuities.git
cd Comparing-Annuities

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the demo
python annuity_comparator.py
```

That's it! You'll see a side-by-side comparison of Fixed, MYGA, and FIA annuities.

---

## ✨ Features

- **Side-by-side summary** comparing any number of annuity products
- **Year-by-year projection** with interest, fees, surrender values, and income benefit base
- **FIA modeling** with participation rate, cap rate, and floor rate
- **Income rider tracking** with compounding benefit base roll-up
- **CSV export** for use in Excel or Google Sheets
- **JSON config files** for saving and reusing client scenarios
- **Surrender charge schedules** with automatic lookups per year
- **Multi-product comparison** — compare 2, 3, or unlimited products
- **Client-specific scenarios** — save and load custom configurations

---

## 📦 Installation

### Prerequisites
- **Python 3.8** or higher
- **pip** (Python package manager)

### Setup

```bash
git clone https://github.com/JessicaCFG/Comparing-Annuities.git
cd Comparing-Annuities
pip install -r requirements.txt
```

---

## 🎯 Usage

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

### View all available options
```bash
python annuity_comparator.py --help
```

---

## 📊 Product Comparison

| Feature | Fixed | MYGA | FIA |
|---------|-------|------|-----|
| **Guaranteed Growth** | ✅ | ✅ | ❌ |
| **Index Participation** | ❌ | ❌ | ✅ |
| **Upside Potential** | Low | Low | High |
| **Downside Protection** | Full | Full | Yes (Floor Rate) |
| **Income Rider** | Optional | Optional | Common |
| **Liquidity** | Limited | Limited | Limited |
| **Complexity** | Low | Low | High |

---

## 🔧 JSON Config Format

Create your own scenario files to save client-specific comparisons. See [`example_scenario.json`](example_scenario.json) for a complete example.

### Basic Structure

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

### Supported Annuity Types

**`annuity_type` values:** `"Fixed"`, `"MYGA"`, `"FIA"`

### FIA-Specific Fields

| Field | Description | Example | Default |
|-------|-------------|---------|---------|
| `participation_rate` | % of index gain credited | `0.85` (85%) | `0.80` |
| `cap_rate` | Maximum annual credit | `0.10` (10%) | `0.10` |
| `floor_rate` | Minimum annual credit | `0.0` (0%, no loss) | `0.0` |
| `income_rider_rate` | Annual benefit base roll-up | `0.07` (7%) | `0.06` |

### Complete Config Example

See [`example_scenario.json`](example_scenario.json) in the repository for a full working example.

---

## 📈 Example Output

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

## 🤝 Contributing

We welcome contributions from financial professionals, developers, and anyone interested in improving this tool!

### How to Contribute

1. **Fork** the repository
2. **Create a feature branch** (`git checkout -b feature/your-feature`)
3. **Make your changes** and test thoroughly
4. **Commit** with clear messages (`git commit -m 'Add your feature'`)
5. **Push** to your fork (`git push origin feature/your-feature`)
6. **Open a Pull Request** with a description of your changes

### Areas for Contribution

- 🐛 **Bug fixes** and improvements
- 📝 **Documentation** and examples
- ✨ **New annuity types** or modeling features
- 🧪 **Test coverage** and validation
- 🎨 **UI/UX enhancements**

Please see [`CONTRIBUTING.md`](CONTRIBUTING.md) for detailed guidelines.

---

## 💬 Support

### Getting Help

- **Documentation:** Review the JSON config format section above
- **Examples:** Check [`example_scenario.json`](example_scenario.json) for sample configurations
- **Issues:** [Open a GitHub Issue](https://github.com/JessicaCFG/Comparing-Annuities/issues) for bugs or feature requests

### Contact

For business inquiries or professional support, visit [CAER Financial Group](https://caerfinancialgroup.com)

---

## ⚠️ Disclaimer

> Projections are illustrations only and are not a guarantee of future performance. This tool is designed to assist in financial planning discussions and should not be construed as investment or financial advice. For personalized guidance, contact CAER Financial Group or a qualified financial professional.

---

## 📄 License

MIT License — free to use, fork, and build on.

See [`LICENSE`](LICENSE) for full details.

---

## 🙏 Acknowledgments

Built with ❤️ for financial advisors and their clients.

**[Back to Top](#-annuity-comparison-tool)**
