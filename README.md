# _Build, Share, Run, any app, anywhere_, with **Docker Enterprise Platform**

This demo will take you through a process of building and testing a web application locally.  We will be using **Docker Desktop Enterprise** `(DDE)` to scaffold an application, we'll then push the docker image up to a private image registry (signing the image using **Docker Content Trust** `(DCT)`), and automatically scan and promote the repository using **Docker Trusted Registry** `(DTR)`.  Once we have completed this phase of the development process we will run the web application **Docker Universal Control Plane** `(UCP)` on a **_Kubernetes_** cluster.

> (NB we can also use Docker Swarm as the orchestration engine (works great for Windows workloads as well as linux based workloads).

## Demo setup

1. Ensure Docker Desktop Enterprise is installed on your machine. If you are using Docker for Windows or Docker for Mac, you're good to go.  If not, you can download DDE from https://hub.docker.com/editions/community/docker-desktop-ent

2. Ensure that you have login credentials for Docker Enerprise Platform 3.0 hosted at https://ucp.west.us.se.dckr.org/

3. Create a `respository` named `catweb` within `DTR` (https://dtr.west.us.se.dckr.org/) and set-up `mirroring` to `DockerHub`, a `promotion` to a production namespace, and optionally a webhook to Slack

4. Set your env variable for `DTR` and `DCT` and login to `DTR`

```bash
$ export DTR=dtr.west.us.se.dckr.org
$ echo $DTR
$ docker login $DTR -u <uname> -p <password>
```

5. **Optional** - _Enable and disable content trust per-shell or per-invocation_
In a shell, you can enable content trust by setting the DOCKER_CONTENT_TRUST environment variable. Enabling per-shell is useful because you can have one shell configured for trusted operations and another terminal shell for untrusted operations. You can also add this declaration to your shell profile to have it turned on always by default.

To enable content trust in a bash shell enter the following command:

```bash
$ export DOCKER_CONTENT_TRUST=1
```

and view it to ensure that it is set.

```bash
$ echo $DOCKER_CONTENT_TRUST
```

7. Install `Visual Studio Code` from https://code.visualstudio.com/download

## Running the demo

There are two parts to the demo.  The first part will take you through the process of quickly creating a net new cloud native application in a matter of seconds.  The process takes you through _scaffolding_ an application based on the **Cloud Native Application Bundle** `(CNAB)` specification using **Docker Application Designer** within `Docker Desktop Enterprise`.  The second part will go through the process of using _GitHub_, _DDE_, _DTR_, and _UCP_.

This demo is designed to show a _build_, _share_, _run_ Docker workflow using a simple Flask-based web app, `catweb`.

The basic flow is to intially build and run the app locally using Docker Desktop Enterprise, modify the web template to show how hot mounting a volume works, pushing the image to `Docker Trusted Registry` _optionally_ signing the image with `Docker Trusted Registry`, then deploying onto `AWS` using `Docker Universal Control Plane`.

## Build #1 - Application Designer

1. Click the `Moby` icon in your system tray and navigate around the interesting options, explaining each one in turn.
2. Click `Design new application...`, `Custom application` and explain the different available `services` and associated `ports` etc.
4. Click the back icon `<` and then select `Choose a template`
5. Click `Flask / NGINX / MySQL application`, leave the ports as default and click `Continue`
6. Click a name `demoApp` and select `Scaffold`
7. Click `Show logs` and describe the process that DDE is going through
8. Click `Hide logs` (optional), `Run application`, view the application by opening a web browser and entering http://localhost
9. Click `Open in Visual Studio Code` and describe the folder and file structure, and the docker files that were generated
10. Run `docker ps` in a terminal to view the running container

We have not had to learn how to create our Dockerfile(s), docker-compose.yaml, or create the folder and file structure, a bonus being that we have a skeleton application which is up and running in less than a minute.

Now that we have our scaffolded (skeleton) Flash / NGINX / MySQL Server application, we can build upon this and create our net new cloud native application for our project

10. Within the Application Designer UI click `Stop` to stop the application, then click the back `<` chevron
11. Click the `delete` icon, `confirm and remove application`, and exit `x` the Application Designer UI

## Build #2 - Docker Desktop Enterprise

1. Open a terminal window and change directory to where you want to clone the `catweb` sample `GitHub` repo too.

```bash
$ cd ~/Documents/Docker/Demonstrations
$ git clone https://github.com/jas-atwal/catweb.git
```

List the files within the directory

```bash
$ cd catweb
$ ls
```

> Notice that we have a `Dockerfile` and a `docker-compose.yaml` file

2. Within `VS Code` open the `catweb` folder, then open the `Dockerfile` and explain the how the app is `built`.  You can also show the source code if you wish

3. `Build` the app (explain that Docker is going through each step within the Dockerfile in the specified order), and use the `docker image` command to view the details of the built image

```bash
$ docker build --no-cache -t catweb .
$ docker image ls | grep catweb
```

4. Now open the `docker-compose` file and explain how it works.  Let's `run` the app within a `container` using the built `image` as per the instructions within within the `docker-compose` file.

```bash
$ docker-compose up
```

**As an alternative to using the docker-compose file, you can run the app within a container using the command below.**
**If you want to try this you will first have to remove the existing container using `docker container rm catweb`**

```bash
$ docker run -d -p 5000:5000 --name catweb -v $PWD:/usr/src/app catweb:latest
```

> $PWD is your current working directory i.e. `catweb`

View the running container using

```bash
$ docker ps
```

5. Open a web browser and show the app running at http://localhost:5000.  You will notice the images are not displaying!

6. Stop the container `$ ^C ` using `control+c`

7. Within `VS Code` open the `app.py` file in the root `catweb` directory, delete the URL's and replace them with the following.  Save your changes.

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

**Note**: A simpler option is to copy the updated `app_new.py` within the `src` folder over the top of the existing `app.py` file within the `catweb` folder using.  Then check that the URL have changed.

```bash
$ cp src/app_new.py app.py
```

7. Run the app again using `docker-compose up`

```bash
$ docker-compose up
```

> If done correctly you should notice that the images are now fixed when you refresh the web browser at http://localhost:5000

8. Stop the container `$ ^C ` using `control+c`

9. Now that we have a working app, let's test the running of the app within multiple containers (three in our case) using `docker stack deploy`, and `docker swarm` for orchestration.  We can check the running containers using `docker ps` or `docker container ls`

```bash
$ docker stack deploy -c docker-compose.yml catweb
$ docker container ls
```

10. Let's view the app at http://localhost:5000.  Refresh the browswer and notice the `Container ID` changes occassionally.  This is because we are running three instances of the application in three separate networked containers and the traffic is being load balanced between them.

11. Let's bring one of the containers identified in step 10 down and then check to see there `STATUS`

```bash
$ docker container kill <CONTAINER ID>
$ docker ps
```

> Notice how a new container has been stood up in place of the container that we killed and has only been up a few seconds

We are now ready to share the image using `Docker Trusted Registry `, during which we will also `sign` and `scan` the image for `vulnerabilities`.

## Share

Now that the docker image has been built and we have successfully tested the running of the `catweb` application locally, we can push the image up to `Docker Trusted Registry` so that we can sign, scan, and promote the image from `dev` through to `production` for final deployment.

1. We need to `tag` the image and then `push` this tagged image to our private registry `(DTR)`.

```bash
$ docker tag catweb:latest $DTR/se-jasatwal/catweb:latest
$ docker push $DTR/se-jasatwal/catweb:latest
```

**Note**: Replace `se-jasatwal` with your own namespace you have within `DTR`
**Note**: If you get an error saying you need to authenticate, you'll need to `log in` to `DTR` using 

```bash
$ docker login $DTR -u <uname> -p <password>
```
> The `DTR` which we are using for this demo is `dtr.west.us.se.dckr.org`

> If you have enabled `DOCKER_CONTENT_TRUST=1` as an `environment varibale` then the first time you `push` an image using `content trust` on your system, the session looks like this:

```bash
Signing and pushing trust metadata
You are about to create a new root signing key passphrase. This passphrase
will be used to protect the most sensitive key in your signing system. Please
choose a long, complex passphrase and be careful to keep the password and the
key file itself secure and backed up. It is highly recommended that you use a
password manager to generate the passphrase and keep it safe. There will be no
way to recover this key. You can find the key in your config directory.
Enter passphrase for new root key with ID fa0e171:
```

Enter a passphrase when prompted.

> **_Make note of this `passphrase` as it is not retrievable if forgotten._**

Once complete you will receive a response similar to that below

```bash
Finished initializing "dtr.west.us.se.dckr.org/se-jasatwal/catweb"
Successfully signed dtr.west.us.se.dckr.org/se-jasatwal/catweb:latest
```

2. In a web browser navigate to https://dtr.west.us.se.dckr.org/. When prompted to log in, please do so

Click on `Repositories` and show the image you just uploaded and discuss the automation of:

```text
image signing
image scanning,
image mirroring
image promotions and
webhooks
```

## Run

Now that the image has been pushed to our private registry, has been signed, scanned, and promoted through to our production namespace, let's run the web application within a container on `Kubernetes` via **Docker Unviversal Control Plane** `UCP`.

> We can run the container using a `Kubernetes yaml` file or alternatively via the `command line`.  We will use the latter!

1. Create a `Kubernetes deployment` and check it exists

```bash
$ kubectl create deployment catweb --image=$DTR/se-jasatwal/catweb
$ kubectl get deploy
```
> Where `se-jasatwal` is your namespace in `DTR`.
> If you have not set the `DTR environment variable` please substitute `$DTR` with `dtr.west.us.se.dckr.org`

2. Create a `Kubernetes service` exposing `port 5000` and using the `LoadBalancer`

```bash
$ kubectl expose deployment catweb --port=5000 --type=LoadBalancer
```

3. Check to see if the container is running

```bash
$ kubectl get pod
```

4. Bring back the details of the service so that you can copy the `EXTERNAL IP` address which you will need in the next step

```bash
$ kubectl get svc
```

5. In a web browser navigate to http://<external_ip>:5000.  View your newly deployed production application running on a `Kubernetes cluster` on `AWS` via the `Docker Enterprise Platform`.

> _**Congratulations!!**_

**Docker Enterprise Platform - the only end-to-end secure software supply chain from dev to prod!**

## Post Demo Clean-up (Needs updating)!

**Note**: Do this after EACH demo

1. Manually delete running swarm container from UCP
2. Manually delete tagged catweb:latest image from DTR
3. Remove all images and containers

```bash
$ docker image rm dtr.west.us.se.dckr.org/se-jasatwal/catweb
$ docker stack rm catweb
$ docker container rm catweb -f
$ docker image rm catweb
$ docker image ls | grep catweb
$ docker image prune -a
$ cd ..
$ rm -R ~/Documents/Docker/Demonstrations/catweb/
```

**Note**: The location of your `catweb` application files will differ from that above

4. Remove the `demoApp` application

```bash
$ rm -R ~/Documents/Docker/Demonstrations/app-designer/demoApp
```

**Note**: The location of your `Application Designer` application files will differ from that above

## ------------------------------------------------------------------------------------------

## Instructions for Deploying to Swarm

1. In a web browser navigate to https://ucp.west.us.se.dckr.org/. If prompted to log in, please do so

2. From the left menu, click `Swarm`, then `Services`

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



