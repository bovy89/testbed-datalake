
**DISCALIMER: do not use this in production**

This testbed (*still a work-in-progress*) provides 2 main modes to retrieve data from external sources:

- batch mode: data is exported from sources, uploaded to s3 and then processed in batch
- realtime mode: data is migrated from sources via CDC (tables are created directly by sink plugin)

NOTE: the use of realtime mode for MongoDB sources is temporarily suspended due to technical/design complications of data sources. For details about the CDC demo see [here](docs/CDC.md)


Requirements:
- `docker`
- `docker compose`
- `keytool` (e.g. provided by java-1.8.0-openjdk-headless)
- `openssl`
- Add `127.0.0.1 nginx` to `/etc/hosts`
- Create trino LDAP properties file (`./conf/trino/ldap.properties`). Example::
```
password-authenticator.name=ldap
ldap.url=CHANGEME
ldap.bind-dn=CHANGEME
ldap.bind-password=CHANGEME
ldap.group-auth-pattern=(|(&(objectClass=inetOrgPerson)(uid=${USER}))(&(objectClass=orgServices)(cn=${USER})))
ldap.user-base-dn=CHANGEME
```
- Set DBT LDAP credentials in `profile.yml` (`./resources/airflow/dbts/dbt_example/profiles.yml`)


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


<!-- ssh -L 9001:localhost:9001 -L 8080:localhost:8080 -L 7777:localhost:7777 <user>>@<remote_host> -->


Setup (batch mode):
- `make create_secrets`
- `make compose_batch_build`
- `make compose_batch`
- `make trino_shell` (login as admin):
```
create schema silver;
create schema gold;
```
- upload files from `examples/json_export_mongo` into bucket "landing/mongodb"
- using airflow, exec `load_mongo_json`
- `make airflow_shell`, then:
```
export DBT_ENV_SECRET_DBT_USER=<CHANGEME>
export DBT_ENV_SECRET_DBT_PASSWORD=<CHANGEME>
cd /opt/airflow/dbts/dbt_example && dbt run
```
- `make trino_shell` (login as non-admin user)
```
show schemas;
       Schema
--------------------
 gold
 silver
 bronze

show tables from gold;
     Table
---------------
 dim_customers
 fct_orders
```

Clean-up:

- `make compose_batch_down` or `make compose_batch_downclean`
