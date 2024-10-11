
**DISCALIMER: do not use this in production**

This testbed (*still a work-in-progress*) provides 2 main modes to retrieve data from external sources:

- batch mode: data is exported from sources, uploaded to s3 and then processed in batch
- realtime mode: data is migrated from sources via CDC (tables are created directly by sink plugin)

NOTE: the use of realtime mode for MongoDB sources is temporarily suspended due to technical/design complications of data sources. For details about the CDC demo see [here](docs/CDC.md)


Services access point:
- minio UI (admin/password): http://localhost:9001/
- airflow UI (see keycloak users credentials): http://localhost:8080
- spark master UI: https://localhost:8061/
- spark worker UI: https://localhost:8062/
- trino UI (see keycloak users credentials): https://localhost:9999/
- keycloak UI: http://localhost:7777/

- realtime mode only services:
    - apicurio/schema-registry UI: http://localhost:8081/
    - kafka UI: http://localhost:8888/


Keycloak users credentials: see [here](.env##keycloak-users)


Setup (batch mode):
- `make create_secrets`
- `make compose_batch_build`
- `make compose_batch`
- upload files from `examples/json_export_mongo` into bucket "warehouse"
- using airflow, exec `load_jaffle_shop_dynamic`
- `make airflow_shell`, then `cd /opt/airflow/dbts/dbt_example && dbt run`
- `make trino_shell`
- verify data:
```
show schemas;
       Schema
--------------------
 default
 gold
 information_schema
 silver
 stage

show tables from gold;
     Table
---------------
 dim_customers
 fct_orders
```

Clean-up:

- `make compose_batch_down` or `compose_batch_downclean`
