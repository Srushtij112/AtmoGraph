"""Small, dependency-free demo for supply-chain ripple scoring.

This module uses in-memory sample records only. It does not connect to Neo4j
or load real supply-chain data.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class SupplierLink:
    supplier: str
    customer: str
    dependency: float  # 0.0 (none) to 1.0 (fully dependent)


SAMPLE_LINKS = (
    SupplierLink("demo_steel", "demo_factory", 0.8),
    SupplierLink("demo_factory", "demo_retailer", 0.6),
)


def estimate_downstream_risk(
    links: tuple[SupplierLink, ...], disrupted_supplier: str, initial_risk: float
) -> dict[str, float]:
    """Return illustrative risk scores propagated along sample supplier links."""
    if not 0.0 <= initial_risk <= 1.0:
        raise ValueError("initial_risk must be between 0.0 and 1.0")

    risk_by_entity = {disrupted_supplier: initial_risk}
    changed = True
    while changed:
        changed = False
        for link in links:
            source_risk = risk_by_entity.get(link.supplier, 0.0)
            propagated_risk = source_risk * link.dependency
            if propagated_risk > risk_by_entity.get(link.customer, 0.0):
                risk_by_entity[link.customer] = propagated_risk
                changed = True
    return risk_by_entity


if __name__ == "__main__":
    scores = estimate_downstream_risk(SAMPLE_LINKS, "demo_steel", 1.0)
    for entity, score in sorted(scores.items()):
        print(f"{entity}: illustrative risk={score:.2f}")
