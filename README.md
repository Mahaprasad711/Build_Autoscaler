# Build Autoscaler

## This project demonstrates how to automatically scale a ResNet18 image classification service running on Kubernetes. We use custom monitoring and autoscaling so the system can react to real-time performance, keeping response times low—even as the load changes. You’ll find everything needed to build, deploy, monitor, and run both a custom latency-based autoscaler and the standard Kubernetes HPA, along with clear steps for reproducing our results and experiments.
## Clone the Project

```
git clone https://github.com/Mahaprasad711/Build_Autoscaler.git
```

## Start Minikube

```
minikube start --cpus=4 --memory=8g
```

- Adjust CPUs and memory for your hardware (4 CPUs/8GB RAM recommended).

## Use Minikube's Docker Daemon

This ensures images are built inside Minikube and accessible to Kubernetes.

```
& minikube -p minikube docker-env | Invoke-Expression
```

## Build Docker Images

```
docker build -t resnet-server:latest ./server
```

*Only **`resnet-server`** is needed for core functionality.*

## Deploy Kubernetes Resources

```
kubectl apply -f k8/serverDeployment.yaml
```

*Wait for pods to reach **`Running`** state:*

```
kubectl get pods
```

## Deploy Monitoring Stack (Prometheus & Grafana)

If not already installed:

```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/prometheus -n monitoring --create-namespace
helm install grafana grafana/grafana -n monitoring
```

*Wait for all monitoring pods to show **`Running`** in*

```
kubectl get pods -n monitoring
```

## Expose Monitoring UIs

You can use the `port-forward.bat` script for convenience. Double-click to open all required ports in separate terminals automatically.

**Manual alternative (if needed):**

```
kubectl -n monitoring port-forward svc/grafana 3000:80
kubectl -n monitoring port-forward deploy/prometheus-server 9090
kubectl port-forward svc/resnet-server-service 8001:8001
```

## Access Dashboards and Metrics

- Grafana: [http://localhost:3000](http://localhost:3000)
  - Default user: `admin` (password from k8s secret; see below)
- Prometheus: [http://localhost:9090](http://localhost:9090)
- ResNet Inference API: [http://localhost:8001/infer](http://localhost:8001/infer)

## Get Grafana Admin Password

```
kubectl get secret --namespace monitoring grafana -o jsonpath="{.data.admin-password}" | base64 --decode
```

*Or, on Windows PowerShell:*

```
kubectl get secret --namespace monitoring grafana -o jsonpath="{.data.admin-password}"
# Then decode manually using online tool or PowerShell base64 decoder.
```

## Run the Load Tester

Navigate to the `client` directory:

```
cd client
python resnet_test.py
```

- This will send image classification requests to the server.
- The workload pattern can be set in `workload.txt`.

## Run the Autoscaler

In the project root, run:

```
python autoscaler.py
```

- Autoscaler will monitor latency and scale pods up/down accordingly (via Prometheus and `kubectl`).

## To Use HPA for Comparison

Enable metrics server (if not already):

```
minikube addons enable metrics-server
```

Create HPA for `resnet-server`:

```
kubectl autoscale deployment resnet-server --cpu-percent=50 --min=1 --max=4
```

Monitor with:

```
kubectl get hpa
kubectl get pods -l app=resnet-server
```

## Collecting Results

- Open Grafana at [http://localhost:3000](http://localhost:3000)
- View/export graphs (latency, pod count, etc) for both autoscaler and HPA runs.
- For best results, screenshot panels or use Grafana's export features.


