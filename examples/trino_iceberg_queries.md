
https://medium.com/@tglawless/apache-iceberg-table-maintenance-using-pyspark-cb2fb4b892bb
https://tabular.io/apache-iceberg-cookbook/data-operations-with-apache-iceberg/
https://tabular.io/apache-iceberg-cookbook/data-operations-compaction/
https://tabular.io/apache-iceberg-cookbook/data-operations-snapshot-expiration/
https://tabular.io/apache-iceberg-cookbook/data-operations-orphan-file-cleanup/


```
trino:default> SELECT committed_at, snapshot_id, operation FROM "pg_example_public_shipments$snapshots";
        committed_at         |     snapshot_id     | operation
-----------------------------+---------------------+-----------
 2023-08-08 13:33:52.103 UTC | 8662459764725222382 | overwrite
 2023-08-08 13:35:13.775 UTC |    9160490111681781 | overwrite
 2023-08-08 13:48:24.894 UTC | 4012176428316334465 | overwrite

snapshot_id = 9160490111681781 --> latest

8662459764725222382 ---> before delete

select * from "pg_example_public_shipments" for version as of 8662459764725222382;

trino:default> select * from "pg_example_public_shipments" for version as of 8662459764725222382;
 shipment_id | order_id | date_created |   status   | __op |  __table  | __source_ts_ms |  __db   | __deleted |          __source_ts
-------------+----------+--------------+------------+------+-----------+----------------+---------+-----------+--------------------------------
       30500 |    10500 | 2021-01-21   | COMPLETED  | r    | shipments |  1691501548310 | example | false     | 2023-08-08 13:32:28.310000 UTC
       32500 |    12500 | 2021-05-31   | PROCESSING | r    | shipments |  1691501548310 | example | false     | 2023-08-08 13:32:28.310000 UTC
         666 |     6666 | 2023-05-31   | TEST       | r    | shipments |  1691501548310 | example | false     | 2023-08-08 13:32:28.310000 UTC
       31500 |    11500 | 2021-04-21   | COMPLETED  | r    | shipments |  1691501548310 | example | false     | 2023-08-08 13:32:28.310000 UTC
(4 rows)



trino:default> SELECT content, file_path, file_format, record_count, file_size_in_bytes FROM "pg_example_public_shipments$files";
            ->
 content |                                                      file_path                                                      | file_format | record_count | file_size_in_bytes
---------+---------------------------------------------------------------------------------------------------------------------+-------------+--------------+--------------------
       0 | s3a://warehouse/hive/pg_example_public_shipments/data/20230808-1-ee6f5eea-cfa0-4525-8b97-fe167907799c-00001.parquet | PARQUET     |            4 |               3463
       0 | s3a://warehouse/hive/pg_example_public_shipments/data/20230808-1-7204a874-7055-4846-ad2b-83fd6bfb55d5-00001.parquet | PARQUET     |            1 |               3081



reduce number of small files

ALTER TABLE "pg_example_public_shipments" EXECUTE optimize;

trino:default> SELECT content, file_path, file_format, record_count, file_size_in_bytes FROM "pg_example_public_shipments$files";
 content |                                                           file_path                                                            | file_format | record_count | file_size_in_bytes
---------+--------------------------------------------------------------------------------------------------------------------------------+-------------+--------------+--------------------
       0 | s3a://warehouse/hive/pg_example_public_shipments/data/20230808_135639_00036_gixdr-a0ffc1c2-4950-4f6b-9d90-c1a3857e2659.parquet | PARQUET     |            3 |               1895


trino:default> select * from "pg_example_public_shipments";
 shipment_id | order_id | date_created |  status   | __op |  __table  | __source_ts_ms |  __db   | __deleted |          __source_ts
-------------+----------+--------------+-----------+------+-----------+----------------+---------+-----------+--------------------------------
         666 |     6666 | 2023-05-31   | COMPLETED | u    | shipments |  1691502503922 | example | false     | 2023-08-08 13:48:23.922000 UTC
       30500 |    10500 | 2021-01-21   | COMPLETED | r    | shipments |  1691501548310 | example | false     | 2023-08-08 13:32:28.310000 UTC
       31500 |    11500 | 2021-04-21   | COMPLETED | r    | shipments |  1691501548310 | example | false     | 2023-08-08 13:32:28.310000 UTC
(3 rows)

Query 20230808_135705_00038_gixdr, FINISHED, 1 node
Splits: 1 total, 1 done (100.00%)
0.19 [3 rows, 2.55KB] [16 rows/s, 13.6KB/s]

trino:default> select * from "pg_example_public_shipments" for version as of 8662459764725222382;
            ->
 shipment_id | order_id | date_created |   status   | __op |  __table  | __source_ts_ms |  __db   | __deleted |          __source_ts
-------------+----------+--------------+------------+------+-----------+----------------+---------+-----------+--------------------------------
       30500 |    10500 | 2021-01-21   | COMPLETED  | r    | shipments |  1691501548310 | example | false     | 2023-08-08 13:32:28.310000 UTC
       32500 |    12500 | 2021-05-31   | PROCESSING | r    | shipments |  1691501548310 | example | false     | 2023-08-08 13:32:28.310000 UTC
         666 |     6666 | 2023-05-31   | TEST       | r    | shipments |  1691501548310 | example | false     | 2023-08-08 13:32:28.310000 UTC
       31500 |    11500 | 2021-04-21   | COMPLETED  | r    | shipments |  1691501548310 | example | false     | 2023-08-08 13:32:28.310000 UTC



trino:default> SELECT committed_at, snapshot_id, operation FROM "pg_example_public_shipments$snapshots";
        committed_at         |     snapshot_id     | operation
-----------------------------+---------------------+-----------
 2023-08-08 13:33:52.103 UTC | 8662459764725222382 | overwrite
 2023-08-08 13:35:13.775 UTC |    9160490111681781 | overwrite
 2023-08-08 13:48:24.894 UTC | 4012176428316334465 | overwrite
 2023-08-08 13:56:39.491 UTC | 6815473541456580779 | replace




SELECT * FROM "pg_example_public_shipments$properties";
SELECT * FROM "pg_example_public_shipments$files";
SELECT * FROM "pg_example_public_shipments$manifests";
SELECT * FROM "pg_example_public_shipments$history";
SELECT * FROM "pg_example_public_shipments$partitions";
SELECT * FROM "pg_example_public_shipments$snapshots";
SELECT * FROM "pg_example_public_shipments$refs";


ALTER TABLE "pg_example_public_shipments" EXECUTE expire_snapshots(retention_threshold => '1d');

The value for retention_threshold must be higher than or equal to iceberg.expire_snapshots.min-retention in the catalog, otherwise the procedure fails with a similar message: Retention specified (1.00d) is shorter than the minimum retention configured in the system (7.00d). The default value for this property is 7d.


ALTER TABLE "pg_example_public_shipments" EXECUTE remove_orphan_files(retention_threshold => '7d');

ALTER TABLE "pg_example_public_shipments" EXECUTE drop_extended_stats;


select * from pg_example_public_shipments for version as of 2061890635617908015;
```
