"""Basic unit tests for the illustrative sample risk propagation."""

import unittest

from sample_supply_chain import SAMPLE_LINKS, SupplierLink, estimate_downstream_risk


class EstimateDownstreamRiskTests(unittest.TestCase):
    def test_propagates_through_multiple_links(self):
        scores = estimate_downstream_risk(SAMPLE_LINKS, "demo_steel", 1.0)
        self.assertAlmostEqual(scores["demo_factory"], 0.8)
        self.assertAlmostEqual(scores["demo_retailer"], 0.48)

    def test_unknown_supplier_has_only_its_initial_score(self):
        self.assertEqual(estimate_downstream_risk(SAMPLE_LINKS, "unknown", 0.4), {"unknown": 0.4})

    def test_rejects_risk_outside_zero_to_one(self):
        with self.assertRaises(ValueError):
            estimate_downstream_risk(SAMPLE_LINKS, "demo_steel", 1.2)

    def test_empty_links(self):
        self.assertEqual(estimate_downstream_risk((), "demo_supplier", 0.5), {"demo_supplier": 0.5})


if __name__ == "__main__":
    unittest.main()
