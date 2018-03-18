FROM revolutionsystems/python:3.6.3-wee-optimized-lto

# Default starting args
ARG PORT=5000
ENV PORT=$PORT
ENV GUNICORN_WORKERS=16
ENV GUNICORN_BIND=0.0.0.0:$PORT
ENV GUNICORN_TIMEOUT=28
# ENV GUNICORN_PRELOAD_APP=true
ENV GUNICORN_WORKER_CLASS=gaiohttp

# Build project 
COPY "" /opt/fakenews/
RUN pip install /opt/fakenews
RUN pip install gunicorn

# Setup filepaths
WORKDIR /opt/fakenews/web
RUN generate_gunicorn_conf
EXPOSE $PORT

# Start the party
ENTRYPOINT gunicorn --config gunicorn.conf app:APP
