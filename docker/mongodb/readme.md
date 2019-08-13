To create a persistent volume for mongo:

`docker volume create mongodbdata`

To run a mongo container on standard mongo port:
`docker run -p 27017:27017 -v mongodbdata:/data/db --rm -it mongo`
