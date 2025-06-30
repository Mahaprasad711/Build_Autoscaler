import time
import requests
import subprocess

PROMETHEUS_URL = "http://localhost:9090"
DEPLOYMENT_NAME = "resnet-server"
NAMESPACE = "default"
MIN_REPLICAS = 1
MAX_REPLICAS = 3
LATENCY_UPPER = 0.05   # 50 milliseconds (in seconds)
LATENCY_LOWER = 0.02   # 20 milliseconds (in seconds)
SCALE_INTERVAL = 30    # Seconds between autoscaler checks

def get_avg_latency():
    
    query = "avg_over_time(resnet_infer_latency_seconds_sum[1m]) / avg_over_time(resnet_infer_latency_seconds_count[1m])"
    url = f"{PROMETHEUS_URL}/api/v1/query"
    try:
        resp = requests.get(url, params={"query": query})
        data = resp.json()
        result = data["data"]["result"]
        if not result:
            print("[Autoscaler] No latency data yet (no load?)")
            return None
        return float(result[0]["value"][1])
    except Exception as e:
        print(f"[Autoscaler] Error querying Prometheus: {e}")
        return None

def scale_deployment(replicas):
    """
    Use kubectl to set the number of replicas for the deployment.
    """
    print(f"[Autoscaler] Scaling '{DEPLOYMENT_NAME}' to {replicas} replicas...")
    try:
        subprocess.run(
            [
                "kubectl", "scale",
                f"deployment/{DEPLOYMENT_NAME}",
                f"--replicas={replicas}",
                "-n", NAMESPACE
            ],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"[Autoscaler] Error scaling deployment: {e}")

def get_current_replicas():
    """
    Get the current number of running replicas for the deployment.
    """
    try:
        out = subprocess.check_output([
            "kubectl", "get", "deployment", DEPLOYMENT_NAME,
            "-n", NAMESPACE, "-o", "jsonpath={.status.replicas}"
        ], universal_newlines=True)
        return int(out)
    except Exception as e:
        print(f"[Autoscaler] Error getting current replicas: {e}")
        return None

if __name__ == "__main__":
    print(" External Autoscaler started. Press Ctrl+C to stop.")
    while True:
        latency = get_avg_latency()
        if latency is None:
            print(f"[Autoscaler] Waiting for valid latency data...")
            time.sleep(SCALE_INTERVAL)
            continue

        print(f"[Autoscaler] 1-minute average latency: {latency * 1000:.1f} ms")
        current_replicas = get_current_replicas()
        if current_replicas is None:
            print("[Autoscaler] Could not determine current replicas.")
            time.sleep(SCALE_INTERVAL)
            continue

        desired_replicas = current_replicas

        if latency > LATENCY_UPPER and current_replicas < MAX_REPLICAS:
            desired_replicas = min(MAX_REPLICAS, current_replicas + 1)
            print("[Autoscaler] High latency detected—scaling up.")

        elif latency < LATENCY_LOWER and current_replicas > MIN_REPLICAS:
            desired_replicas = max(MIN_REPLICAS, current_replicas - 1)
            print("[Autoscaler] Low latency detected—scaling down.")

        else:
            print("[Autoscaler] No scaling action needed.")

        if desired_replicas != current_replicas:
            scale_deployment(desired_replicas)

        time.sleep(SCALE_INTERVAL)
