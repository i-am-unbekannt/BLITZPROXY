# ⚡ BlitzProxy

> **BlitzProxy provides regularly updated free proxy lists** – automatically refreshed every 2 days – including HTTP/S, SOCKS4, and SOCKS5 proxies.  
> It features a real-time web-based GUI, built-in proxy testing, and is designed for easy deployment via Docker.

---

## 🚀 Features

- Scrapes free proxies (HTTP/S, SOCKS4, SOCKS5)
- Verifies and checks availability and response time
- Outputs clean proxy lists in `.txt` format
- Interactive web GUI with terminal and file browser
- Easy Docker-based setup

---

## 🖥️ Web Interface

Accessible via browser on port `3000`:

- Start/Stop the checking script
- View live output in a terminal
- View contents of output `.txt` files
- Download proxy lists directly

Basic HTTP Auth is included (`admin:blitzproxy` by default – override in `server.js`, line 14).

---

## 🐳 Docker Setup

### Build and run:

```bash
git clone https://github.com/i-am-unbekannt/BLITZPROXY
cd BLITZPROXY
docker-compose build
docker-compose up -d
```
