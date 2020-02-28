FROM puckel/docker-airflow

USER root

COPY requiriments.txt .

RUN apt-get update && \
echo Y | apt install python3-pip && \
pip install -U pip && \
pip install -r requiriments.txt
