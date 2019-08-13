
docker-compose build
# docker tag docker_ayfn-api gojira00/ayfn_api
# docker push gojira00/ayfn_api

docker tag docker_plotter gojira00/ayfn_plotter
docker push gojira00/ayfn_plotter

docker tag docker_web gojira00/ayfn_web
docker push gojira00/ayfn_web


docker tag docker_nlp gojira00/ayfn_nlp
docker push gojira00/ayfn_nlp


docker tag docker_plotter gojira00/ayfn_plotter
docker push gojira00/ayfn_plotter
kubectl delete deployment plotter

kubectl apply -f yaml

# gcloud container node-pools create g1-small-pool \
#    --cluster  standard-cluster-1	  \
#    --zone us-west2-a \
#    --machine-type g1-small  \
#    --num-nodes 3 \
#    --scopes https://www.googleapis.com/auth/devstorage.read_write