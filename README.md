# NourrIR Flask Project
  
**Note**: You are on the REVAMP branch. For the UI/UX revamp plan and detailed roadmap, see `REVAMP_ROADMAP.md`. Implementation tasks are tracked in the following files:
- `TODO_nav.md` (Navigation)
- `TODO_theme.md` (Dark/Light Mode Toggle)
- `TODO_i18n.md` (Internationalization)
- `TODO_layout.md` (Structured Layout & Responsive Design)
- `TODO_tooltips.md` (Tippy.js Tooltips)

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
  - Performance Policy (`/performance`)
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
- `PORT`: Port for the Flask server. Default: `8080`.

Example:

```bash
export OLLAMA_CHAT_URL=https://ollama.artemis-ai.ca/v1/chat/completions
export OLLAMA_MODELS_URL=https://ollama.artemis-ai.ca/v1/models
export OLLAMA_MODEL=mistral:latest
export PORT=8080
```

## Running the App

### Locally with Flask

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
export OLLAMA_CHAT_URL=https://ollama.artemis-ai.ca/v1/chat/completions
export OLLAMA_MODELS_URL=https://ollama.artemis-ai.ca/v1/models
export OLLAMA_MODEL=mistral:latest
export PORT=8080
flask run --host=0.0.0.0 --port=$PORT
```

Open your browser at [http://localhost:8080](http://localhost:8080).

### With Docker

docker build -t nourrir-flask .
docker run -d -p 8282:8080 \
  -e OLLAMA_CHAT_URL=https://ollama.artemis-ai.ca/v1/chat/completions \
  -e OLLAMA_MODELS_URL=https://ollama.artemis-ai.ca/v1/models \
  -e OLLAMA_MODEL=mistral:latest \
  -e PORT=8080 \
  --name nourrir-flask nourrir-flask
```

Browse to [http://localhost:8282](http://localhost:8282).

### With docker-compose

```bash
docker-compose up --build
```

By default, the web service is exposed on port `8282`.

## Usage

- Navigate to the static pages via the top navigation bar, including the new **Performance Policy** section.
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
## Running Tests

Run the test suite with:

```bash
pytest
```

### Local static build

Render the site to static HTML and serve it locally:

```bash
pip install -r requirements.txt
python freeze.py
npx serve build
```


## Deployment on Netlify

1. Install the Netlify CLI and log in with `netlify login`.
2. Run `netlify deploy --prod` to build and deploy.
3. The build step installs requirements and runs `python freeze.py`.
4. Netlify automatically uploads the rendered `build/` directory.

## Troubleshooting

- **Cannot connect to Ollama**: Verify `OLLAMA_CHAT_URL` (or legacy `OLLAMA_URL`) and that the Ollama server is reachable from your network.
- **Port conflicts**: Ensure ports `8080` (Flask) or `8282` (Docker) are available. Set `PORT` to change the Flask port.
- **Asset loading issues**: Check the `/assets/<filename>` route and that files exist under `static/assets/`.

## License

This project is provided for educational and demonstration purposes.
Released under the MIT License.
