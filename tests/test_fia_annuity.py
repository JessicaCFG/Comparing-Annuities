"""Unit tests for FIA Annuity calculations."""

import unittest
from annuity_comparator import FIAAnnuity


class TestFIAAnnuity(unittest.TestCase):
    """Test cases for FIAAnnuity class."""

    def setUp(self):
        """Set up test fixtures."""
        self.config = {
            "name": "Test FIA",
            "annuity_type": "FIA",
            "premium": 100000,
            "term_years": 10,
            "participation_rate": 0.85,
            "cap_rate": 0.10,
            "floor_rate": 0.0,
            "annual_fee": 0.01,
            "income_rider_rate": 0.07,
            "market_return_rate": 0.07,
            "surrender_schedule": [0.10] * 10,
            "carrier": "Test Carrier",
            "am_best_rating": "A",
        }

    def test_initialization(self):
        """Test FIA initialization."""
        product = FIAAnnuity(self.config)
        self.assertEqual(product.name, "Test FIA")
        self.assertEqual(product.participation_rate, 0.85)
        self.assertEqual(product.cap_rate, 0.10)

    def test_calculate_projection(self):
        """Test FIA projection calculation."""
        product = FIAAnnuity(self.config)
        projection = product.calculate_projection()

        # Should have 10 years of projections
        self.assertEqual(len(projection), 10)

        # Each year should have income base
        for year in projection:
            self.assertGreater(year["income_base"], self.config["premium"])

    def test_participation_rate(self):
        """Test participation rate application."""
        product = FIAAnnuity(self.config)
        projection = product.calculate_projection()

        # First year credited rate should be capped
        credited = projection[0]["credited_rate"]
        expected_max = min(0.07 * 0.85, 0.10)  # 5.95% capped at 10%
        self.assertLessEqual(credited, self.config["cap_rate"])

    def test_floor_rate(self):
        """Test floor rate protection."""
        config = self.config.copy()
        config["floor_rate"] = 0.0
        config["market_return_rate"] = -0.05  # Negative market return

        product = FIAAnnuity(config)
        projection = product.calculate_projection()

        # Credited rate should be at floor
        for year in projection:
            self.assertGreaterEqual(year["credited_rate"], config["floor_rate"])

    def test_income_rider_rollup(self):
        """Test income benefit base roll-up."""
        product = FIAAnnuity(self.config)
        projection = product.calculate_projection()

        # Income base should grow each year
        prev_income_base = self.config["premium"]
        for year in projection:
            current_income_base = year["income_base"]
            self.assertGreater(current_income_base, prev_income_base)
            prev_income_base = current_income_base


if __name__ == "__main__":
    unittest.main()
