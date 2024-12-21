from aiohttp import web
import sys 

port = 0
async def handle_get(request):
    global port
    response_data = {"message": f"Hello from slave {port}"}
    return web.json_response(response_data)

async def handle_post(request):
    global port
    try:
        data = await request.json()
        print(f"Received data: {data}")
        
        response_data = {
            "message": "hello from {port}",
            "your_data": data
        }
        return web.json_response(response_data)
    
    except Exception as e:
        return web.json_response(
            {"error": "Invalid JSON payload", "details": str(e)},
            status=400
        )

app = web.Application()

app.router.add_get("/", handle_get)
app.router.add_post("/", handle_post)

if __name__ == "__main__":
    if len(sys.argv) == 4:
        print(" ".join(sys.argv))
        port = int(sys.argv[3])
        web.run_app(app, host="127.0.0.1", port=port)
    else:
        print("Provide the configuration file")
