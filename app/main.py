from fastapi import FastAPI
import psutil
import os

app = FastAPI()

def ping():
    os.system('clear')
    ip = "192.168.18.0".split('.')
    ip_list = []
    for i in range (0, 23):
        ip [3] = str(i)
        ip_formatado = '.'.join(ip)
        rs = os.system('ping -c 1 {}'.format(ip_formatado))
        if rs == 0:
            ip_list.append(ip_formatado)
    return(ip_list)
            

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