# NourrIR Flask Project

NourrIR is a minimal Flask-based web application showcasing static pages and an AI-powered chat assistant ("NuRiH Ami") that proxies messages to an Ollama LLM server.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the App](#running-the-app)
  - [Locally with Flask](#locally-with-flask)
  - [With Docker](#with-docker)
  - [With docker-compose](#with-docker-compose)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Features

- Static pages:
  - Home (`/`)
  - Integration Policy (`/politique`)
  - HR Contact (`/contact`)
- Floating AI chat widget ("NuRiH Ami") available on all pages
- Proxy endpoint (`/nurih-ami`) to forward user messages to an Ollama LLM server
- Dockerized application with Dockerfile and docker-compose support

## Prerequisites

- Python 3.11 or higher
- pip
- (Optional) Docker & docker-compose
- Access to an Ollama server for the chat backend

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd nourrir_flask
   ```

2. (Optional) Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install Python dependencies:

   ```bash
   pip install --no-cache-dir -r requirements.txt
   ```

## Configuration

Set the `OLLAMA_URL` environment variable to point to your Ollama chat API endpoint. If not set, it defaults to:

```
http://192.168.2.10:11434/api/chat
```

Example:

```bash
export OLLAMA_URL=http://<ollama-host>:11434/api/chat
```

## Running the App

### Locally with Flask

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
export OLLAMA_URL=http://<ollama-host>:11434/api/chat
flask run --host=0.0.0.0 --port=8080
```

Open your browser at [http://localhost:8080](http://localhost:8080).

### With Docker

```bash
docker build -t nourrir-flask .
docker run -d -p 8282:8080 \
  -e OLLAMA_URL=http://<ollama-host>:11434/api/chat \
  --name nourrir-flask nourrir-flask
```

Browse to [http://localhost:8282](http://localhost:8282).

### With docker-compose

```bash
docker-compose up --build
```

By default, the web service is exposed on port `8282`.

## Usage

- Navigate to the static pages via the top navigation bar.
- Click the chat icon (💬) in the bottom right to open the NuRiH Ami assistant.
- Type your questions or prompts; the message will be forwarded to the Ollama model and the response displayed in the chat widget.

## Project Structure

```
.
├── app.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── static/
│   └── assets/...
└── templates/
    ├── base.html
    ├── index.html
    ├── politique.html
    └── contact.html
```

## Troubleshooting

- **Cannot connect to Ollama**: Verify `OLLAMA_URL` and that the Ollama server is reachable from your network.
- **Port conflicts**: Ensure ports `8080` (Flask) or `8282` (Docker) are available.
- **Asset loading issues**: Check the `/assets/<filename>` route and that files exist under `static/assets/`.

## License

This project is provided for educational and demonstration purposes.