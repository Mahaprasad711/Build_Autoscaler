# Build_Autoscaler

## Clone the Project

>git clone https://github.com/Mahaprasad711/Build_Autoscaler.git

## Start Minikube

>minikube start
This will create a local K8s cluster inside Docker.
## Use Minikube's Docker Daemon
This ensures images are built inside Minikube and accessible to Kubernetes.


>& minikube -p minikube docker-env | Invoke-Expression


### Build the containers

Run the following command in the root folder:

`docker-compose up --build`

The server should start and client should now try to connect and display results of image recognition.

You can also run the client container in docker desktop to get the results
