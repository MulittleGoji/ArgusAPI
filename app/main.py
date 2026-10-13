from fastapi import Depends, FastAPI
import psutil
import os
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import pwd
import subprocess
import app.auth as auth
import socket
import ipaddress

app = FastAPI(dependencies=[Depends(auth.verify_api_key)])

def find_hosts():
    cmd = psutil.net_if_addrs()
    ip_list = []
    for interface in cmd:
        for address in cmd[interface]:
            if address.family == socket.AF_INET:
                if address.netmask == '255.255.255.255':
                    continue
                if address.address.startswith('127.'):
                    continue
                ipmask = (address.address) + ('/') + (address.netmask)
                ips = ipaddress.IPv4Interface(ipmask)
                for ip in ips.network.hosts():
                    ip_list.append(ip)
    return ip_list    

def ping():
    hosts = find_hosts()
    ip_list = []
    future_to_ip = {}
    with ThreadPoolExecutor(max_workers=128) as executor:
        for host in hosts:    
            func = subprocess.run
            cmd = ['ping', '-c', '1','-W', '1', str(host)]
            future = executor.submit(func, cmd, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
            future_to_ip[future] = str(host)
        for future in concurrent.futures.as_completed(future_to_ip):
            rs = future.result()
            if rs.returncode == 0:
                ip_list.append(future_to_ip[future])
    return(ip_list)

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

@app.post('/system/shutdown')
def shutdown_system():
    shutdown()
    return 'PC desligado'

@app.get('/system/processes')
def get_processes():
    processes = []
    for proc in psutil.process_iter(['pid','name','username']):
        processes.append(proc.info)

    return {'processes': processes}
