ARG SPARK_MAJOR_VERSION=3.5
ARG SPARK_HOTFIX_VERSION=2
ARG SCALA_VERSION=2.12
ARG SHA256=sha256:6c3e5524f6f33775b0b4f7c44b90f19ea426d524bbb19bdf7edcd10e3513d945

FROM apache/spark:$SPARK_MAJOR_VERSION.$SPARK_HOTFIX_VERSION-scala$SCALA_VERSION-java11-python3-ubuntu@$SHA256
ARG SPARK_MAJOR_VERSION
ARG SCALA_VERSION


ENV ICEBERG_VERSION=1.6.0
ENV AWS_SDK_VERSION=1.12.238
ENV HADOOP_VERSION=3.3.6

RUN mkdir -p "$SPARK_HOME"/iceberg/spark-events "$SPARK_HOME"/conf

# needed to fix nosuchmethoderror
# see https://issues.apache.org/jira/browse/HIVE-22915
RUN rm -rf "${SPARK_HOME}"/jars/guava-* \
&& curl -L https://repo1.maven.org/maven2/com/google/guava/guava/27.0-jre/guava-27.0-jre.jar -o \
"${SPARK_HOME}"/jars/guava-27.0-jre.jar

RUN curl -L https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/${HADOOP_VERSION}/hadoop-aws-${HADOOP_VERSION}.jar -o \
"${SPARK_HOME}"/jars/hadoop-aws-${HADOOP_VERSION}.jar \
&& curl -L https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk/${AWS_SDK_VERSION}/aws-java-sdk-${AWS_SDK_VERSION}.jar -o \
"${SPARK_HOME}"/jars/aws-java-sdk-${AWS_SDK_VERSION}.jar \
&& curl -L https://repo1.maven.org/maven2/net/java/dev/jets3t/jets3t/0.9.4/jets3t-0.9.4.jar -o \
"${SPARK_HOME}"/jars/jets3t-0.9.4.jar \
&& curl -L https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-core/${AWS_SDK_VERSION}/aws-java-sdk-core-${AWS_SDK_VERSION}.jar -o \
"${SPARK_HOME}"/jars/aws-java-sdk-core-${AWS_SDK_VERSION}.jar \
&& curl -L https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/${AWS_SDK_VERSION}/aws-java-sdk-bundle-${AWS_SDK_VERSION}.jar -o \
"${SPARK_HOME}"/jars/aws-java-sdk-bundle-${AWS_SDK_VERSION}.jar \
&& curl -L https://repo1.maven.org/maven2/org/apache/logging/log4j/log4j-web/2.17.2/log4j-web-2.17.2.jar -o \
"${SPARK_HOME}"/jars/log4j-web-2.17.2.jar

# Download iceberg spark runtime
RUN curl https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-${SPARK_MAJOR_VERSION}_${SCALA_VERSION}/${ICEBERG_VERSION}/iceberg-spark-runtime-${SPARK_MAJOR_VERSION}_${SCALA_VERSION}-${ICEBERG_VERSION}.jar \
-Lo "${SPARK_HOME}"/jars/iceberg-spark-runtime-${SPARK_MAJOR_VERSION}_${SCALA_VERSION}-${ICEBERG_VERSION}.jar

# Download AWS bundle
RUN curl -s https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-aws-bundle/${ICEBERG_VERSION}/iceberg-aws-bundle-${ICEBERG_VERSION}.jar \
-Lo "${SPARK_HOME}"/jars/iceberg-aws-bundle-${ICEBERG_VERSION}.jar

ENV PATH="${SPARK_HOME}/sbin:${SPARK_HOME}/bin:${PATH}"

COPY entrypoint.sh /opt/

ENTRYPOINT [ "/opt/entrypoint.sh" ]
