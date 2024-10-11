```
connector.name=mongodb
mongodb.connection-url=mongodb://debezium:dbz@db-mongo:27017/?replicaSet=rs0



trino@8db756cebbb8:/$ /bin/trino --server trino:8080 --catalog mongodb
trino> show schemas;
       Schema
--------------------
 information_schema
 inventory
(2 rows)

Query 20240820_073716_00009_3r7j8, FINISHED, 1 node
Splits: 19 total, 19 done (100.00%)
0.11 [2 rows, 37B] [18 rows/s, 343B/s]

trino> use inventory;
USE
trino:inventory>
trino:inventory>
trino:inventory>
trino:inventory> show tables;
   Table
-----------
 customers
 orders
 products
(3 rows)

Query 20240820_073728_00013_3r7j8, FINISHED, 1 node
Splits: 19 total, 19 done (100.00%)
0.12 [3 rows, 80B] [25 rows/s, 678B/s]

trino:inventory> select * from customers;
 _id  | first_name | last_name |                                     contact
------+------------+-----------+---------------------------------------------------------------------------------
 1001 | Sally      | Thomas    | [{type=email, value=sally.thomas@acme.com}, {type=phone, value=+39 0000000000}]
 1002 | George     | Bailey    | [{type=email, value=gbailey@foobar.com}, {type=phone, value=+39 1111111111}]
 1003 | Edward     | Walker    | [{type=email, value=ed@walker.com}, {type=phone, value=+39 2222222222}]
 1004 | Anne       | Kretchmar | [{type=email, value=annek@noanswer.org}, {type=phone, value=+39 3333333333}]
(4 rows)

Query 20240820_073732_00014_3r7j8, FINISHED, 1 node
Splits: 1 total, 1 done (100.00%)
0.27 [4 rows, 0B] [15 rows/s, 0B/s]

trino:inventory> select * from orders;
  _id  |       order_date        | purchaser_id | quantity | product_id
-------+-------------------------+--------------+----------+------------
 10001 | 2016-01-16 00:00:00.000 |         1111 |        1 |       1666
 10002 | 2016-01-17 00:00:00.000 |         2222 |        2 |       2666
 10003 | 2016-02-19 00:00:00.000 |         3333 |        2 |       3666
 10004 | 2016-02-21 00:00:00.000 |         4444 |        1 |       4666
(4 rows)

Query 20240820_073933_00015_3r7j8, FINISHED, 1 node
Splits: 1 total, 1 done (100.00%)
0.16 [4 rows, 0B] [24 rows/s, 0B/s]

trino:inventory> select * from products;
 _id |        name        |            description             | quantity
-----+--------------------+------------------------------------+----------
 101 | scooter            | Small 2-wheel scooter              |        3
 102 | car battery        | 12V car battery                    |        8
 103 | 12-pack drill bits | 12-pack from #40 to #3             |       18
 104 | hammer             | 12oz carpenter's hammer            |        4
 105 | hammer             | 14oz carpenter's hammer            |        5
 106 | hammer             | 16oz carpenter's hammer            |        0
 107 | rocks              | box of assorted rocks              |       44
 108 | jacket             | water resistent black wind breaker |        2
 109 | spare tire         | 24 inch spare tire                 |        5
(9 rows)

Query 20240820_073942_00016_3r7j8, FINISHED, 1 node
Splits: 1 total, 1 done (100.00%)
0.07 [9 rows, 0B] [136 rows/s, 0B/s]
```
