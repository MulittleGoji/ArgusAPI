from fastapi import FastAPI
import psutil
import os
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import pwd
import subprocess

app = FastAPI()

def ping():
    os.system('clear')
    ip = "192.168.18.0".split('.')
    ip_list = []
    future_to_ip = {}
    with ThreadPoolExecutor(max_workers=128) as executor:
        for i in range(0, 255):
            ip [3] = str(i)
            ip_formatado = '.'.join(ip)
            func = os.system
            future = executor.submit(func, 'ping -c 1 {}'.format(ip_formatado))
            future_to_ip[future] = ip_formatado
        for future in concurrent.futures.as_completed(future_to_ip):
            rs = future.result()
            if rs == 0:
                ip_list.append(future_to_ip[future])
    return ip_list

def shutdown():
    os.system('clear')
    os.system('systemctl poweroff')

@app.get("/")
def read_root():
    return{"Hello": "World"}

@app.get('/network')
def network():
    return{'network': psutil.net_if_addrs()}

@app.get("/system/cpu")
def read_cpu():
    return{"cpu_percent": psutil.cpu_percent(interval=0.0), "cpu_cores": psutil.cpu_count(True)}

@app.get("/system/ram")
def read_ram():
    return{"virtual memory": psutil.virtual_memory()}

@app.get("/system/disk")
def read_disk():
    return{"disk": psutil.disk_usage('/')}

@app.get("/system/users")
def read_users():
    cmd = ['uptime', '-p']
    uptime = subprocess.check_output(cmd).decode("utf-8").strip("\n")
    return{"users": pwd.getpwuid(1000).pw_name, "uid": pwd.getpwuid(1000).pw_uid, "uptime":uptime}

@app.get("/system/network/devices")
def read_network():
    return{"dispositivos": ping()}

@app.get('/system/shutdown')
def shutdown_system():
    shutdown()
    return 'PC desligado'

@app.get('/system/processes')
def get_processes():
    processes = []
    for proc in psutil.process_iter(['pid\n','name\n','username\n']):
        processes.append(proc.info)

    return {'processes': processes}