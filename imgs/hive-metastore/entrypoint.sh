#!/bin/bash

# https://github.com/apache/hive/blob/master/packaging/src/docker/entrypoint.sh

DB_DRIVER=${DB_DRIVER:=derby}
SKIP_SCHEMA_INIT="${IS_RESUME:-false}"
VERBOSE="${VERBOSE:-false}"
LOGLEVEL="${LOGLEVEL:-INFO}"


[[ $VERBOSE = "true" ]] && VERBOSE_MODE="--verbose" || VERBOSE_MODE=""

function initialize_hive {
  COMMAND="-initOrUpgradeSchema"
  if [ "$(echo "$HIVE_VERSION" | cut -d '.' -f1)" -lt "4" ]; then
    COMMAND="-${SCHEMA_COMMAND:-initSchema}"
  fi

  # shellcheck disable=SC2086
  if "$HIVE_HOME"/bin/schematool -dbType $DB_DRIVER $COMMAND $VERBOSE_MODE; then
    echo "Initialized schema successfully.."
  else
    echo "Schema initialization failed!"
    exit 1
  fi
}

if [[ "${SKIP_SCHEMA_INIT}" == "false" ]]; then
  # handles schema initialization
  initialize_hive
fi

# shellcheck disable=SC2086
"$HIVE_HOME/bin/hive" -hiveconf hive.root.logger=$LOGLEVEL,console --service metastore $VERBOSE_MODE
