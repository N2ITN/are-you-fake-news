
docker-compose build
docker tag docker_web gojira00/ayfn_web
docker push gojira00/ayfn_web

docker tag docker_plotter gojira00/ayfn_plotter
docker push gojira00/ayfn_plotter

kubectl apply -f yaml


# gcloud container node-pools create n1-standard-2-pool \
#    --cluster  standard-cluster-1	  \
#    --zone us-west2-a \
#    --machine-type n1-standard-2  \
#    --num-nodes 1 \
#    --scopes https://www.googleapis.com/auth/devstorage.read_write