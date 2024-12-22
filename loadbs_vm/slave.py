from aiohttp import web
import sys 

async def handle_get(request):
    response_data = {"message": f"Hello from slave "}
    return web.json_response(response_data)

async def handle_post(request):
    try:
        data = await request.json()
        response_data = {
            "message": "hello from ",
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
        web.run_app(app, host="127.0.0.1", port=8080)
