FROM python:3.6-slim

RUN pip install tensorflow==1.5.0 

RUN pip install nltk==3.2.5 \
    h5py==2.7.1 \ 
    tldextract \
    unidecode
RUN pip install flask

COPY . .

CMD python lambda_function.py