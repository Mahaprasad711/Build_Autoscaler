# Build_Autoscaler

## Clone the Project
code:
>git clone https://github.com/Mahaprasad711/Build_Autoscaler.git

## Start Minikube
code:
>minikube start

This will create a local K8s cluster inside Docker.
## Use Minikube's Docker Daemon
This ensures images are built inside Minikube and accessible to Kubernetes.

code:
>& minikube -p minikube docker-env | Invoke-Expression

## Build Docker Image
code:
>docker build -t resnet-server:latest ./server

>docker build -t resnet-client:latest ./client

Every time the code changes, it requires to be run.

## Deploy Kubernetes resources
code:
>kubectl apply -f k8/serverDeployment.yaml

>kubectl apply -f k8/clientDeployment.yaml

Do it one time, but **you need to run it again if changes made to Yaml files**

## View logs from the client


>kubectl logs -l app=resnet-client

Expected output:

>Waiting for server to start on port 8001...

>Server is up - starting client
['apple', 'Granny Smith', 'fruit', 'red wine', 'pomegranate'] 0.243

## Tested Environment

- Docker Desktop (v24+)

- Minikube v1.33+

- kubectl v1.30+
