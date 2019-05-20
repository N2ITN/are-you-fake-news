
docker-compose build
docker tag docker_ayfn-api gojira00/ayfn_api
docker push gojira00/ayfn_api

docker tag docker_web gojira00/ayfn_web:
docker push gojira00/ayfn_web


kubectl apply -f yaml

# gcloud container node-pools create n1-standard-2-pool \
#    --cluster  standard-cluster-1	  \
#    --zone us-west2-a \
#    --machine-type n1-standard-2  \
#    --num-nodes 1 \
#    --scopes https://www.googleapis.com/auth/devstorage.read_write