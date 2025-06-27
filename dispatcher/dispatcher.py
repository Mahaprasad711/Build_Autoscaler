
from aiohttp import web
import asyncio
import aiohttp
import json

print(" Dispatcher server is starting...")


# Hardcoded list of server service URLs (we’ll improve this later)
SERVER_URLS = [
    "http://resnet-server-service:8001/infer",  # You can run multiple replicas using the same K8s service
]

# Shared queue for incoming requests
request_queue = asyncio.Queue()
current_idx = 0  # for round-robin

routes = web.RouteTableDef()


@routes.post("/dispatch")
async def handle_dispatch(request):
    data = await request.json()
    print(f" Received request in dispatcher: {len(data.get('data', ''))} bytes")
    response_data = await forward_request(data)
    return web.json_response(response_data)


async def forward_request(data):
    global current_idx
   

    # Use round-robin server selection
    url = SERVER_URLS[current_idx % len(SERVER_URLS)]
    current_idx += 1

    print(f"Forwarding request to: {url}")

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as resp:
            result = await resp.text()
            print("📡 Raw dispatcher response:", result)
            try:
                return json.loads(result)
            except:
                return {"error": "Invalid response from server", "raw": result}


app = web.Application()
app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app, host="0.0.0.0", port=9000)
