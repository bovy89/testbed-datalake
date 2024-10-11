#!/bin/bash

export SPARK_MODE="${SPARK_MODE:-master}"
export SPARK_MASTER_URL="${SPARK_MASTER_URL:-spark://CHANGEME:7077}"
export SPARK_NO_DAEMONIZE="${SPARK_NO_DAEMONIZE:-true}"


case "$SPARK_MODE" in
  master)
    echo "** Starting Spark in master mode **"
    start-master.sh;
    ;;
  worker)
    echo "** Starting Spark in worker mode **"
    start-worker.sh "$SPARK_MASTER_URL";
    ;;
  *)
    echo "Invalid mode $SPARK_MODE. Supported types are 'master/worker'"
    exit 1
    ;;
esac
