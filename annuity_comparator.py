"""
CAER Financial Group – Annuity Comparison Tool
================================================
Compare Fixed, MYGA, and Fixed Indexed Annuities (FIA) side by side.
Outputs a detailed projection table and summary report.

Usage:
    python annuity_comparator.py
    python annuity_comparator.py --config my_scenario.json
    python annuity_comparator.py --export results.csv
"""

import argparse
import csv
import json
import sys
from dataclasses import dataclass, field, asdict
from typing import Optional
from tabulate import tabulate  # pip install tabulate


# ─────────────────────────────────────────────
# Data Models
# ─────────────────────────────────────────────

@dataclass
class AnnuityProduct:
    """Represents a single annuity product for comparison."""
    name: str
    annuity_type: str           # "Fixed", "MYGA", or "FIA"
    premium: float              # Initial lump-sum premium
    term_years: int             # Surrender period / contract term
    interest_rate: float        # Annual rate (e.g. 0.05 for 5%)
    # FIA-specific
    participation_rate: float = 1.0   # e.g. 0.80 = 80%
    cap_rate: Optional[float] = None  # e.g. 0.10 = 10% cap
    floor_rate: float = 0.0           # e.g. 0.0 = 0% floor (no loss)
    # Fees
    annual_fee: float = 0.0           # Rider/admin fee as decimal (e.g. 0.01)
    # Surrender charges (list of rates by year, e.g. [0.09, 0.08, ...])
    surrender_schedule: list = field(default_factory=list)
    # Optional income rider
    income_rider_rate: float = 0.0    # Annual roll-up rate on benefit base
    # Carrier
    carrier: str = ""
    am_best_rating: str = ""


@dataclass
class ProjectionRow:
    year: int
    age: Optional[int]
    beginning_value: float
    interest_earned: float
    fees: float
    ending_value: float
    surrender_charge_pct: float
    surrender_value: float
    income_benefit_base: float


# ─────────────────────────────────────────────
# Projection Engine
# ─────────────────────────────────────────────

class AnnuityProjector:
    """Projects accumulation values for an annuity product year by year."""

    def __init__(self, product: AnnuityProduct, owner_age: Optional[int] = None):
        self.p = product
        self.owner_age = owner_age

    def _get_surrender_charge(self, year: int) -> float:
        """Return the surrender charge rate for a given year (1-indexed)."""
        schedule = self.p.surrender_schedule
        if not schedule:
            return 0.0
        idx = year - 1
        return schedule[idx] if idx < len(schedule) else 0.0

    def _credited_rate(self, base_rate: float) -> float:
        """Apply FIA adjustments (participation, cap, floor) if applicable."""
        if self.p.annuity_type != "FIA":
            return base_rate
        credited = base_rate * self.p.participation_rate
        if self.p.cap_rate is not None:
            credited = min(credited, self.p.cap_rate)
        credited = max(credited, self.p.floor_rate)
        return credited

    def project(self, years: Optional[int] = None) -> list[ProjectionRow]:
        """Run a year-by-year projection. Defaults to the contract term."""
        term = years or self.p.term_years
        rows = []
        value = self.p.premium
        benefit_base = self.p.premium  # Income rider benefit base

        for yr in range(1, term + 1):
            age = (self.owner_age + yr - 1) if self.owner_age else None
            bov = value
            credited = self._credited_rate(self.p.interest_rate)
            interest = bov * credited
            fees = bov * self.p.annual_fee
            value = bov + interest - fees
            sc_pct = self._get_surrender_charge(yr)
            surrender_value = value * (1 - sc_pct)
            # Compound income rider benefit base
            benefit_base *= (1 + self.p.income_rider_rate)

            rows.append(ProjectionRow(
                year=yr,
                age=age,
                beginning_value=round(bov, 2),
                interest_earned=round(interest, 2),
                fees=round(fees, 2),
                ending_value=round(value, 2),
                surrender_charge_pct=sc_pct,
                surrender_value=round(surrender_value, 2),
                income_benefit_base=round(benefit_base, 2),
            ))

        return rows


# ─────────────────────────────────────────────
# Comparison Engine
# ─────────────────────────────────────────────

class AnnuityComparator:
    """Compares multiple annuity products and generates reports."""

    def __init__(self, products: list[AnnuityProduct], owner_age: Optional[int] = None):
        self.products = products
        self.owner_age = owner_age
        self.projectors = [AnnuityProjector(p, owner_age) for p in products]

    def run_all(self, years: Optional[int] = None) -> dict[str, list[ProjectionRow]]:
        return {
            p.name: proj.project(years)
            for p, proj in zip(self.products, self.projectors)
        }

    def summary_table(self, years: Optional[int] = None) -> str:
        """Returns a formatted side-by-side summary at end of term."""
        results = self.run_all(years)
        rows = []
        for name, projection in results.items():
            p = next(pr for pr in self.products if pr.name == name)
            final = projection[-1]
            total_interest = sum(r.interest_earned for r in projection)
            total_fees = sum(r.fees for r in projection)
            net_gain = final.ending_value - p.premium
            rows.append([
                name,
                p.annuity_type,
                p.carrier or "—",
                p.am_best_rating or "—",
                f"${p.premium:,.0f}",
                f"{p.interest_rate*100:.2f}%",
                f"{p.term_years} yrs",
                f"${final.ending_value:,.2f}",
                f"${final.surrender_value:,.2f}",
                f"${total_interest:,.2f}",
                f"${total_fees:,.2f}",
                f"${net_gain:,.2f}",
            ])

        headers = [
            "Product", "Type", "Carrier", "AM Best", "Premium",
            "Rate", "Term", "Ending Value", "Surrender Value",
            "Total Interest", "Total Fees", "Net Gain"
        ]
        return tabulate(rows, headers=headers, tablefmt="rounded_outline")

    def detail_table(self, product_name: str, years: Optional[int] = None) -> str:
        """Returns a year-by-year projection table for one product."""
        results = self.run_all(years)
        if product_name not in results:
            return f"Product '{product_name}' not found."
        rows = []
        for r in results[product_name]:
            rows.append([
                r.year,
                r.age or "—",
                f"${r.beginning_value:,.2f}",
                f"${r.interest_earned:,.2f}",
                f"${r.fees:,.2f}",
                f"${r.ending_value:,.2f}",
                f"{r.surrender_charge_pct*100:.1f}%",
                f"${r.surrender_value:,.2f}",
                f"${r.income_benefit_base:,.2f}",
            ])
        headers = [
            "Year", "Age", "Beg. Value", "Interest", "Fees",
            "End Value", "Surr. Charge", "Surr. Value", "Inc. Benefit Base"
        ]
        title = f"\n  ── Detail Projection: {product_name} ──\n"
        return title + tabulate(rows, headers=headers, tablefmt="rounded_outline")

    def export_csv(self, filepath: str, years: Optional[int] = None):
        """Exports all product projections to a CSV file."""
        results = self.run_all(years)
        fieldnames = [
            "product", "year", "age", "beginning_value", "interest_earned",
            "fees", "ending_value", "surrender_charge_pct", "surrender_value",
            "income_benefit_base"
        ]
        with open(filepath, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for name, rows in results.items():
                for r in rows:
                    row_dict = asdict(r)
                    row_dict["product"] = name
                    writer.writerow(row_dict)
        print(f"\n✅  Exported projections to: {filepath}")


# ─────────────────────────────────────────────
# Default Demo Scenario
# ─────────────────────────────────────────────

def build_demo_products() -> list[AnnuityProduct]:
    """Three realistic demo products: Fixed, MYGA, and FIA."""
    fixed = AnnuityProduct(
        name="Fixed Annuity – Carrier A",
        annuity_type="Fixed",
        premium=100_000,
        term_years=7,
        interest_rate=0.045,
        annual_fee=0.0,
        surrender_schedule=[0.08, 0.07, 0.06, 0.05, 0.04, 0.03, 0.02],
        carrier="Carrier A",
        am_best_rating="A",
    )

    myga = AnnuityProduct(
        name="MYGA – Athene",
        annuity_type="MYGA",
        premium=100_000,
        term_years=5,
        interest_rate=0.055,
        annual_fee=0.0,
        surrender_schedule=[0.09, 0.08, 0.07, 0.06, 0.05],
        carrier="Athene Annuity",
        am_best_rating="A",
    )

    fia = AnnuityProduct(
        name="FIA w/ Income Rider – American National",
        annuity_type="FIA",
        premium=100_000,
        term_years=10,
        interest_rate=0.08,       # Index return assumption (before participation/cap)
        participation_rate=0.85,
        cap_rate=0.10,
        floor_rate=0.0,
        annual_fee=0.01,          # 1% income rider fee
        income_rider_rate=0.07,   # 7% roll-up on benefit base
        surrender_schedule=[0.10, 0.09, 0.08, 0.07, 0.06, 0.05, 0.04, 0.03, 0.02, 0.01],
        carrier="American National",
        am_best_rating="A",
    )

    return [fixed, myga, fia]


# ─────────────────────────────────────────────
# CLI Entry Point
# ─────────────────────────────────────────────

def load_config(path: str) -> tuple[list[AnnuityProduct], Optional[int]]:
    """Load products from a JSON config file."""
    with open(path) as f:
        data = json.load(f)
    owner_age = data.get("owner_age")
    products = [AnnuityProduct(**p) for p in data["products"]]
    return products, owner_age


def main():
    parser = argparse.ArgumentParser(
        description="CAER Financial Group – Annuity Comparison Tool"
    )
    parser.add_argument("--config", help="Path to JSON config file with product definitions.")
    parser.add_argument("--export", help="Export CSV to specified file path.")
    parser.add_argument("--years", type=int, help="Override projection term (years).")
    parser.add_argument("--age", type=int, help="Owner's current age for age tracking.")
    parser.add_argument("--detail", help="Show year-by-year detail for a named product.")
    args = parser.parse_args()

    # Load products
    if args.config:
        products, owner_age = load_config(args.config)
        if args.age:
            owner_age = args.age
    else:
        products = build_demo_products()
        owner_age = args.age or 60

    comparator = AnnuityComparator(products, owner_age=owner_age)

    print("\n" + "═" * 80)
    print("  CAER FINANCIAL GROUP  |  Annuity Comparison Report")
    print("═" * 80)
    if owner_age:
        print(f"  Client Age: {owner_age}")
    print()

    # Summary table
    print(comparator.summary_table(years=args.years))

    # Optional detail table
    if args.detail:
        print(comparator.detail_table(args.detail, years=args.years))
    else:
        # Default: show detail for first product
        print(comparator.detail_table(products[0].name, years=args.years))

    # Optional CSV export
    if args.export:
        comparator.export_csv(args.export, years=args.years)

    print("\n  ⚠️  Projections are illustrations only and not a guarantee of future performance.")
    print("  For personalized guidance, contact CAER Financial Group.\n")


if __name__ == "__main__":
    main()
