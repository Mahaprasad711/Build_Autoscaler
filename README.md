# Build_Autoscaler

## Clone the Project
code:
> git clone https://github.com/Mahaprasad711/Build_Autoscaler.git

## Start Minikube
code:
> minikube start

This will create a local K8s cluster inside Docker.

## Use Minikube's Docker Daemon
This ensures images are built inside Minikube and accessible to Kubernetes.

code:
> & minikube -p minikube docker-env | Invoke-Expression

## Build Docker Images
code:
> docker build -t resnet-server:latest ./server

> docker build -t resnet-client:latest ./client

> docker build -t dispatcher:latest ./dispatcher

Every time the code changes, these commands must be re-run to rebuild the images inside Minikube.

## Deploy Kubernetes Resources
code:
> kubectl apply -f k8/serverDeployment.yaml

> kubectl apply -f k8/clientDeployment.yaml

> kubectl apply -f k8/dispatcherDeployment.yaml

Apply these once initially, and again whenever you make changes to the YAML files.

## Expose Dispatcher Service
code:
> minikube service dispatcher-service --url

This command will output a URL (e.g., `http://127.0.0.1:56006`). Use this in the `load_tester` script as the endpoint.

## Run the Load Tester
Navigate to the load tester directory:
> cd load_tester

Then run:
> python resnet_test.py

This will send image classification requests to the dispatcher and simulate variable client load.

You can customize the workload pattern in `resnet_test.py`:
```python
workload = [2, 3, 5, 5, 8, 8, 10]  # Each value represents the number of requests per second
