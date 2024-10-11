
TODO: must be adapted to work with tls and kerberos


Setup (CDC):
- `make compose_cdc_build`
- `make compose_cdc`
- `make debezium_logs`
- [setup postgresql source](#setup-postgresql-source)
- [setup mongodb source](#setup-mongodb-source)
- [setup iceberg sink verso s3](#setup-iceberg-sink-verso-s3)
- check kafka status (topics and connectors status) using kafka ui
- cehck debezium_logs
- `make trino_shell`
- verify data:
```
show schemas;
       Schema
--------------------
 default
 information_schema
(2 rows)

show tables from default;
            Table
-----------------------------
 mongodb_inventory_customers
 mongodb_inventory_orders
 mongodb_inventory_products
 pg_example_public_shipments
 pg_example_public_suppliers
(5 rows)
```

Clean-up:

- `make compose_cdc_down` or `compose_cdc_downclean`


## setup postgresql source

```
make postgresql_shell

CREATE TABLE IF NOT EXISTS shipments
(
    shipment_id bigint NOT NULL,
    order_id bigint NOT NULL,
    date_created character varying(255) COLLATE pg_catalog."default",
    status character varying(25) COLLATE pg_catalog."default",
    CONSTRAINT shipments_pkey PRIMARY KEY (shipment_id)
);

CREATE TABLE IF NOT EXISTS suppliers
(
    supplier_id bigint NOT NULL,
    supplier_name character varying(255) COLLATE pg_catalog."default",
    CONSTRAINT suppliers_pkey PRIMARY KEY (supplier_id)
);


INSERT INTO shipments values (30500,10500,'2021-01-21','COMPLETED');
INSERT INTO shipments values (31500,11500,'2021-04-21','COMPLETED');
INSERT INTO shipments values (32500,12500,'2021-05-31','PROCESSING');
INSERT INTO shipments values (666,6666,'2023-05-31','TEST');


INSERT INTO suppliers values (1, 'Pippo');
INSERT INTO suppliers values (2, 'Pluto');
INSERT INTO suppliers values (3, 'Paperino');

curl -X DELETE http://localhost:8083/connectors/pg_example-connector

curl -X POST -H 'Content-Type: application/json' http://localhost:8083/connectors --data '
{
  "name": "pg_example-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "tasks.max": 1,
    "plugin.name": "decoderbufs",
    "database.hostname": "db-pg",
    "database.port": "5432",
    "database.user": "postgres",
    "database.password": "postgres",
    "slot.name": "dbz_example",
    "publication.name": "dbzpublication_example",
    "database.dbname" : "example",
    "topic.prefix": "pg_example",
    "table.include.list": "public.shipments,public.suppliers"
  }
}'
```

## setup mongodb source

```
make mongodb_shell

db.getSiblingDB('inventory').orders.insertMany([
    { _id : NumberLong("10001"), order_date : new ISODate("2016-01-16T00:00:00Z"), purchaser_id : NumberLong("1111"), quantity : NumberInt("1"), product_id : NumberLong("1666") },
    { _id : NumberLong("10002"), order_date : new ISODate("2016-01-17T00:00:00Z"), purchaser_id : NumberLong("2222"), quantity : NumberInt("2"), product_id : NumberLong("2666") },
    { _id : NumberLong("10003"), order_date : new ISODate("2016-02-19T00:00:00Z"), purchaser_id : NumberLong("3333"), quantity : NumberInt("2"), product_id : NumberLong("3666") },
    { _id : NumberLong("10004"), order_date : new ISODate("2016-02-21T00:00:00Z"), purchaser_id : NumberLong("4444"), quantity : NumberInt("1"), product_id : NumberLong("4666") }
])

db.getSiblingDB('inventory').products.insertMany([
    { _id : NumberLong("101"), name : 'scooter', description: 'Small 2-wheel scooter', weight : Decimal128("3.14"), quantity : NumberInt("3") },
    { _id : NumberLong("102"), name : 'car battery', description: '12V car battery', weight : Decimal128("8.1"), quantity : NumberInt("8") },
    { _id : NumberLong("103"), name : '12-pack drill bits', description: '12-pack from #40 to #3', weight : Decimal128("0.8"), quantity : NumberInt("18") },
    { _id : NumberLong("104"), name : 'hammer', description: "12oz carpenter's hammer", weight : Decimal128("0.75"), quantity : NumberInt("4") },
    { _id : NumberLong("105"), name : 'hammer', description: "14oz carpenter's hammer", weight : Decimal128("0.875"), quantity : NumberInt("5") },
    { _id : NumberLong("106"), name : 'hammer', description: "16oz carpenter's hammer", weight : Decimal128("1.0"), quantity : NumberInt("0") },
    { _id : NumberLong("107"), name : 'rocks', description: 'box of assorted rocks', weight : Decimal128("5.3"), quantity : NumberInt("44") },
    { _id : NumberLong("108"), name : 'jacket', description: 'water resistent black wind breaker', weight : Decimal128("0.1"), quantity : NumberInt("2") },
    { _id : NumberLong("109"), name : 'spare tire', description: '24 inch spare tire', weight : Decimal128("22.2"), quantity : NumberInt("5") }
])

db.getSiblingDB('inventory').customers.insertMany([
    { _id : NumberLong("1001"), first_name : 'Sally', last_name : 'Thomas', "contact": [{"type": "email", "value": "sally.thomas@acme.com"}, {"type": "phone", "value": "+39 0000000000"}]},
    { _id : NumberLong("1002"), first_name : 'George', last_name : 'Bailey', "contact": [{"type": "email", "value": "gbailey@foobar.com"}, {"type": "phone", "value": "+39 1111111111"}]},
    { _id : NumberLong("1003"), first_name : 'Edward', last_name : 'Walker', "contact": [{"type": "email", "value": "ed@walker.com"}, {"type": "phone", "value": "+39 2222222222"}]},
    { _id : NumberLong("1004"), first_name : 'Anne', last_name : 'Kretchmar', "contact": [{"type": "email", "value": "annek@noanswer.org"}, {"type": "phone", "value": "+39 3333333333"}]}
])

db.getSiblingDB('inventory').runCommand ( { collMod: "orders", changeStreamPreAndPostImages: { enabled: true } } );
db.getSiblingDB('inventory').runCommand ( { collMod: "products", changeStreamPreAndPostImages: { enabled: true } } );
db.getSiblingDB('inventory').runCommand ( { collMod: "customers", changeStreamPreAndPostImages: { enabled: true } } );


db.getSiblingDB('inventory').getCollectionInfos();
db.getSiblingDB('inventory').getCollectionInfos({ name: "orders" });


curl -X DELETE http://localhost:8083/connectors/mongodb-connector

curl -X POST -H 'Content-Type: application/json' http://localhost:8083/connectors --data '
{
  "name": "mongodb-connector",
  "config": {
    "connector.class" : "io.debezium.connector.mongodb.MongoDbConnector",
    "tasks.max": 1,
    "mongodb.connection.string": "mongodb://db-mongo:27017/?replicaSet=rs0",
    "mongodb.user" : "debezium",
    "mongodb.password" : "dbz",
    "topic.prefix" : "mongodb",
    "collection.include.list": "inventory.products,inventory.orders,inventory.customers",
    "capture.mode": "change_streams_with_pre_image"
  }
}'
```

# setup iceberg sink verso s3

## postgresql

```
curl -X DELETE http://localhost:8083/connectors/iceberg-sink-pg

curl -X POST -H 'Content-Type: application/json' http://localhost:8083/connectors --data '
{
  "name" :"iceberg-sink-pg",
  "config": {
    "connector.class": "com.getindata.kafka.connect.iceberg.sink.IcebergSink",
    "topics.regex": "pg_.*",
    "iceberg.catalog-impl": "org.apache.iceberg.hive.HiveCatalog",
    "iceberg.warehouse": "s3a://warehouse/iceberg",
    "iceberg.uri": "thrift://hive-metastore:9083",
    "iceberg.io-impl": "org.apache.iceberg.aws.s3.S3FileIO",
    "iceberg.s3.endpoint": "http://minio:9000",
    "iceberg.s3.access-key-id": "admin",
    "iceberg.s3.secret-access-key": "password",
    "iceberg.s3.path-style-access": true,
    "table.auto-create": true,
    "upsert.keep-deletes": false,
    "transforms" : "unwrap",
    "transforms.unwrap.type":"io.debezium.transforms.ExtractNewRecordState",
    "transforms.unwrap.add.fields":"op,table,source.ts_ms,db",
    "transforms.unwrap.drop.tombstones": true,
    "transforms.unwrap.delete.handling.mode": "rewrite"
  }
}'
```


## mongodb

```
curl -X DELETE http://localhost:8083/connectors/iceberg-sink-mongodb

curl -X POST -H 'Content-Type: application/json' http://localhost:8083/connectors --data '
{
  "name" :"iceberg-sink-mongodb",
  "config": {
    "connector.class": "com.getindata.kafka.connect.iceberg.sink.IcebergSink",
    "topics.regex": "mongodb.*",
    "iceberg.catalog-impl": "org.apache.iceberg.hive.HiveCatalog",
    "iceberg.warehouse": "s3a://warehouse/iceberg",
    "iceberg.uri": "thrift://hive-metastore:9083",
    "iceberg.io-impl": "org.apache.iceberg.aws.s3.S3FileIO",
    "iceberg.s3.endpoint": "http://minio:9000",
    "iceberg.s3.access-key-id": "admin",
    "iceberg.s3.secret-access-key": "password",
    "iceberg.s3.path-style-access": true,
    "table.auto-create": true,
    "allow-field-addition": false,
    "upsert.keep-deletes": false,
    "transforms": "unwrap,renamekeyfield",
    "transforms.unwrap.type": "io.debezium.connector.mongodb.transforms.ExtractNewDocumentState",
    "transforms.unwrap.add.fields": "op,collection,source.ts_ms,db",
    "transforms.unwrap.drop.tombstones": true,
    "transforms.unwrap.delete.handling.mode": "rewrite",
    "transforms.renamekeyfield.type": "org.apache.kafka.connect.transforms.ReplaceField$Key",
    "transforms.renamekeyfield.renames": "id:_id"
  }
}'
```
