
Test kerberos client partenda da immagine base almalinux 8

```
docker exec -it test_kerberos /bin/bash
yum install -y krb5-workstation
kinit -kt /etc/trino/keytabs/trino.keytab trino/trino.example.com@EXAMPLE.COM
kinit -kt /etc/trino/keytabs/hive.keytab hive/hive-metastore.example.com@EXAMPLE.COM
klist
```

Link utili:

- https://github.com/trinodb/trino/blob/b9855eeb6ceaf129331138948d485ad4ae53c803/docs/src/main/sphinx/security/kerberos.md?plain=1#L18
- https://github.com/mans0954/docker-kerberos/blob/master/kadmin/Dockerfile

