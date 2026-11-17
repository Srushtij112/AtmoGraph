"""Simple tests for dummy risk engine functionality."""

import unittest

from risk_engine_demo import calculate_risk_score


class RiskEngineDemoTests(unittest.TestCase):
    def test_calculates_score(self):
        self.assertEqual(calculate_risk_score(0.8, 0.5), 0.4)

    def test_rejects_invalid_severity(self):
        with self.assertRaises(ValueError):
            calculate_risk_score(1.5, 0.5)

    def test_rejects_invalid_dependency(self):
        with self.assertRaises(ValueError):
            calculate_risk_score(0.8, 1.5)


if __name__ == "__main__":
    unittest.main()
