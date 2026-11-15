CREATE CONSTRAINT supplier_id_unique IF NOT EXISTS
FOR (s:Supplier)
REQUIRE s.supplier_id IS UNIQUE;

CREATE CONSTRAINT port_id_unique IF NOT EXISTS
FOR (p:Port)
REQUIRE p.port_id IS UNIQUE;

CREATE CONSTRAINT factory_id_unique IF NOT EXISTS
FOR (f:Factory)
REQUIRE f.factory_id IS UNIQUE;

CREATE CONSTRAINT customer_id_unique IF NOT EXISTS
FOR (c:Customer)
REQUIRE c.customer_id IS UNIQUE;

CREATE CONSTRAINT order_id_unique IF NOT EXISTS
FOR (o:Order)
REQUIRE o.order_id IS UNIQUE;

CREATE CONSTRAINT order_item_id_unique IF NOT EXISTS
FOR (oi:OrderItem)
REQUIRE oi.order_item_id IS UNIQUE;

CREATE CONSTRAINT product_id_unique IF NOT EXISTS
FOR (p:Product)
REQUIRE p.product_id IS UNIQUE;