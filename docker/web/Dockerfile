FROM python:3.6-slim
RUN pip install  boto3==1.4.4 \
    Flask==0.12.2 \
    requests>=2.20.0 \
    tldextract==2.2.0 \
    WTForms==2.1

RUN pip install newspaper3k pandas pymongo langdetect unidecode


COPY . .
CMD python3  app.py

