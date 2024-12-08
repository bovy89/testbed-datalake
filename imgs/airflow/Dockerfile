FROM apache/airflow:2.10.3@sha256:a297f7672778ba65d4d95cd1fee0213133ae8d8dd176fe9a697af918f945368f

USER root

# Install OpenJDK-17
RUN apt-get update \
&& apt-get install -y openjdk-17-jdk \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64/
# RUN export JAVA_HOME

USER airflow

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt \
&& rm requirements.txt
