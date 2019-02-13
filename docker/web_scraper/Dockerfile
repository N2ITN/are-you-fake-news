FROM python:3.6-slim

RUN pip install requests>=2.20.0
RUN pip install newspaper3k


COPY . .

CMD python lambda_function.py