### Glossary
* Image:	A static "blueprint" of a machine ready to instantiated.
* Container:	A runnable instance created from an image; the equivalent of a running machine.
A service comprises of 1 or more containers.
* Dockerfile:	A file with human-readable instructions on how to create an image
* Compose: A container orchestration tool provided with Docker. It allows you to set up multiple services 
in a single environment.
The service definition file is called docker-compose.yml by default.
* ECS	Amazon Elastic Container Service. Amazon's container control plane that operates on top of AWS EC2.
* Kubernetes	An enterprise-ready container orchestration platform.
Amazon provides its own Kubernetes service for AWS called EKS (Elastic Kubernetes Service).

### Useful Docker commands
[Full docs](https://docs.docker.com/engine/reference/commandline/docker/)

* ps:	Lists all running containers.
* images:	Lists all images.
* rm:	Destroys a container.
* rmi:	Destroys an image.
* exec -it <container> /bin/bash: open a shell into your running container

## Useful Docker-compose commands
[Full docs](https://docs.docker.com/compose/reference/overview/)

* up:	Builds images, instantiates containers.
* build:	Builds images.
* start:	Starts existing containers.
* stop:	Stops running containers.
* down: Stops and destroys containers and images.
* exec <service>:	Executes a command on running service and outputs the results to your terminal.
* logs:	Print container output logs.

The commands above take action against all services defined in the Docker Compose file unless a 
service name(s) is specified, i.e. docker-compose stop spyder-admin.
