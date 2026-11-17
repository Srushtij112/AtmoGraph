"""Demo graph builder for illustrating supply-chain relationships."""

from __future__ import annotations

SAMPLE_GRAPH = {
    "nodes": [
        {"id": "port_01", "label": "Port"},
        {"id": "factory_01", "label": "Factory"},
        {"id": "warehouse_01", "label": "Warehouse"},
    ],
    "edges": [
        {"source": "port_01", "target": "factory_01", "type": "SHIP_TO"},
        {"source": "factory_01", "target": "warehouse_01", "type": "DELIVER_TO"},
    ],
}


def build_demo_graph() -> dict[str, list[dict[str, str]]]:
    """Return a toy graph structure used for documentation and demos."""
    return {
        "nodes": [node.copy() for node in SAMPLE_GRAPH["nodes"]],
        "edges": [edge.copy() for edge in SAMPLE_GRAPH["edges"]],
    }


if __name__ == "__main__":
    graph = build_demo_graph()
    print(f"Graph nodes: {len(graph['nodes'])}")
    print(f"Graph edges: {len(graph['edges'])}")
