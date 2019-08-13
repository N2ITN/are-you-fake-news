FROM python:3.6-slim
RUN pip install Flask==0.12.2 \
    requests>=2.20.0 \
    tldextract==2.2.0 
    

RUN pip install newspaper3k pandas pymongo langdetect unidecode

WORKDIR /opt/
COPY . .

CMD python3  lambda_function.py

