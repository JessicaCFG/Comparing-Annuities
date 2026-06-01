"""Unit tests for Fixed Annuity calculations."""

import unittest
from annuity_comparator import FixedAnnuity


class TestFixedAnnuity(unittest.TestCase):
    """Test cases for FixedAnnuity class."""

    def setUp(self):
        """Set up test fixtures."""
        self.config = {
            "name": "Test Fixed Annuity",
            "annuity_type": "Fixed",
            "premium": 100000,
            "term_years": 5,
            "interest_rate": 0.05,
            "annual_fee": 0.0,
            "surrender_schedule": [0.10, 0.08, 0.06, 0.04, 0.02],
            "carrier": "Test Carrier",
            "am_best_rating": "A",
        }

    def test_initialization(self):
        """Test product initialization."""
        product = FixedAnnuity(self.config)
        self.assertEqual(product.name, "Test Fixed Annuity")
        self.assertEqual(product.premium, 100000)
        self.assertEqual(product.interest_rate, 0.05)

    def test_calculate_projection(self):
        """Test year-by-year projection calculation."""
        product = FixedAnnuity(self.config)
        projection = product.calculate_projection()

        # Should have 5 years of projections
        self.assertEqual(len(projection), 5)

        # First year should have positive interest
        self.assertGreater(projection[0]["interest_earned"], 0)
        self.assertGreater(projection[0]["account_value"], product.premium)

    def test_end_value(self):
        """Test that end value is calculated correctly."""
        product = FixedAnnuity(self.config)
        end_value = product.get_end_value()

        # End value should be greater than premium due to interest
        self.assertGreater(end_value, product.premium)

    def test_no_fees(self):
        """Test calculation with no annual fees."""
        product = FixedAnnuity(self.config)
        projection = product.calculate_projection()

        # All fees should be zero
        for year in projection:
            self.assertEqual(year["fees"], 0.0)

    def test_with_fees(self):
        """Test calculation with annual fees."""
        config = self.config.copy()
        config["annual_fee"] = 0.01  # 1% annual fee

        product = FixedAnnuity(config)
        projection = product.calculate_projection()

        # All fees should be positive
        for year in projection:
            self.assertGreater(year["fees"], 0)

    def test_surrender_value(self):
        """Test surrender value calculation."""
        product = FixedAnnuity(self.config)
        projection = product.calculate_projection()

        # Surrender value should be less than account value due to charges
        for i, year in enumerate(projection):
            expected_charge_rate = self.config["surrender_schedule"][i]
            actual_charge_rate = year["surrender_charge_rate"]
            self.assertAlmostEqual(actual_charge_rate, expected_charge_rate)


if __name__ == "__main__":
    unittest.main()
