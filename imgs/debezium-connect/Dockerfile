FROM confluentinc/cp-kafka-connect:7.0.9 as cp
RUN confluent-hub install --no-prompt confluentinc/kafka-connect-s3:10.5.1

FROM quay.io/debezium/connect:2.7.1.Final
USER root:root

# Add S3 dependency (plugindir: /kafka/connect)
COPY --from=cp /usr/share/confluent-hub-components/confluentinc-kafka-connect-s3/ /kafka/connect/kafka-connect-s3/

RUN curl -L https://repo1.maven.org/maven2/com/google/guava/guava/30.1.1-jre/guava-30.1.1-jre.jar -o \
/kafka/connect/kafka-connect-s3/lib/guava-30.1.1-jre.jar \
&& curl -L https://repo1.maven.org/maven2/com/google/guava/failureaccess/1.0.1/failureaccess-1.0.1.jar -o \
/kafka/connect/kafka-connect-s3/lib/failureaccess-1.0.1.jar \
&& chown -R kafka:kafka /kafka/connect/kafka-connect-s3

# https://github.com/getindata/kafka-connect-iceberg-sink
RUN curl -L https://github.com/getindata/kafka-connect-iceberg-sink/releases/download/0.4.0/kafka-connect-iceberg-sink-0.4.0-plugin.zip -o \
/kafka/connect/kafka-connect-iceberg-sink-0.4.0-plugin.zip \
&& unzip -q /kafka/connect/kafka-connect-iceberg-sink-0.4.0-plugin.zip \
&& chown -R kafka:kafka /kafka/connect/kafka-connect-iceberg-sink \
&& rm -f /kafka/connect/kafka-connect-iceberg-sink-0.4.0-plugin.zip

USER kafka
