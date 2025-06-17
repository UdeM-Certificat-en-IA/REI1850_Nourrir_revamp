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

Configure the Ollama API endpoints via environment variables:

- `OLLAMA_CHAT_URL`: URL for the chat completion endpoint. For OpenAI-compatible API, this is typically:
  ```
  https://ollama.artemis-ai.ca/v1/chat/completions
  ```
  Fallback default (legacy Ollama API):
  ```
  http://192.168.2.10:11434/api/chat
  ```
- `OLLAMA_MODELS_URL`: URL for the models listing endpoint. For OpenAI-compatible API:
  ```
  https://ollama.artemis-ai.ca/v1/models
  ```
  Fallback default (legacy):
  ```
  http://192.168.2.10:11434/api/models
  ```
- `OLLAMA_MODEL`: The primary model identifier to use (e.g. `mistral:latest`). Default: `mistral:latest`.

Example:

```bash
export OLLAMA_CHAT_URL=https://ollama.artemis-ai.ca/v1/chat/completions
export OLLAMA_MODELS_URL=https://ollama.artemis-ai.ca/v1/models
export OLLAMA_MODEL=mistral:latest
```

## Running the App

### Locally with Flask

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
export OLLAMA_CHAT_URL=https://ollama.artemis-ai.ca/v1/chat/completions
export OLLAMA_MODELS_URL=https://ollama.artemis-ai.ca/v1/models
export OLLAMA_MODEL=mistral:latest
flask run --host=0.0.0.0 --port=8080
```

Open your browser at [http://localhost:8080](http://localhost:8080).

### With Docker

docker build -t nourrir-flask .
docker run -d -p 8282:8080 \
docker build -t nourrir-flask .
docker run -d -p 8282:8080 \
  -e OLLAMA_CHAT_URL=https://ollama.artemis-ai.ca/v1/chat/completions \
  -e OLLAMA_MODELS_URL=https://ollama.artemis-ai.ca/v1/models \
  -e OLLAMA_MODEL=mistral:latest \
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

- **Cannot connect to Ollama**: Verify `OLLAMA_CHAT_URL` (or legacy `OLLAMA_URL`) and that the Ollama server is reachable from your network.
- **Port conflicts**: Ensure ports `8080` (Flask) or `8282` (Docker) are available.
- **Asset loading issues**: Check the `/assets/<filename>` route and that files exist under `static/assets/`.

## License

This project is provided for educational and demonstration purposes.
Released under the MIT License.
