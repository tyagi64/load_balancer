from aiohttp import web
import sys 
import os
import signal
import requests

config_file =[]
hostname = ''
processes = []
num_sys = 0
round_rob = 0
request_url_base = f"http://"

async def handle_exit(request):
    global round_rob,num_sys,request_url_base
    params = None
    params = request.rel_url.query
    try:
        if None != params:
                params = dict(params)
        response = requests.get(f"{request_url_base}{processes[round_rob]}/exit",params=params)
        round_rob = (round_rob+1)%num_sys
        if response.status_code == 200:
            return web.json_response(response.json(),status=200)
        else:
            return web.json_response({"message":"Something Went Wrong"})
    except:
        return web.json_response({"message":"Something Went Wrong"})
async def handle_get(request):
	global round_rob,num_sys,request_url_base
	params = None
	params = request.rel_url.query
	try:
		if None != params:
			params = dict(params)
#		print(f"{request_url_base}{processes[round_rob]}")
		response = requests.get(f"{request_url_base}{processes[round_rob]}",params=params)
		round_rob = (round_rob+1)%num_sys
		if response.status_code == 200:
			return web.json_response(response.json(),status=200)
		else:
			return web.json_response(response.json())
	except Exception as e:
		return web.json_response({"message":f" {str(e)} 1 Something Went Wrong"})

async def handle_post(request):
    global round_rob,num_sys,request_url_base
    try:
        data = await request.json()
        response = requests.get(f"{request_url_base}{processes[round_rob]}",json=data)
        round_rob = (round_rob+1)%num_sys
        if response.status_code == 200:
            return web.json_response(response.json(),status=200)
        else:
            return web.json_response({"message":"Something Went Wrong"},status=504)
    except Exception as e:
        return web.json_response(
            {"error": "Invalid JSON payload", "details": str(e)},
            status=400
        )

app = web.Application()

app.router.add_get("/", handle_get)
app.router.add_get("/exit",handle_exit)
app.router.add_post("/", handle_post)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        config_file = open(sys.argv[1]).readlines()
        config_file = [ i.replace('\n','') for i in config_file]
        hostname = config_file[0]
        request_url_base += hostname + ":"
        processes = []
        num_sys = int(config_file[1])
        for i in range(0,num_sys):
                os.system(f"qemu-system-x86_64 -m 1024 -drive if=virtio,file=slave_{config_file[i+3]},format=qcow2 -netdev user,id=mynet0,hostfwd=tcp:0.0.0.0:{int(config_file[i+2])+20}-:22,hostfwd=tcp:0.0.0.0:{config_file[i+3]}-:80 -device virtio-net,netdev=mynet0 -display none -daemonize")
                processes.append(int(config_file[i+3]))
        web.run_app(app, host=hostname, port=int(config_file[2]))
    else:
        print("Provide the configuration file")
