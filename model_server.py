
from torchvision.models import resnet18, ResNet18_Weights
import torch
import base64
from PIL import Image
import io
import numpy as np
from aiohttp import web
import time


preprocessor = ResNet18_Weights.IMAGENET1K_V1.transforms()

# These two lines are important, as your pods will have CPU request and CPU limit of "1" (for memory also use "1G" for both request and limit)
torch.set_num_interop_threads(1)
torch.set_num_threads(1)


resnet_model = resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)
resnet_model.eval()



def infer(d):
    t = time.perf_counter()
    decoded = base64.b64decode(d["data"])
    inp = Image.open(io.BytesIO(decoded))
    inp = np.array(preprocessor(inp))
    inp = torch.from_numpy(np.array([inp]))
    
    preds = resnet_model(inp)
    labels = []
    for idx in list(preds[0].sort()[1])[-1:-6:-1]:
        labels.append(ResNet18_Weights.IMAGENET1K_V1.meta["categories"][idx])
    print("Server-side processing took:", round(time.perf_counter() - t, 3))
    return labels
  
  
app = web.Application()


async def infer_handler(request):
    req = await request.json()
    return web.json_response(infer(req))
    

app.add_routes(
    [
        web.post("/infer", infer_handler),
    ]
)

if __name__ == '__main__':
    web.run_app(app, host="0.0.0.0", port=8000, access_log=None)


   
    
   
   
   
   
   
   