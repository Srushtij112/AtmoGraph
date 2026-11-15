import os
from pathlib import Path

from dotenv import load_dotenv
from neo4j import GraphDatabase


# Find the Graph Engineering folder
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Load database credentials
load_dotenv(PROJECT_ROOT / ".env")

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")
DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")

if not all([URI, USERNAME, PASSWORD]):
    raise ValueError("Neo4j credentials are missing from the .env file.")

# Locate the Cypher file
schema_file = PROJECT_ROOT / "cypher" / "schema.cypher"

# Read the Cypher commands
cypher_text = schema_file.read_text(encoding="utf-8")
queries = [q.strip() for q in cypher_text.split(";") if q.strip()]

# Connect and execute
driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)

try:
    driver.verify_connectivity()
    print("Successfully connected to Neo4j!")

    with driver.session(database=DATABASE) as session:
        for query in queries:
            session.run(query).consume()
            print("Executed:", query.splitlines()[0])

    print("Graph schema created successfully!")

finally:
    driver.close()
