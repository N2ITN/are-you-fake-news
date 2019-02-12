FROM python:3.6-slim
RUN pip install  beautifulsoup4==4.7.1 \
    certifi==2018.11.29 \
    chardet==3.0.4 \
    idna==2.8 \
    numpy==1.16.1 \
    pymongo==3.7.2 \
    requests==2.21.0 \
    scikit-learn==0.20.2 \
    scipy==1.2.1 \
    singledispatch==3.4.0.3 \
    six==1.12.0 \
    sklearn==0.0 \
    soupsieve==1.7.3 \
    urllib3==1.24.1

RUN pip install newspaper3k  fake_useragent
RUN pip install httplib2


COPY . .
CMD python3 labels_MBFC.py
