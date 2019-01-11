FROM python:3.6.4-slim as base
FROM base as builder

RUN mkdir /install
WORKDIR /install

RUN apt-get update \
    && apt-get install -y build-essential pkg-config python-dev \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt -t /install

# Use the base container again but this time without the build cache
# created by pip - just copy the installed packages into the correct 
# location.

FROM base

COPY --from=builder /install/ /usr/local/lib/python3.6/site-packages/

RUN apt-get update \
    && apt-get install -y build-essential pkg-config python-dev \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["python"]
CMD ["main.py"]
