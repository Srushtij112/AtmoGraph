"""Demo data-ingestion script for AtmoGraph.

This is intentionally lightweight and uses hard-coded sample records.
"""

from __future__ import annotations

SAMPLE_RAW_EVENTS = [
    {"supplier": "north_port", "country": "USA", "event": "storm_delay", "severity": 0.8},
    {"supplier": "east_factory", "country": "India", "event": "power_cut", "severity": 0.6},
    {"supplier": "south_warehouse", "country": "Brazil", "event": "strike", "severity": 0.7},
]


def load_sample_events() -> list[dict[str, object]]:
    """Return sample disruption events for mock pipeline testing."""
    return [event.copy() for event in SAMPLE_RAW_EVENTS]


if __name__ == "__main__":
    events = load_sample_events()
    print(f"Loaded {len(events)} sample disruption events")
    for event in events:
        print(event)
