# Argus

> PC monitoring API: check your computer's resources and local network from anywhere through HTTP.

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![Status](https://img.shields.io/badge/status-in%20development-orange)

Argus is a REST API written in Python that collects and exposes information about the machine it runs on: CPU, memory, disk, processes, network interfaces and the devices connected to the local network.

The goal is to grow it step by step into a complete monitoring system, with historical data, remote access and its own dashboard.

---

## Features

- **System metrics**: CPU, RAM, disk, uptime, current user and running processes.
- **Network interfaces**: addresses and netmasks of every interface on the host.
- **Automatic network discovery**: the API detects the host's own network (IP and netmask), so it works on any machine or network without configuration. Loopback and `/32` interfaces (such as VPN tunnels) are ignored.
- **Concurrent device scan**: hosts are probed in parallel with `ThreadPoolExecutor`, with a 1-second timeout per host.
- **API key authentication**: every route is protected by a global dependency.
- **Remote power control**: shutdown endpoint (see the security notes below).

---

## How the network scan works

```text
psutil.net_if_addrs()
        ↓
Filter IPv4 interfaces (skip loopback and /32)
        ↓
ipaddress.IPv4Interface(ip/netmask) → network → hosts
        ↓
ThreadPoolExecutor (128 workers) → ping -c 1 -W 1 <host>
        ↓
Hosts that answered (return code 0)
```

Because the network is derived from the host's own configuration, the same code works on a `192.168.x.x`, `10.x.x.x` or `172.16.x.x` network, whatever the prefix length.

---

## Tech stack

| Area | Tools |
|---|---|
| Language | Python |
| Web framework | FastAPI, Uvicorn |
| Configuration | pydantic-settings (`.env`) |
| System information | psutil |
| Networking | `ipaddress`, `socket`, `subprocess` |
| Concurrency | `concurrent.futures.ThreadPoolExecutor` |
| Packaging | uv |
| Planned | SQLite, Tailscale |

---

## Project structure

```text
Argus/
├── app/
│   ├── __init__.py
│   ├── auth.py        # API key verification
│   ├── config.py      # settings loaded from environment / .env
│   └── main.py        # routes and network scan logic
├── tests/
│   └── __init__.py
├── .env.example       # template for the required environment variables
├── pyproject.toml
├── uv.lock
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Requirements

- Linux (the project uses `systemctl`, `uptime -p`, `pwd` and the Linux `ping` flags)
- Python 3.x
- [uv](https://docs.astral.sh/uv/)

---

## Getting started

```bash
# install dependencies
uv sync

# create your .env with ARGUS_API_KEY (see "Authentication" below)
cp .env.example .env

# run in development mode
uv run fastapi dev
```

The API is available at `http://127.0.0.1:8000` and the interactive documentation at `http://127.0.0.1:8000/docs`.

To reach it from another device on the same network, use the host's IP address:

```text
http://<COMPUTER_IP>:8000
```

### Authentication

All endpoints require an API key, checked by a global FastAPI dependency (`app/auth.py`). The key is read from the `ARGUS_API_KEY` environment variable (`app/config.py`, using `pydantic-settings`), which can be defined in a `.env` file at the project root.

1. Generate a key:

   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

2. Create a `.env` file (it is ignored by Git) based on `.env.example`:

   ```text
   ARGUS_API_KEY=<your-generated-key>
   ```

3. Send the key in the `api_key` header with every request:

   ```bash
   curl -H "api_key: <your-generated-key>" http://127.0.0.1:8000/system/cpu
   ```

Requests with a missing or wrong key are rejected (`401 Unauthorized` for a wrong key; FastAPI also rejects requests with no header).

---

## Endpoints

| Method | Route | Description |
|---|---|---|
| GET | `/` | Health check |
| GET | `/network` | Addresses of all network interfaces |
| GET | `/system/cpu` | CPU usage and core count |
| GET | `/system/ram` | Virtual memory information |
| GET | `/system/disk` | Disk usage of `/` |
| GET | `/system/users` | Current user, UID and uptime |
| GET | `/system/processes` | Running processes (PID, name, user) |
| GET | `/system/network/devices` | Devices on the local network that answered a ping |
| POST | `/system/shutdown` | Shuts the computer down |

### Examples

**`GET /system/cpu`**

```json
{
    "cpu_percent": 4.2,
    "cpu_cores": 8
}
```

**`GET /system/users`**

```json
{
    "users": "murilo",
    "uid": 1000,
    "uptime": "up 8 hours, 59 minutes"
}
```

**`GET /system/network/devices`**

```json
{
    "dispositivos": [
        "192.168.18.1",
        "192.168.18.5",
        "192.168.18.19"
    ]
}
```

---

## Security notes

- `POST /system/shutdown` powers off the machine. Keep it behind authentication and do not expose the API to the internet without additional protection.
- Remote access is currently limited to the local network. Access from outside is planned through Tailscale.

---

## Known limitations

- **Devices that block ICMP do not appear in the scan.** The scan relies on ping, so hosts with a firewall that drops echo requests are reported as offline. Reading the ARP table is planned to fix this on local networks.
- **No size limit for large networks.** On a `/16` network the scan would probe about 65,000 hosts. A cap on the number of hosts is planned.
- **Linux only.**

---

## Roadmap

### Monitoring
- [x] CPU
- [x] RAM
- [x] Disk
- [x] User, UID and uptime
- [x] Processes
- [x] Network interfaces
- [x] Network devices with automatic network discovery
- [ ] Device discovery through the ARP table (devices that block ping)
- [ ] Host limit for large networks
- [ ] Swap
- [ ] Temperature
- [ ] GPU

### API
- [x] Basic API
- [x] System endpoints
- [x] API key authentication
- [ ] Easier API key generation and management
- [ ] Validation and response models
- [ ] Error handling
- [ ] Permissions per endpoint
- [ ] Automated tests

### Persistence
- [ ] SQLite
- [ ] Metrics history
- [ ] Historical queries
- [ ] Automatic cleanup of old data

### Remote access
- [x] Local network access
- [ ] Tailscale
- [ ] Monitoring outside the local network

### Interface
- [ ] Dashboard
- [ ] Charts
- [ ] Usage history

---

## What I'm learning

Argus is a learning project. It is helping me practice API design with FastAPI, networking fundamentals (IP, subnets, ICMP, ARP), concurrency, Linux system internals, authentication, Git and, soon, databases and infrastructure.

The project is built incrementally: understand each part before adding the next layer.

> **Observe. Understand. Build. Monitor.**

---

## Author

**Murilo**: personal project for learning and experimentation.