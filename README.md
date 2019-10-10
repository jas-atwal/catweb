# _Build, Share, Run, any app, anywhere_, with **Docker Enterprise Platform**

This demo will take you through a process of building and testing a web application locally.  We will be using **Docker Desktop Enterprise** `(DDE)` to scaffold an application, we'll then push the docker image up to a private image registry (signing the image using **Docker Content Trust** `(DCT)`), and automatically scan and promote the repository using **Docker Trusted Registry** `(DTR)`.  Once we have completed this phase of the development process we will run the web application **Docker Universal Control Plane** `(UCP)` on a **_Kubernetes_** cluster.

> (NB we can also use Docker Swarm as the orchestration engine (works great for Windows workloads as well as linux based workloads).

## Demo setup

1. Ensure Docker Desktop Enterprise is installed on your machine. If you are using Docker for Windows or Docker for Mac, you're good to go.  If not, you can download DDE from https://hub.docker.com/editions/community/docker-desktop-ent

2. Ensure that you have login credentials for Docker Enerprise Platform 3.0 hosted at https://ucp.west.us.se.dckr.org/

3. Create a `respository` named `catweb` within `DTR` (https://dtr.west.us.se.dckr.org/) and set-up `mirroring` to `DockerHub`, a `promotion` to a production namespace, and optionally a webhook to `Slack`.

4. Within a `terminal` set your env variable for `DTR` and login to `DTR`

```bash
$ export DTR=dtr.west.us.se.dckr.org
$ echo $DTR
$ docker login $DTR -u <uname> -p <password>
```

5. **Optional** - _Enable and disable content trust per-shell or per-invocation_
In a shell, you can enable content trust by setting the DOCKER_CONTENT_TRUST environment variable. Enabling per-shell is useful because you can have one shell configured for trusted operations and another terminal shell for untrusted operations. You can also add this declaration to your shell profile to have it turned on always by default.

To enable `docker content trust` in a bash shell enter the following commands to set the env var and view it

```bash
$ export DOCKER_CONTENT_TRUST=1
$ echo $DOCKER_CONTENT_TRUST
1
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
Cloning into 'catweb'...
remote: Enumerating objects: 6, done.
remote: Counting objects: 100% (6/6), done.
remote: Compressing objects: 100% (6/6), done.
remote: Total 291 (delta 2), reused 0 (delta 0), pack-reused 285
Receiving objects: 100% (291/291), 59.90 KiB | 285.00 KiB/s, done.
Resolving deltas: 100% (161/161), done.
```

List the files within the directory

```bash
$ cd catweb
$ ls
COMMANDS.md             README.md               catweb-deployment.yaml  expose-service.yaml     src
Dockerfile              app.py                  docker-compose.yml      requirements.txt        templates
```

> Notice that we have a `Dockerfile` and a `docker-compose.yaml` file

2. Within `VS Code` open the `catweb` folder, then open the `Dockerfile` and explain the how the app is `built`.  You can also show the source code if you wish

3. `Build` the app (explain that Docker is going through each step within the Dockerfile in the specified order), and use the `docker image` command to view the details of the built image

```bash
$ docker build --no-cache -t catweb .
Successfully built fd80b366dad9
Successfully tagged catweb:latest
Tagging alpine@sha256:72c42ed48c3a2db31b7dafe17d275b634664a708d901ec9fd57b1529280f01fb as alpine:latest
```

Let's view the generated `image`

```bash
$ docker image ls | grep catweb
catweb                                       latest                    fd80b366dad9        2 minutes ago       74.1MB
```

4. Now that the image has been built, we can run the image as a container using `docker-compose`.  Open the `docker-compose.yaml` file within `VS Code` and describe the contents.  Now let's `run` the app on `Docker Swarm` as the `orchestration engine` using the commands contained within the  `docker-compose` file.

```bash
$ docker-compose up
WARNING: The Docker Engine you're using is running in swarm mode.

Compose does not use swarm mode to deploy services to multiple nodes in a swarm. All containers will be scheduled on the current node.

To deploy your application across the swarm, use `docker stack deploy`.

Creating catweb_web_1 ... done
Attaching to catweb_web_1
web_1  |  * Serving Flask app "app" (lazy loading)
web_1  |  * Environment: development
web_1  |  * Debug mode: on
web_1  |  * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
web_1  |  * Restarting with stat
web_1  |  * Debugger is active!
web_1  |  * Debugger PIN: 316-525-960
```

Open a second `terminal` and view the running container using

```bash
$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED              STATUS              PORTS                    NAMES
7c9ba2ff21b2        catweb_web          "python3 /usr/src/ap…"   About a minute ago   Up About a minute   0.0.0.0:5000->5000/tcp   catweb_web_1
```

5. Open a web browser and show the app running at http://localhost:5000

6. Open the `templates/index.html` file within `VS Code` and update the `html` tag `<h4>Catweb - Curated Cat Gifs!</h4>` by adding your name

```html
<h4>Catweb - Jas' Curated Cat Gifs!</h4>
```

7. `Refresh` the web page at http://localhost:5000 and notice the change.

8. Stop the container using `CTRL+C`

```bash
^CGracefully stopping... (press Ctrl+C again to force)
Stopping catweb_web_1 ... done
```

8. Let's test the running of the app within multiple containers (three in our case) using `docker stack deploy`, and `docker swarm` for orchestration.  We can check the running containers using `docker ps` or `docker container ls`

**Note** We can also run the containers locally using _Kubernetes_ as the orchestrator

```bash
$ docker stack deploy -c docker-compose-prod.yml catweb 
Creating network catweb_default
Creating service catweb_web
```

10. Let's view the app at http://localhost:5000.  Refresh the browswer and notice the `Container ID` changes occassionally.  This is because we are running three instances of the application in three separate networked containers and the traffic is being load balanced between them.

11. View the three running containers

```bash
$ docker ps             
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
438d7ec74910        catweb:latest       "python3 /usr/src/ap…"   4 minutes ago       Up 4 minutes        5000/tcp            catweb_web.1.5bqnigtauc6ewd1jrts10lm7v
a6d46717c3e1        catweb:latest       "python3 /usr/src/ap…"   4 minutes ago       Up 4 minutes        5000/tcp            catweb_web.2.uvcfnuaxsyg0wffosupokrt5q
17665d8af3c3        catweb:latest       "python3 /usr/src/ap…"   4 minutes ago       Up 4 minutes        5000/tcp            catweb_web.3.azc8ed275lfeyzwfd1xap38rd
```

11. Let's bring one of the containers identified in step 11 down and then check to see there `STATUS`

```bash
$ docker container kill 438d7ec74910
438d7ec74910
```

12. Let's check the running containers

```bash
$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
8610e3297c89        catweb:latest       "python3 /usr/src/ap…"   8 seconds ago       Up 4 seconds        5000/tcp            catweb_web.1.p9o12hs072rbzfy27cjm10ocr
a6d46717c3e1        catweb:latest       "python3 /usr/src/ap…"   5 minutes ago       Up 5 minutes        5000/tcp            catweb_web.2.uvcfnuaxsyg0wffosupokrt5q
17665d8af3c3        catweb:latest       "python3 /usr/src/ap…"   5 minutes ago       Up 5 minutes        5000/tcp            catweb_web.3.azc8ed275lfeyzwfd1xap38rd
```

> Notice how a new container has been stood up in place of the container that we killed and has only been up a few seconds

We are now ready to share the image using `Docker Trusted Registry `, during which we will also `sign` and `scan` the image for `vulnerabilities`.

## Share

Now that the docker image has been built and we have successfully tested the running of the `catweb` application locally, we can push the image up to `Docker Trusted Registry` so that we can sign, scan, and promote the image from `dev` through to `production` for final deployment.

1. We need to `tag` the image and then `push` this tagged image to our private registry `(DTR)` ensuring that you use your own namespace (replace se-jasatwal with your namespace)

```bash
$ docker tag catweb:latest $DTR/se-jasatwal/catweb:latest
$ docker image ls | grep catweb                          
catweb_web                                   latest                    cc5142167446        51 minutes ago      74.1MB
catweb                                       latest                    ebbdcec5a92d        About an hour ago   74.1MB
dtr.west.us.se.dckr.org/se-jasatwal/catweb   latest                    ebbdcec5a92d        About an hour ago   74.1MB
```

```bash
$ docker push $DTR/se-jasatwal/catweb:latest
The push refers to repository [dtr.west.us.se.dckr.org/se-jasatwal/catweb]
aa9ff091b287: Pushed 
164e79b62389: Pushed 
2f6e52a272df: Pushed 
8d4536d51aeb: Pushed 
13806d62f1e3: Pushed 
226cecc8e243: Pushed 
03901b4a2ea8: Layer already exists 
latest: digest: sha256:2d9db17f7849327fe7c53e5e90e3b9c7398820acd189bc24a97536f59742f3c3 size: 1783
Signing and pushing trust metadata
Enter passphrase for repository key with ID 7d9b31d: 
Successfully signed dtr.west.us.se.dckr.org/se-jasatwal/catweb:latest
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

Click on `Repositories` and within the `Filter by: All Namespaces` enter your `namespace` name, select the `catweb` repositories and select the `tag` first to show the image that you just uploaded.  Then discuss the automation of:

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

1. Create a `Kubernetes deployment` using the `image` that you pushed up to `DTR` and check it exists

```bash
$ kubectl create deployment catweb --image=$DTR/se-jasatwal/catweb
deployment.apps/catweb created
$ kubectl get deploy | grep catweb
catweb      1/1     1            1           30s
```
> Where `se-jasatwal` is your namespace in `DTR`.
> If you have not set the `DTR environment variable` please substitute `$DTR` with `dtr.west.us.se.dckr.org`

2. Create a `Kubernetes service` exposing `port 5000` and using type `LoadBalancer`

```bash
$ kubectl expose deployment catweb --port=5000 --type=LoadBalancer
service/catweb exposed
```

3. Check to see if the container is running

```bash
$ kubectl get pod | grep catweb
catweb-5c6d4b9c95-z8f4f      1/1     Running            0          5m49s
```

4. Bring back the details of the service so that you can copy the `EXTERNAL IP` address which you will need in the next step

```bash
$ kubectl get svc
$ kubectl get svc | grep catweb
catweb       LoadBalancer   10.96.33.124   a3c5da531eb2111e9a6fb0242ac11000-757615726.us-west-2.elb.amazonaws.com   5000:35435/TCP   3h27m
```

> If the EXTERNAL_IP is showing as pending, please wait a few seconds and run the `kubectl get svc | grep catweb` command again until it returns a string as above.

5. In a web browser navigate to http://<external_ip>:5000.  View your newly deployed production application running on a `Kubernetes cluster` on `AWS` via the `Docker Enterprise Platform`.

> NOTE: the external_ip address in the example above is _a3c5da531eb2111e9a6fb0242ac11000-757615726.us-west-2.elb.amazonaws.com_

## Congratulations!!! :tada:

**You have successcully _containerised an application, tested it locally, pushed it up to a private registry, signed, scanned, and promoted the image, then deployed the application to Kubernetes_.   All using the Docker Enterprise Platform - the only end-to-end secure software supply chain from DEV to PROD!** :grin:





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

## --------------------------------------------------------------------------

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



