# Argus

**Argus** is a lightweight system monitoring API built with Python and FastAPI.

The project provides HTTP endpoints for retrieving real-time information about the host system, with the long-term goal of evolving into a complete remote monitoring solution.

---

## Overview

Argus exposes system metrics through a REST API, allowing compatible clients to retrieve information about the machine where the service is running.

Current monitoring capabilities include:

* CPU utilization
* CPU core count
* Memory information
* Disk usage

The API is designed to be accessed locally or from other devices on the same network.

```text
┌──────────────────────┐
│   Client / Browser   │
│  Mobile / Dashboard  │
└──────────┬───────────┘
           │ HTTP
           ▼
┌──────────────────────┐
│        Argus         │
│      FastAPI API     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│      Host System     │
│ CPU · RAM · Storage  │
└──────────────────────┘
```

---

## Features

### System Monitoring

| Resource    | Endpoint           | Status    |
| ----------- | ------------------ | --------- |
| CPU         | `GET /system/cpu`  | Available |
| Memory      | `GET /system/ram`  | Available |
| Disk        | `GET /system/disk` | Available |
| Swap        | —                  | Planned   |
| Processes   | —                  | Planned   |
| Network     | —                  | Planned   |
| GPU         | —                  | Planned   |
| Temperature | —                  | Planned   |

---

## API

### CPU

```http
GET /system/cpu
```

Returns information about the current CPU utilization and available CPU cores.

Example:

```json
{
  "cpu_percent": 16.0,
  "cpu_cores": 8
}
```

### Memory

```http
GET /system/ram
```

Returns information about system memory.

### Disk

```http
GET /system/disk
```

Returns information about disk usage.

---

## API Documentation

Argus uses FastAPI's automatic interactive documentation.

When the server is running, the documentation is available at:

```text
http://127.0.0.1:8000/docs
```

The OpenAPI schema is available at:

```text
http://127.0.0.1:8000/openapi.json
```

---

## Network Access

Argus can be accessed from other devices on the same local network when the server is configured to listen on the network interface.

For example:

```text
http://192.168.18.19:8000/system/cpu
```

The IP address shown above is only an example and depends on the host's current network configuration.

Remote access through a private network such as Tailscale is planned for a future stage.

---

## Requirements

* Python 3
* FastAPI
* Uvicorn
* psutil
* uv

---

## Installation

Clone the repository and enter the project directory:

```bash
git clone <repository-url>
cd Argus
```

Create and activate a virtual environment according to your Python environment.

Install the project dependencies with `uv`.

---

## Running

Start the development server with:

```bash
uv run fastapi dev
```

Once running, the API will be available locally at:

```text
http://127.0.0.1:8000
```

For development, FastAPI's interactive documentation can be accessed through:

```text
http://127.0.0.1:8000/docs
```

---

## Project Structure

```text
Argus/
├── app/
│   ├── __init__.py
│   └── main.py
├── tests/
│   └── __init__.py
├── .gitignore
├── README.txt
├── pyproject.toml
├── requirements.txt
└── uv.lock
```

---

## Roadmap

### Monitoring

* [x] CPU metrics
* [x] Memory metrics
* [x] Disk metrics
* [ ] Swap metrics
* [ ] Process monitoring
* [ ] Network statistics
* [ ] GPU monitoring
* [ ] Temperature monitoring

### API

* [x] FastAPI foundation
* [x] System endpoints
* [ ] Response models
* [ ] Input validation
* [ ] Error handling
* [ ] Authentication
* [ ] Authorization

### Data

* [ ] SQLite integration
* [ ] Metric history
* [ ] Historical queries
* [ ] Data retention

### Remote Access

* [x] Localhost access
* [x] Local network access
* [ ] Private remote access
* [ ] Tailscale integration

### Interface

* [ ] Web dashboard
* [ ] Real-time metrics
* [ ] Historical charts
* [ ] Mobile-friendly interface

---

## Architecture Goals

As the project evolves, Argus aims to separate its responsibilities into distinct layers:

```text
Client
  │
  ▼
API
  │
  ▼
Monitoring Services
  │
  ├── CPU
  ├── Memory
  ├── Disk
  ├── Network
  └── Processes
  │
  ▼
Persistence
  │
  └── SQLite
```

This structure is intended to make the project easier to maintain, test, and extend.

---

## Development

Argus is developed incrementally, with an emphasis on understanding the underlying concepts rather than relying on abstractions without understanding their purpose.

The project serves as a practical environment for exploring:

* Python
* REST APIs
* FastAPI
* HTTP
* JSON
* Linux system information
* Networking
* Database design
* Authentication
* Testing
* Git
* Remote infrastructure

---

## Project Status

**Early Development**

The API is functional and capable of exposing basic system metrics. Architecture, endpoints, data models, persistence, authentication, and remote access are expected to evolve as development continues.

---

## License

License information will be added as the project matures.

---

**Argus**
*System monitoring, exposed through an API.*
