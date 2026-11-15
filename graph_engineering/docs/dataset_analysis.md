# DataCo Supply Chain Dataset Analysis

## 1. Dataset Overview

- Total records: 180,519
- Total columns: 53
- Unique orders: 65,752
- Unique products: 118
- Unique customers: 20,652
- Duplicate rows: 0

## 2. Delivery Analysis

| Delivery Status | Records |
|---|---:|
| Late delivery | 98,977 |
| Advance shipping | 41,592 |
| Shipping on time | 32,196 |
| Shipping canceled | 7,754 |

## 3. Shipping Mode Analysis

| Shipping Mode | Late Delivery Rate |
|---|---:|
| First Class | 95.32% |
| Second Class | 76.63% |
| Same Day | 45.74% |
| Standard Class | 38.07% |

## 4. Regional Analysis

Highest late-delivery rates:

- Central Africa: 60.15%
- Western Europe: 58.53%
- South of USA: 58.52%
- South Asia: 58.35%
- East Africa: 58.17%

## 5. Identifier Validation

- Every Order ID is present.
- Every Order Item ID is unique.
- Every Product ID maps to one product name.
- Every Product ID maps to one category.
- Every Order Item belongs to one Order.
- Every Order Item refers to one Product.
- Customer ID matches Order Customer ID.

## 6. Order-Level Validation

The following properties have one distinct value
per Order ID:

- Delivery Status
- Shipping Mode
- Actual shipping days
- Scheduled shipping days
- Shipping date
- Order Status
- Order Region
- Order Country
- Market
- Order date
- Customer ID

## 7. Customer Validation

- Unique customers: 20,652
- Maximum orders per customer: 15
- Maximum countries per customer: 1
- Customer segments per customer: 1
- Missing customer IDs: 0

## 8. Proposed Graph Model

(Customer)-[:PLACED]->(Order)
(Order)-[:CONTAINS]->(OrderItem)
(OrderItem)-[:REFERS_TO]->(Product)

## 9. Neo4j Schema

Seven uniqueness constraints are implemented:

- Supplier: supplier_id
- Port: port_id
- Factory: factory_id
- Customer: customer_id
- Order: order_id
- OrderItem: order_item_id
- Product: product_id

All seven constraints were verified using SHOW CONSTRAINTS.

## 10. Limitations

- DataCo does not directly provide Supplier-Port-Factory relationships.
- Delivery delays do not establish their real-world causes.
- Additional network and disruption-news data are required.
- Customer personal information is excluded from graph processing.