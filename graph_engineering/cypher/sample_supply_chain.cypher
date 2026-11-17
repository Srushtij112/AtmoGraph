// Illustrative demo fixture only; all names and values are fictional.
// Run against a disposable Neo4j database, not production data.

MERGE (steel:Supplier {id: 'demo_steel', name: 'Demo Steel Supplier'})
MERGE (factory:Factory {id: 'demo_factory', name: 'Demo Factory'})
MERGE (retailer:Retailer {id: 'demo_retailer', name: 'Demo Retailer'})

MERGE (steel)-[:SUPPLIES {dependency: 0.8}]->(factory)
MERGE (factory)-[:SUPPLIES {dependency: 0.6}]->(retailer);

// Example read-only inspection of the fictional chain:
MATCH (supplier:Supplier {id: 'demo_steel'})-[:SUPPLIES*1..3]->(downstream)
RETURN supplier.name AS source, downstream.name AS downstream_entity;
