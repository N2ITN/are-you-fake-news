FROM python:3.6-slim 

# RUN mkdir /install
# WORKDIR /install

# RUN apt-get update \
#     && apt-get install -y build-essential pkg-config python-dev \
#     --no-install-recommends 
    # && rm -rf /var/lib/apt/lists/*

# FROM base as builder

ADD requirements.txt /requirements.txt
# RUN pip install -r /requirements.txt -t /install
RUN pip install -r /requirements.txt 

# Use the base container again but this time without the build cache
# created by pip - just copy the installed packages into the correct 
# location.

# FROM base as app

# COPY --from=builder /install/ /usr/local/lib/python3.6/site-packages/

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


RUN mkdir /plots
COPY ./ /plotter/
WORKDIR /plotter

ENTRYPOINT ["python"]
CMD ["main.py"]
