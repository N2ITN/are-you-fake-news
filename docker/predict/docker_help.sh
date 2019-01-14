docker build -t nlp_predict .
docker run -p 7007:7007 --rm -it nlp_predict