"""Demo risk engine placeholder for ripple-effect scoring."""

from __future__ import annotations


def calculate_risk_score(disruption_severity: float, dependency_weight: float) -> float:
    """Return a simple illustrative risk score.

    Value is intentionally simple and meant for demonstration only.
    """
    if not 0.0 <= disruption_severity <= 1.0:
        raise ValueError("disruption_severity must be between 0.0 and 1.0")
    if not 0.0 <= dependency_weight <= 1.0:
        raise ValueError("dependency_weight must be between 0.0 and 1.0")
    return round(disruption_severity * dependency_weight, 3)


if __name__ == "__main__":
    score = calculate_risk_score(0.9, 0.7)
    print(f"Illustrative risk score: {score}")
