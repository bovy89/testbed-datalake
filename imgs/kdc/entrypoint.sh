#!/bin/bash

if [ ! -f /etc/krb5.conf ]; then
    echo "krb5.conf File not found!"
fi

if [ ! -f /var/kerberos/krb5kdc/kdc.conf ]; then
    echo "kdc.conf File not found!"
fi

if [ ! -f /var/kerberos/krb5kdc/kadm5.acl ]; then
    echo "kadm5.acl File not found!"
fi

export KEYTABS_BASEDIR="${KEYTABS_BASEDIR:-/root/kerberos-keytabs}"


mkdir -p "$KEYTABS_BASEDIR" || exit 1

kdb5_util create -s -P password -r EXAMPLE.COM || true


TRINO_KEYTAB_PATH="${KEYTABS_BASEDIR}"/trino.keytab
HIVE_KEYTAB_PATH="${KEYTABS_BASEDIR}"/hive.keytab
SPARK_KEYTAB_PATH="${KEYTABS_BASEDIR}"/spark.keytab

echo "Adding principals"

cat << EOF | kadmin.local &>/dev/null
add_principal -randkey trino/trino.example.com@EXAMPLE.COM
add_principal -randkey hive/hive-metastore.example.com@EXAMPLE.COM
add_principal -randkey spark/spark-iceberg.example.com@EXAMPLE.COM
quit
EOF

echo "Listing principals"

cat << EOF | kadmin.local &>/dev/stdout
listprincs
quit
EOF

if [ ! -f "${TRINO_KEYTAB_PATH}" ]; then
    echo "Creating trino keytab"
    cat << EOF | kadmin.local &>/dev/null
ktadd -k ${TRINO_KEYTAB_PATH} -norandkey trino/trino.example.com@EXAMPLE.COM
EOF
fi

if [ ! -f "${HIVE_KEYTAB_PATH}" ]; then
    echo "Creating hive keytab"
    cat << EOF | kadmin.local &>/dev/null
ktadd -k ${HIVE_KEYTAB_PATH} -norandkey hive/hive-metastore.example.com@EXAMPLE.COM
quit
EOF
fi

if [ ! -f "${SPARK_KEYTAB_PATH}" ]; then
    echo "Creating spark keytab"
    cat << EOF | kadmin.local &>/dev/null
ktadd -k ${SPARK_KEYTAB_PATH} -norandkey spark/spark-iceberg.example.com@EXAMPLE.COM
quit
EOF
fi

echo "Checking keytabs"

klist -e -kt "${TRINO_KEYTAB_PATH}"
klist -e -kt "${HIVE_KEYTAB_PATH}"
klist -e -kt "${SPARK_KEYTAB_PATH}"

chmod 666 "${KEYTABS_BASEDIR}"/*

/usr/sbin/krb5kdc -n
