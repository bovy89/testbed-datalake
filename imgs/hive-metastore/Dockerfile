FROM eclipse-temurin:11-jre-alpine@sha256:eeca23b6c113f1817837d3ced7d70405db4664aade6b6f30076160e346fbbfb9

ENV HIVE_VERSION=4.0.0
ENV POSTGRESQL_DRIVER_VERSION=42.6.0
ENV AWS_SDK_VERSION=1.12.238
ENV HADOOP_VERSION=3.3.4
# questo deve combaciare con la hadoop-client-api/hadoop-client-runtime distribuita da spark

ENV HADOOP_HOME=/opt/hadoop
ENV HIVE_HOME=/opt/hive-metastore

WORKDIR /opt

RUN apk add --no-cache bash curl

RUN curl -L https://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz \
| tar xz -C /opt/  \
&& mv "/opt/hadoop-$HADOOP_VERSION" "$HADOOP_HOME" \
&& rm -r "$HADOOP_HOME"/share/doc

RUN curl -L https://archive.apache.org/dist/hive/hive-${HIVE_VERSION}/apache-hive-${HIVE_VERSION}-bin.tar.gz \
| tar xz -C /opt/  \
&& mv "/opt/apache-hive-$HIVE_VERSION-bin" "$HIVE_HOME"

#needed to fix nosuchmethoderror
#see https://issues.apache.org/jira/browse/HIVE-22915
RUN rm -rf "$HIVE_HOME"/lib/guava-* && \
cp "$HADOOP_HOME"/share/hadoop/hdfs/lib/guava-* "$HIVE_HOME"/lib


# Download and install the Postgres connector.
RUN curl -L https://jdbc.postgresql.org/download/postgresql-${POSTGRESQL_DRIVER_VERSION}.jar -o \
"$HIVE_HOME"/lib/postgresql-${POSTGRESQL_DRIVER_VERSION}.jar 

# Download and install the S3 related Jars
RUN curl -L https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/${HADOOP_VERSION}/hadoop-aws-${HADOOP_VERSION}.jar -o \
"$HIVE_HOME"/lib/hadoop-aws-${HADOOP_VERSION}.jar \
&& curl -L https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk/${AWS_SDK_VERSION}/aws-java-sdk-${AWS_SDK_VERSION}.jar -o \
"$HIVE_HOME"/lib/aws-java-sdk-${AWS_SDK_VERSION}.jar \
&& curl -L https://repo1.maven.org/maven2/net/java/dev/jets3t/jets3t/0.9.4/jets3t-0.9.4.jar -o \
 "$HIVE_HOME"/lib/jets3t-0.9.4.jar \
&& curl -L https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-core/${AWS_SDK_VERSION}/aws-java-sdk-core-${AWS_SDK_VERSION}.jar -o \
"$HIVE_HOME"/lib/aws-java-sdk-core-${AWS_SDK_VERSION}.jar \
&& curl -L https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/${AWS_SDK_VERSION}/aws-java-sdk-bundle-${AWS_SDK_VERSION}.jar -o \
"$HIVE_HOME"/lib/aws-java-sdk-bundle-${AWS_SDK_VERSION}.jar \
# Below for transcaction bug https://github.com/trinodb/trino/issues/6980
&& curl -L  https://repo1.maven.org/maven2/org/apache/hive/hive-exec/${HIVE_VERSION}/hive-exec-${HIVE_VERSION}.jar -o \
"$HIVE_HOME"/lib/hive-exec-${HIVE_VERSION}.jar \
&& curl -L https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-web/2.17.2/log4j-web-2.17.2.jar -o \
"$HIVE_HOME"/lib/log4j-web-2.17.2.jar

ARG UID=1000

RUN adduser -D -H -s /sbin/nologin --gecos "" --uid $UID hive

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh \
&& chown hive:hive -R "$HADOOP_HOME" \
&& chown hive:hive -R "$HIVE_HOME"

USER hive
EXPOSE 9083

ENTRYPOINT ["sh", "-c", "/entrypoint.sh"]
