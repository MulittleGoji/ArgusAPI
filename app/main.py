from fastapi import FastAPI
import psutil
import os
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

app = FastAPI()

def ping():
    os.system('clear')
    ip = "192.168.18.0".split('.')
    ip_list = []
    future_to_ip = {}
    with ThreadPoolExecutor (max_workers=24) as executor:
        for i in range (0, 23):
            ip [3] = str(i)
            ip_formatado = '.'.join(ip)
            func = os.system
            future = executor.submit(func, 'ping -c 1 {}'.format(ip_formatado))
            future_to_ip[future] = ip_formatado
        for future in concurrent.futures.as_completed(future_to_ip):
            rs = future.result()
            if rs == 0:
                ip_list.append(future_to_ip[future])
    return(ip_list)

def shutdown():
    os.system('clear')
    os.system('systemctl poweroff')

@app.get("/")
def read_root():
    return{"Hello": "World"}

@app.get("/system/cpu")
def read_cpu():
    return{"cpu_percent": psutil.cpu_percent(interval= 0.0), "cpu_cores": psutil.cpu_count(True)}

@app.get("/system/ram")
def read_ram():
    return{"virtual memory": psutil.virtual_memory()}

@app.get("/system/disk")
def read_disk():
    return{"disk": psutil.disk_usage('/')}

@app.get("/system/users")
def read_users():
    return{"users": psutil.users()}

@app.get("/system/network/devices")
def read_network():
    return{"dispositivos": ping()}

@app.get('/system/shutdown')
def shutdown_system():
    shutdown()
    return('PC desligado')