# ARGUS

> PC Monitoring API — monitor your computer through an API.

**Argus** is an API developed in Python for monitoring computer resources.

The idea behind the project is to gradually turn Argus into a system capable of collecting, organizing, and providing information about a computer through an API accessible locally or over a network.

---

## 🚧 Status

**In development**

The project is still in its early stages and is being developed as a learning project, focusing on Python, APIs, networking, data persistence, and infrastructure.

---

## 🎯 Objective

The goal of Argus is to allow computer information to be accessed remotely through an API.

Example:

```text
Phone / another computer
          ↓
       HTTP Request
          ↓
        Argus
          ↓
       FastAPI
          ↓
       System
```

In the long term, the project may evolve into a complete monitoring system, including historical data, authentication, and its own interface.

---

## 🛠️ Technologies

* Python
* FastAPI
* Uvicorn
* psutil
* subprocess
* ThreadPoolExecutor
* uv
* SQLite (planned)
* Tailscale (planned)

---

## 📁 Structure

```text
Argus/
├── app/
│   ├── __init__.py
│   └── main.py
├── tests/
│   └── __init__.py
├── pyproject.toml
├── uv.lock
├── requirements.txt
├── README.txt
└── .gitignore
```

---

## 📡 Current Endpoints

### Root

```http
GET /
```

Returns a basic response to verify that the API is running.

### CPU

```http
GET /system/cpu
```

Returns information about the processor, such as:

* CPU usage
* number of CPU cores

### RAM

```http
GET /system/ram
```

Returns information about the system's RAM.

### Disk

```http
GET /system/disk
```

Returns information about the system's storage.

### User and System

```http
GET /system/users
```

Returns information about the currently logged-in user and the computer's uptime.

Example:

```json
{
    "users": "murilo",
    "uid": 1000,
    "uptime": "up 8 hours, 59 minutes"
}
```

The uptime information is obtained directly from the operating system.

### Processes

```http
GET /system/processes
```

Returns information about the processes currently running on the system.

Currently, the following information is collected:

* process ID (PID)
* process name
* process user

Process information is collected using `psutil.process_iter()`.

### Network Devices

```http
GET /system/network/devices
```

Scans the local network and returns the IP addresses that responded to a ping.

Argus uses `ThreadPoolExecutor` to execute network tests concurrently.

Example:

```json
{
    "dispositivos": [
        "192.168.18.1",
        "192.168.18.5",
        "192.168.18.10",
        "192.168.18.19"
    ]
}
```

### Shutdown

```http
GET /system/shutdown
```

Requests the computer to shut down through the operating system.

Currently uses:

```text
systemctl poweroff
```

> This endpoint should be protected with authentication before making the API available outside the local network.

---

## 🌐 Network Access

Argus can be accessed over the local network.

Example:

```text
http://192.168.18.19:8000/system/cpu
```

The IP address depends on the network where the computer is connected.

Currently, remote access is limited to the local network.

Internet access is not part of the current configuration.

---

## ▶️ Running

With the virtual environment configured:

```bash
uv run fastapi dev
```

During development, the API can be accessed at:

```text
http://127.0.0.1:8000
```

The interactive FastAPI documentation is available at:

```text
http://127.0.0.1:8000/docs
```

To access the API from the local network, use the computer's IP address:

```text
http://COMPUTER_IP:8000
```

---

## 🔭 Roadmap

### Monitoring

* [x] CPU
* [x] RAM
* [x] Disk
* [x] User and UID
* [x] Uptime
* [x] Processes
* [x] Network devices
* [ ] Swap
* [ ] Detailed network information
* [ ] Temperature
* [ ] GPU

### API

* [x] Basic API
* [x] System endpoints
* [ ] Validation and models
* [ ] Error handling
* [ ] Authentication
* [ ] Permissions

### Persistence

* [ ] SQLite
* [ ] Metrics history
* [ ] Historical queries
* [ ] Automatic cleanup of old data

### Remote Access

* [x] Local network access
* [ ] Tailscale
* [ ] Monitoring outside the local network

### Interface

* [ ] Dashboard
* [ ] Charts
* [ ] Usage history
* [ ] Custom interface

---

## 📚 What I'm Learning

Argus is also a practical project for learning:

* Python
* API development
* HTTP
* FastAPI
* JSON
* Networking
* Linux
* Databases
* Authentication
* Git and GitHub
* Infrastructure
* System monitoring
* Concurrency
* Operating system processes

---

## 📌 Project Philosophy

Argus is being built incrementally.

The idea is to understand each part of the system before adding new layers of complexity.

> **Observe. Understand. Build. Monitor.**

---

## 👤 Author

**Murilo**

Personal project developed for learning and experimentation.
