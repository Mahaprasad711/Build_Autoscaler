from prometheus_client import (
    Counter,
    Summary,
    start_http_server,
    generate_latest,
    CONTENT_TYPE_LATEST,
)
from torchvision.models import resnet18, ResNet18_Weights
import torch, base64, io, time
from PIL import Image

import numpy as np

from aiohttp import web



preprocessor = ResNet18_Weights.IMAGENET1K_V1.transforms()


torch.set_num_threads(1)

torch.set_num_interop_threads(1)

resnet_model = resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)
resnet_model.eval()


REQUEST_COUNT = Counter(
    "resnet_infer_requests_total",
    "Total number of inference requests received",
)
REQUEST_LATENCY = Summary(
    "resnet_infer_latency_seconds",
    "Time spent processing inference requests",
)



@REQUEST_LATENCY.time()     
def infer(d: dict):
    """Run a single ResNet-18 inference and return top-5 labels."""
    REQUEST_COUNT.inc()     

    t0 = time.perf_counter()

    decoded = base64.b64decode(d["data"])
    img = Image.open(io.BytesIO(decoded)).convert("RGB")
    tensor = preprocessor(img)
    tensor = torch.unsqueeze(tensor, 0)         

    with torch.no_grad():
        preds = resnet_model(tensor)

    top5 = preds[0].topk(5).indices
    labels = [ResNet18_Weights.IMAGENET1K_V1.meta["categories"][idx] for idx in top5]

    print("Server-side processing took:", round(time.perf_counter() - t0, 3), "s")
    return labels


app = web.Application()


async def infer_handler(request: web.Request):
    """POST /infer  →  {predictions: [...] }"""
    try:
        body = await request.json()
    except Exception:
        return web.json_response({"error": "invalid JSON"}, status=400)

    try:
        preds = infer(body)
        return web.json_response({"predictions": preds})
    except Exception as exc:
        return web.json_response({"error": str(exc)}, status=500)


async def metrics_handler(request: web.Request):
    """GET /metrics  →  Prometheus text exposition format"""
    return web.Response(body=generate_latest(), content_type=CONTENT_TYPE_LATEST)


app.add_routes(
    [
        web.post("/infer", infer_handler),
        web.get("/metrics", metrics_handler),  
    ]
)


if __name__ == "__main__":
    start_http_server(8002)  
    web.run_app(app, host="0.0.0.0", port=8001, access_log=None)
