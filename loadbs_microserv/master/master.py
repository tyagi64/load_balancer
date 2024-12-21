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
    global processes
    print(processes)
    for i in processes:
        try:
            os.kill(i,signal.SIGTERM)
            print(f"Sent SIGTERM to process with PID: {i}.")
        except ProcessLookupError:
            print(f"No process with PID: {i} found.")
        except Exception as e:
            print(f"Error killing process {i}: {e}")
    return web.json_response({"status":"done"})

async def handle_get(request):
    global round_rob,num_sys,request_url_base
    params = None
    params = request.rel_url.query
    try:
        if None != params:
                params = dict(params)
        response = requests.get(request_url_base+config_file[3+round_rob],params=params)
        round_rob = (round_rob+1)%num_sys
        if response.status_code == 200:
            return web.json_response(response.json(),status=200)
        else:
            return web.json_response({"message":"Something Went Wrong"})
    except:
        return web.json_response({"message":"Something Went Wrong"})

async def handle_post(request):
    global round_rob,num_sys,request_url_base
    try:
        data = await request.json()
        response = requests.get(request_url_base+config_file[3+round_rob],json=data)
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
        print(hostname)
        for i in range(0,num_sys):
            pid = os.fork()          
            if pid == 0:
                    os.execvp("python3", ["python3", "slave.py",hostname,config_file[2],config_file[i+3]])
            else:
                processes.append(pid)
        web.run_app(app, host=hostname, port=int(config_file[2]))
    else:
        print("Provide the configuration file")
