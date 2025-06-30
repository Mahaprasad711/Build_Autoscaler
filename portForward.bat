start cmd /k "kubectl -n monitoring port-forward svc/grafana 3000:80"
start cmd /k "kubectl -n monitoring port-forward deploy/prometheus-server 9090"
start cmd /k "kubectl port-forward svc/resnet-server-service 8001:8001"

