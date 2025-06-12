import requests
import cv2
import base64
import json
import time
import os

image_path = os.getenv("IMAGE_PATH", "apple.jpeg")
server_url = os.getenv("SERVER_URL", "http://resnet-server-service:8001/infer")

im = cv2.imread(image_path)
im = cv2.resize(im, dsize=(256, 256), interpolation=cv2.INTER_CUBIC)
encoded = base64.b64encode(cv2.imencode(".jpeg", im)[1].tobytes()).decode("utf-8")

t = time.perf_counter()
response = requests.post(server_url, data=json.dumps({"data": encoded}))
print(response.text, round(time.perf_counter() - t, 3))