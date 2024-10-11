FROM apache/airflow:2.10.0@sha256:0bdad079614ecd800397966c8584a72ff568407554c81b7728560cee368cc637

USER root

# Install OpenJDK-17
RUN apt-get update \
&& apt-get install -y openjdk-17-jdk python3 python3-pip gnupg2 wget bash tini libc6 libpam-modules krb5-user libnss3 procps net-tools gosu libnss-wrapper \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME /usr/lib/jvm/java-17-openjdk-amd64/
ENV SPARK_HOME /opt/spark

ENV SPARK_MAJOR_VERSION=3.5
ENV SPARK_HOTFIX_VERSION=2
ENV SCALA_VERSION=2.12
ENV ICEBERG_VERSION=1.6.0
ENV AWS_SDK_VERSION=1.12.238
ENV HADOOP_VERSION=3.3.6


# Install Apache Spark
# https://downloads.apache.org/spark/KEYS
ENV SPARK_TGZ_URL=https://archive.apache.org/dist/spark/spark-$SPARK_MAJOR_VERSION.$SPARK_HOTFIX_VERSION/spark-$SPARK_MAJOR_VERSION.$SPARK_HOTFIX_VERSION-bin-hadoop3.tgz \
    SPARK_TGZ_ASC_URL=https://archive.apache.org/dist/spark/spark-$SPARK_MAJOR_VERSION.$SPARK_HOTFIX_VERSION/spark-$SPARK_MAJOR_VERSION.$SPARK_HOTFIX_VERSION-bin-hadoop3.tgz.asc \
    GPG_KEY=D76E23B9F11B5BF6864613C4F7051850A0AF904D

RUN mkdir -p "${SPARK_HOME}" "${SPARK_HOME}"/python "${SPARK_HOME}"/examples "${SPARK_HOME}"/work-dir "$SPARK_HOME"/iceberg/spark-events "$SPARK_HOME"/conf \
&& chmod g+w "${SPARK_HOME}"/work-dir \
&& echo "auth required pam_wheel.so use_uid" >> /etc/pam.d/su \
&& touch "${SPARK_HOME}"/RELEASE

RUN set -ex; \
    export SPARK_TMP="$(mktemp -d)"; \
    cd $SPARK_TMP; \
    wget -nv -O spark.tgz "$SPARK_TGZ_URL"; \
    wget -nv -O spark.tgz.asc "$SPARK_TGZ_ASC_URL"; \
    export GNUPGHOME="$(mktemp -d)"; \
    gpg --batch --keyserver hkps://keys.openpgp.org --recv-key "$GPG_KEY" || \
    gpg --batch --keyserver hkps://keyserver.ubuntu.com --recv-keys "$GPG_KEY"; \
    gpg --batch --verify spark.tgz.asc spark.tgz; \
    gpgconf --kill all; \
    rm -rf "$GNUPGHOME" spark.tgz.asc; \
    \
    tar -xf spark.tgz --strip-components=1; \
    mv jars "${SPARK_HOME}"/; \
    mv bin "${SPARK_HOME}"/; \
    mv sbin "${SPARK_HOME}"/; \
    mv kubernetes/dockerfiles/spark/decom.sh /opt/; \
    mv examples "${SPARK_HOME}"/; \
    mv kubernetes/tests "${SPARK_HOME}"/; \
    mv data "${SPARK_HOME}"/; \
    mv python/pyspark "${SPARK_HOME}"/python/pyspark/; \
    mv python/lib "${SPARK_HOME}"/python/lib/; \
    mv R "${SPARK_HOME}"/; \
    chmod a+x /opt/decom.sh; \
    cd ..; \
    rm -rf "$SPARK_TMP";

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


RUN chown -R airflow:root "${SPARK_HOME}"

USER airflow

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
&& rm requirements.txt

ENV PATH="${SPARK_HOME}/sbin:${SPARK_HOME}/bin:${PATH}"
