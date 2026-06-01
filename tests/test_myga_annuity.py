"""Unit tests for MYGA Annuity calculations."""

import unittest
from annuity_comparator import MYGAAnnuity, FixedAnnuity


class TestMYGAAnnuity(unittest.TestCase):
    """Test cases for MYGAAnnuity class."""

    def setUp(self):
        """Set up test fixtures."""
        self.config = {
            "name": "Test MYGA",
            "annuity_type": "MYGA",
            "premium": 100000,
            "term_years": 5,
            "interest_rate": 0.055,
            "annual_fee": 0.0,
            "surrender_schedule": [0.09, 0.08, 0.07, 0.06, 0.05],
            "carrier": "Test Carrier",
            "am_best_rating": "A",
        }

    def test_initialization(self):
        """Test MYGA initialization."""
        product = MYGAAnnuity(self.config)
        self.assertEqual(product.name, "Test MYGA")
        self.assertEqual(product.premium, 100000)
        self.assertEqual(product.interest_rate, 0.055)

    def test_calculate_projection(self):
        """Test MYGA projection calculation."""
        product = MYGAAnnuity(self.config)
        projection = product.calculate_projection()

        # Should have 5 years of projections
        self.assertEqual(len(projection), 5)

        # Each year should show positive interest
        for year in projection:
            self.assertGreater(year["account_value"], 0)

    def test_higher_rate_than_fixed(self):
        """Test that MYGA with higher rate grows faster than Fixed."""
        myga_config = self.config.copy()
        fixed_config = self.config.copy()
        fixed_config["interest_rate"] = 0.045  # Lower than MYGA
        fixed_config["annuity_type"] = "Fixed"

        myga = MYGAAnnuity(myga_config)
        fixed = FixedAnnuity(fixed_config)

        myga_end = myga.get_end_value()
        fixed_end = fixed.get_end_value()

        self.assertGreater(myga_end, fixed_end)


if __name__ == "__main__":
    unittest.main()
