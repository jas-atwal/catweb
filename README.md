# CatWeb - Build, Share, and Run any app, anywhere, with Docker Enterprise Platform

This demo will take you through a process of building and testing a web application locally using Docker Desktop Enterprise (DDE), pushing the docker image up to our private registry for scanning, signing, and promotions etc., in Docker Trusted Registry (DTR), and then running the web application via a container on Swarm or vanilla upstream Kubernetes through Docker Universal Control Plane (UCP).

## Demo setup

1. Ensure Docker Desktop Enterprise is installed on your machine. If you are using Docker for Windows or Docker for Mac, you're good to go.  If not, you can download DDE from https://hub.docker.com/editions/community/docker-desktop-ent

2. Ensure that you have login credentials for Docker Enerprise Platform 3.0 hosted at https://ucp.west.us.se.dckr.org/

3. Create a repository named `catweb` in your `namespace` in Docker Trusted Registry https://dtr.west.us.se.dckr.org/

4. Set your env variable for DTR and DCT

```bash
$ export DTR=dtr.west.us.se.dckr.org
$ echo $DTR
$ export DOCKER_CONTENT_TRUST=1
$ echo $DOCKER_CONTENT_TRUST
```

5. Open a terminal and `cd` to where you want to `git clone` the GitHub repo to, then `cd` to the app folder

```bash
$ git clone https://github.com/jas-atwal/catweb.git
$ cd catweb
```

## Running the demo

There are two parts to the demo.  The first part will take you through the process of quickly creating a net new cloud native application in a matter of seconds.  The process takes you through scaffolding an application based on the Cloud Native Application Bundle (CNAB) specification using Docker Application Designer within Docker Desktop Enterprise.  The second part will go through the process of using 

This demo is designed to show a build, ship, run workflow using a simple Flask-based web app, `catweb`.

The basic flow is to intially build and run the app locally using Docker Desktop Enterprise, modify the web template to show how hot mounting a volume works, build an updated image, push to Docker Trusted Registry, then deploy on AWS using Docker Universal Control Plane.

## Build #1 - Application Designer

1. Select the `Moby` icon in your system tray and navigate around the interesting options, explaining each one in turn.
2. Select `Design new application...`, `Custom application` and explain the different available `services` and associated `ports` etc.
4. Select the back icon `<` and then select `Choose a template`
5. Select `Flask / NGINX / MySQL application`, leave the ports as default and click `Continue`
6. Enter a name `demoApp` and select `Scaffold`
7. Select `Show logs` and describe the process that DDE is going through
8. Select `Hide logs` (optional), `Run application`, view the application by opening a web browser and entering http://localhost
9. Select `Open in Visual Studio Code` and describe the folder and file structure, and the docker files that were generated

We have not had to learn how to create our Dockerfile(s), docker-compose.yaml, or create the folder and file structure, a bonus being that we have a skeleton application which is up and running in less than a minute.

Now that we have our scaffolded (skeleton) Flash / NGINX / MySQL Server application, we can build upon this and create our net new cloud native applications.  

10. `Stop` the application, and then `exit` the Application Designer UI

## Build #2 - Docker Desktop Enterprise

1. Open a terminal and `$ ls` within the `catweb` directory (explain what the Dockerfile and docker-compose file do!)

2. Open the catweb diretory within VS Code, and show and explain the Dockerfile and how the app is built, you can also show the source code if you wish.

3. Build the app (explain that Docker is going through each step within the Dockerfile in the specified order)

```bash
$ docker build --no-cache -t catweb .
$ docker image ls | grep catweb
```

4. Run the app and mount the local directory into the source code directory in the container

```bash
$ docker run -d -p 5001:5000 --name catweb -v $PWD:/usr/src/app catweb:latest
$ docker ps
```

> Note: the volume mount is attaching itself but the live update is not working!

5. Open a web browser and show the app running at http://localhost:5001.  You will notice the images are not displaying!

6. Stop the container

```bash
$ docker ps
$ docker container stop catweb
```

6. Switch back to VS Code and edit the `index.html` file in the `templates` directory. Usually I change it by using an attendee's name in the title e.g. "Mandy's Random Cat Gif's". Save your changes.

7. Edit the `app.py` file in the root `catweb` directory, delete the URL's and replace them with the following.  Save your changes.

```
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
```

**Note**: If you using the terminal to make your edits, you will have done a `cd` into the `templates` directory to edit the file, make sure to `cd` back into the `catweb` directory before rebuilding the image in a few steps

7. Switch back to the web browser and show how the change you made is immediately reflected in the running container.

8. Switch back to the terminal and build a new version of the catweb image.

**Note**: I usually tag the image w/ the name I used when I edited the `index.html` file so it's easier to remember which one to deploy

```bash
$ docker build -t catweb:mandy .
```

9. This time, use the `docker-compose.yaml` file to run the container ensuring that you are in the `catweb` directory within your terminal

```bash
$ docker-compose up -d
```

## Share

Now that the docker image has been built and we have successfully tested the running of the `catweb` application locally, let's push it up to Docker Trusted Registry so that we can sign, scan, and promote the image from `dev` through to `production` for final deployment.

1. We need to `tag` the image and then `push` this tagged image to our private Docker Trusted Registry (DTR).

```bash
$ docker tag catweb:latest $DTR/se-jasatwal/catweb:mandy
$ docker push $DTR/se-jasatwal/catweb:mandy
```

**Note**: Replace `se-jasatwal` with your own namespace you have within DTR
**Note**: If you get an error saying you need to authenticate, you'll need to log in to the DTR server

```bash
$ docker login $DTR -u <uname> -p <password>
```

2. In a web browser navigate to https://dtr.west.us.se.dckr.org/. If prompted to log in, please do so

	Click on `Repositories` and show the image you just uploaded
	Discuss:

```text
image signing
image scanning,
image promotions and
image mirroring
webhooks
```

## Run

Now that the image has been pushed to our private registry, has been signed, scanned, and promoted through relevant stages of our development lifcycle, Let's run the web application within a container on Kubernetes via Docker Unviversal Control Plane.

1. In a web browser navigate to https://ucp.west.us.se.dckr.org/. If prompted to log in, please do so

2. From the left menu, click `Swarm`, then `Services`

**Note**: Sometimes the left menu is blank, simply reload the page if this happens

3. Click the `Create` button and fill in the following values replacing `se-jasatwal` with your `namespace`

- Image name: `dtr.west.us.se.dckr.org/se-jasatwal/catweb:mandy`
- Under `Network` select `Add Port+`
- Enter the port numbers `5001`, and `5000` in the `source` and `target` fields respectively
- Under `Labels` add two lables:
	- `interlock.hostname` and `www`
	- `interlock.domain` and `catweb.demo`

**Note**: Make sure to click the plus after each one

4. Click `Create`

5. After the container is successfully deployed, navigate in the web browser to http://www.catweb.demo. This will navigate to your newly deployed container running on AWS via Docker Enterprise Platform.

> Congratulations!!

## Post Demo Clean-up

**Note**: Do this after EACH demo

1. Manually delete running swarm container from UCP
2. Manually delete tagged catweb:latest image from DTR
3. Remove all images and containers

```bash
$ docker image rm dtr.west.us.se.dckr.org/se-jasatwal/catweb
$ docker container rm catweb -f
$ docker image rm catweb
$ docker image ls | grep catweb
$ docker image prune -a
```

4. Remove the `demoApp` application

```bash
rm -p /Users/jas.atwal/Documents/Docker/Demonstrations/app-designer/demoApp
```

**Note**: The location of your Application Designer application files will differ from that above
