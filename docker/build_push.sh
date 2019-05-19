
docker-compose build
docker tag docker_web gojira00/ayfn_web
docker push gojira00/ayfn_web

docker tag docker_plotter gojira00/ayfn_plotter
docker push gojira00/ayfn_plotter

kubectl apply -f docker/yaml/