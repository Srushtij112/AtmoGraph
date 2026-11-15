# Neo4j Graph Schema Documentation

## 1. Purpose

This document describes the initial Neo4j graph schema
developed for the AtmoGraph supply-chain project.

The graph represents the relationships between suppliers,
ports and factories.

## 2. Node Types

### Supplier
Represents a company that supplies materials or components.

Unique identifier:
- supplier_id

### Port
Represents a shipping or transportation port.

Unique identifier:
- port_id

### Factory
Represents a manufacturing facility.

Unique identifier:
- factory_id

## 3. Uniqueness Constraints

The following constraints have been created in Neo4j:

| Node Label | Unique Property |
|------------|-----------------|
| Supplier   | supplier_id     |
| Port       | port_id         |
| Factory    | factory_id      |

These constraints prevent duplicate values for the
respective identifier properties.

## 4. Implementation

The schema is maintained in:

- cypher/schema.cypher

The Python execution script is:

- src/create_schema.py

The Python script reads the Cypher commands and executes
them against the configured Neo4j database.

## 5. Verification

The following Cypher command verifies the constraints:

SHOW CONSTRAINTS;

The three expected constraints are:
- supplier_id_unique
- port_id_unique
- factory_id_unique

## 6. Next Development Steps

- Create sample supply-chain nodes.
- Define relationships between graph entities.
- Obtain the cleaned supply-chain CSV dataset.
- Map dataset columns to graph node properties.
- Implement CSV-to-Neo4j ingestion.

Relationship types and final property mappings will be
confirmed with the team before implementation.