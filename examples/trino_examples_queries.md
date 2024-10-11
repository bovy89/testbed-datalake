
https://www.findinpath.com/parse-json-in-trino/



```
select * from pg_example_public_shipments;
 shipment_id | order_id | date_created |   status   | __op |  __table  | __source_ts_ms |  __db   | __deleted |          __source_ts
-------------+----------+--------------+------------+------+-----------+----------------+---------+-----------+--------------------------------
       30500 |    10500 | 2021-01-21   | COMPLETED  | r    | shipments |  1691495717463 | example | false     | 2023-08-08 11:55:17.463000 UTC
       32500 |    12500 | 2021-05-31   | PROCESSING | r    | shipments |  1691495717463 | example | false     | 2023-08-08 11:55:17.463000 UTC
         666 |     6666 | 2023-05-31   | TEST       | r    | shipments |  1691495717463 | example | false     | 2023-08-08 11:55:17.463000 UTC
       31500 |    11500 | 2021-04-21   | COMPLETED  | r    | shipments |  1691495717463 | example | false     | 2023-08-08 11:55:17.463000 UTC
(4 rows)


select * from pg_example_public_suppliers;
 supplier_id | supplier_name | __op |  __table  | __source_ts_ms |  __db   | __deleted |          __source_ts
-------------+---------------+------+-----------+----------------+---------+-----------+--------------------------------
           1 | Pippo         | r    | suppliers |  1691495717463 | example | false     | 2023-08-08 11:55:17.463000 UTC
           2 | Pluto         | r    | suppliers |  1691495717463 | example | false     | 2023-08-08 11:55:17.463000 UTC
           3 | Paperino      | r    | suppliers |  1691495717463 | example | false     | 2023-08-08 11:55:17.463000 UTC
(3 rows)



DELETE FROM shipments WHERE shipment_id = 32500;
UPDATE shipments SET status = 'COMPLETED' WHERE shipment_id = 666;
ALTER TABLE suppliers ADD COLUMN email_address character varying(255) COLLATE pg_catalog."default";
INSERT INTO suppliers values (4, 'Minnie', 'minnie@example.com');



select * from pg_example_public_shipments;
 shipment_id | order_id | date_created |  status   | __op |  __table  | __source_ts_ms |  __db   | __deleted |          __source_ts
-------------+----------+--------------+-----------+------+-----------+----------------+---------+-----------+--------------------------------
         666 |     6666 | 2023-05-31   | COMPLETED | u    | shipments |  1691502503922 | example | false     | 2023-08-08 13:48:23.922000 UTC
       30500 |    10500 | 2021-01-21   | COMPLETED | r    | shipments |  1691501548310 | example | false     | 2023-08-08 13:32:28.310000 UTC
       31500 |    11500 | 2021-04-21   | COMPLETED | r    | shipments |  1691501548310 | example | false     | 2023-08-08 13:32:28.310000 UTC
(3 rows)


select * from pg_example_public_suppliers;
 supplier_id | supplier_name | __op |  __table  | __source_ts_ms |  __db   | __deleted |          __source_ts           |   email_address
-------------+---------------+------+-----------+----------------+---------+-----------+--------------------------------+--------------------
           4 | Minnie        | c    | suppliers |  1691502511154 | example | false     | 2023-08-08 13:48:31.154000 UTC | minnie@example.com
           1 | Pippo         | r    | suppliers |  1691501548310 | example | false     | 2023-08-08 13:32:28.310000 UTC | NULL
           2 | Pluto         | r    | suppliers |  1691501548310 | example | false     | 2023-08-08 13:32:28.310000 UTC | NULL
           3 | Paperino      | r    | suppliers |  1691501548310 | example | false     | 2023-08-08 13:32:28.310000 UTC | NULL
(4 rows)



select * from mongodb_inventory_customers;
 _id  | first_name | last_name |                                     contact                                     | __deleted | __op | __collection | __source_ts_ms |   __db    |          __source_ts
------+------------+-----------+---------------------------------------------------------------------------------+-----------+------+--------------+----------------+-----------+--------------------------------
 1001 | Sally      | Thomas    | [{type=email, value=sally.thomas@acme.com}, {type=phone, value=+39 0000000000}] | false     | r    | customers    |              0 | inventory | 1970-01-01 00:00:00.000000 UTC
 1002 | George     | Bailey    | [{type=email, value=gbailey@foobar.com}, {type=phone, value=+39 1111111111}]    | false     | r    | customers    |              0 | inventory | 1970-01-01 00:00:00.000000 UTC
 1003 | Edward     | Walker    | [{type=email, value=ed@walker.com}, {type=phone, value=+39 2222222222}]         | false     | r    | customers    |              0 | inventory | 1970-01-01 00:00:00.000000 UTC
 1004 | Anne       | Kretchmar | [{type=email, value=annek@noanswer.org}, {type=phone, value=+39 3333333333}]    | false     | r    | customers    |              0 | inventory | 1970-01-01 00:00:00.000000 UTC
(4 rows)



select 
first_name,
last_name,
json_query(json_format(cast(contact as JSON)), 'strict $[*]?(@.type == "email").value' OMIT QUOTES) as email,
json_query(json_format(cast(contact as JSON)), 'strict $[*]?(@.type == "phone").value' OMIT QUOTES) as phone
from
mongodb_inventory_customers;

 first_name | last_name |         email         |     phone
------------+-----------+-----------------------+----------------
 Sally      | Thomas    | sally.thomas@acme.com | +39 0000000000
 George     | Bailey    | gbailey@foobar.com    | +39 1111111111
 Edward     | Walker    | ed@walker.com         | +39 2222222222
 Anne       | Kretchmar | annek@noanswer.org    | +39 3333333333


select * from mongodb_inventory_products;
 _id |        name        |            description             | weight | quantity | __deleted | __op | __collection | __source_ts_ms |   __db    |          __source_ts
-----+--------------------+------------------------------------+--------+----------+-----------+------+--------------+----------------+-----------+--------------------------------
 101 | scooter            | Small 2-wheel scooter              | 3.14   |        3 | false     | r    | products     |              0 | inventory | 1970-01-01 00:00:00.000000 UTC
 102 | car battery        | 12V car battery                    | 8.1    |        8 | false     | r    | products     |              0 | inventory | 1970-01-01 00:00:00.000000 UTC
 103 | 12-pack drill bits | 12-pack from #40 to #3             | 0.8    |       18 | false     | r    | products     |              0 | inventory | 1970-01-01 00:00:00.000000 UTC
 104 | hammer             | 12oz carpenter's hammer            | 0.75   |        4 | false     | r    | products     |              0 | inventory | 1970-01-01 00:00:00.000000 UTC
 105 | hammer             | 14oz carpenter's hammer            | 0.875  |        5 | false     | r    | products     |              0 | inventory | 1970-01-01 00:00:00.000000 UTC
 106 | hammer             | 16oz carpenter's hammer            | 1.0    |        0 | false     | r    | products     |              0 | inventory | 1970-01-01 00:00:00.000000 UTC
 107 | rocks              | box of assorted rocks              | 5.3    |       44 | false     | r    | products     |              0 | inventory | 1970-01-01 00:00:00.000000 UTC
 108 | jacket             | water resistent black wind breaker | 0.1    |        2 | false     | r    | products     |              0 | inventory | 1970-01-01 00:00:00.000000 UTC
 109 | spare tire         | 24 inch spare tire                 | 22.2   |        5 | false     | r    | products     |              0 | inventory | 1970-01-01 00:00:00.000000 UTC
(9 rows)



select * from mongodb_inventory_orders;
            ->
  _id  |  order_date   | purchaser_id | quantity | product_id | __deleted | __op | __collection | __source_ts_ms |   __db    |          __source_ts
-------+---------------+--------------+----------+------------+-----------+------+--------------+----------------+-----------+--------------------------------
 10004 | 1456012800000 |         4444 |        7 |       4666 | false     | u    | orders       |  1693241918000 | inventory | 2023-08-28 16:58:38.000000 UTC
 10001 | 1452902400000 |         1111 |        1 |       1666 | false     | r    | orders       |              0 | inventory | 1970-01-01 00:00:00.000000 UTC
 10002 | 1452988800000 |         2222 |        2 |       2666 | false     | r    | orders       |              0 | inventory | 1970-01-01 00:00:00.000000 UTC
 10003 | 1455840000000 |         3333 |        2 |       3666 | false     | r    | orders       |              0 | inventory | 1970-01-01 00:00:00.000000 UTC
(4 rows)


db.getSiblingDB('inventory').orders.updateOne(
  {"_id": 10004 },
  {
    $set: { 'quantity': NumberInt("7") },
  }
);


select * from mongodb_inventory_orders;
            ->
  _id  |  order_date   | purchaser_id | quantity | product_id | __deleted | __op | __collection | __source_ts_ms |   __db    |          __source_ts
-------+---------------+--------------+----------+------------+-----------+------+--------------+----------------+-----------+--------------------------------
 10004 | 1456012800000 |         4444 |        7 |       4666 | false     | u    | orders       |  1693241918000 | inventory | 2023-08-28 16:58:38.000000 UTC
 10001 | 1452902400000 |         1111 |        1 |       1666 | false     | r    | orders       |              0 | inventory | 1970-01-01 00:00:00.000000 UTC
 10002 | 1452988800000 |         2222 |        2 |       2666 | false     | r    | orders       |              0 | inventory | 1970-01-01 00:00:00.000000 UTC
 10003 | 1455840000000 |         3333 |        2 |       3666 | false     | r    | orders       |              0 | inventory | 1970-01-01 00:00:00.000000 UTC
(4 rows)

db.getSiblingDB('inventory').orders.deleteOne({"_id": 10004 })


select * from mongodb_inventory_orders;
            ->
  _id  |  order_date   | purchaser_id | quantity | product_id | __deleted | __op | __collection | __source_ts_ms |   __db    |          __source_ts
-------+---------------+--------------+----------+------------+-----------+------+--------------+----------------+-----------+--------------------------------
 10001 | 1452902400000 |         1111 |        1 |       1666 | false     | r    | orders       |              0 | inventory | 1970-01-01 00:00:00.000000 UTC
 10002 | 1452988800000 |         2222 |        2 |       2666 | false     | r    | orders       |              0 | inventory | 1970-01-01 00:00:00.000000 UTC
 10003 | 1455840000000 |         3333 |        2 |       3666 | false     | r    | orders       |              0 | inventory | 1970-01-01 00:00:00.000000 UTC
(3 rows)




CREATE OR REPLACE VIEW shipments_view
AS
select shipment_id, order_id, status, courier from postgres_public_shipments ;



CREATE MATERIALIZED VIEW shipments_mview
AS
select shipment_id, order_id, status from pg_example_public_shipments ;
```
