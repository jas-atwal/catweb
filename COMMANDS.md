## SET-UP

export DTR=dtr.west.us.se.dckr.org
echo $DTR

docker login $DTR -u <uname> -p <password>

export DOCKER_CONTENT_TRUST=1
echo $DOCKER_CONTENT_TRUST

## BUILD
cd ~/Documents/Docker/Demonstrations
git clone https://github.com/jas-atwal/catweb.git

docker build --no-cache -t catweb .
docker image ls | grep catweb

docker-compose up
docker run -d -p 5001:5000 --name catweb -v $PWD:/usr/src/app catweb:latest

## COPY URLs
cp ../app.py app.py

"https://media.giphy.com/media/H4DjXQXamtTiIuCcRU/giphy.gif",
"https://media.giphy.com/media/MCfhrrNN1goH6/giphy.gif",
"https://media.giphy.com/media/VbnUQpnihPSIgIXuZv/giphy.gif",
"https://media.giphy.com/media/LqON4xbn2u0JDWRniQ/giphy.gif",
"https://media.giphy.com/media/IWG1kktEJFFDy/giphy.gif",
"https://media.giphy.com/media/QGwIkEl3QbIY0/giphy.gif",
"https://media.giphy.com/media/2eKoCnqFwHpD5W7RW6/giphy.gif",
"https://media.giphy.com/media/1BGwLa5CRz8pZK6bbH/giphy.gif",
"https://media.giphy.com/media/11s7Ke7jcNxCHS/giphy.gif",
"https://media.giphy.com/media/vFKqnCdLPNOKc/giphy.gif",
"https://media.giphy.com/media/Nm8ZPAGOwZUQM/giphy.gif",
"https://media.giphy.com/media/Jjo6WPW26zDdS/giphy.gif"

docker-compose up

docker stack deploy -c docker-compose.yml catweb
docker container ls

docker container kill <CONTAINER ID>
docker ps

## SHARE
docker tag catweb:latest $DTR/se-jasatwal/catweb:latest
docker push $DTR/se-jasatwal/catweb:latest

## RUN
kubectl create deployment catweb --image=dtr.west.us.se.dckr.org/se-prod-jasatwal/catweb
kubectl get deploy

kubectl expose deployment catweb --port=5000 --type=LoadBalancer
kubectl get pod
kubectl get svc




