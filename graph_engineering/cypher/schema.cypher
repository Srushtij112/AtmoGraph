CREATE CONSTRAINT supplier_id_unique IF NOT EXISTS
FOR (s:Supplier)
REQUIRE s.supplier_id IS UNIQUE;

CREATE CONSTRAINT port_id_unique IF NOT EXISTS
FOR (p:Port)
REQUIRE p.port_id IS UNIQUE;

CREATE CONSTRAINT factory_id_unique IF NOT EXISTS
FOR (f:Factory)
REQUIRE f.factory_id IS UNIQUE;