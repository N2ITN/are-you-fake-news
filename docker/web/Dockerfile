FROM python:3.6-slim
RUN pip install  boto3==1.4.4 \
    Flask==0.12.2 \
    requests>=2.20.0 \
    tldextract==2.2.0 \
    WTForms==2.1

RUN pip install newspaper3k pandas pymongo langdetect unidecode

ENV GCSFUSE_REPO gcsfuse-jessie

RUN apt-get update && apt-get install --yes --no-install-recommends \
    ca-certificates \
    curl \
    gnupg2 \
    && echo "deb http://packages.cloud.google.com/apt $GCSFUSE_REPO main" \
    | tee /etc/apt/sources.list.d/gcsfuse.list \
    && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - \
    && apt-get update \
    && apt-get install --yes gcsfuse \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* 

WORKDIR /opt/
COPY . .
RUN mkdir /opt/static/plots
CMD python3  app.py

