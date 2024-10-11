FROM apache/airflow:2.10.0@sha256:0bdad079614ecd800397966c8584a72ff568407554c81b7728560cee368cc637

USER root

# Install OpenJDK-17
RUN apt-get update \
&& apt-get install -y openjdk-17-jdk \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME
ENV JAVA_HOME /usr/lib/jvm/java-17-openjdk-amd64/
# RUN export JAVA_HOME

USER airflow

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt
