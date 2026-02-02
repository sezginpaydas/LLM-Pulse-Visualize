# Visual LLM Dashboard

A real-time, sci-fi themed dashboard to visualize Local LLM (Ollama) inference stages (Request, Thinking, Output) with live statistics.

##  Features
- **Real-time Visualization**: Watch the model process request, think/generate, and output results.
- **WebSocket Integration**: Live status updates without polling.
- **Cyberpunk / Sci-Fi UI**: Beautiful dark interface with neon accents.
- **Ollama Powered**: Works locally with Ollama models (default `qwen3:0.6b`).
- **One-Click Setup**: Automated script for Windows environment setup.

##  Quick Start (Windows)

1.  **Install Ollama**: [Download and install from ollama.com](https://ollama.com).
2.  **Clone/Download this repo**.
3.  **Run `run.bat`**:
    - This script checks for Python and Ollama.
    - Creates a virtual environment (`venv`).
    - Installs dependencies.
    - Pulls the valid model.
    - Starts the server.

##  Manual Installation

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run Ollama**:
    ```bash
    ollama serve
    # Make sure you have the model
    ollama pull qwen3:0.6b
    ```
3.  **Start Application**:
    ```bash
    python main.py
    ```

##  Dashboard

Open your browser to: [http://127.0.0.1:8000](http://127.0.0.1:8000)

##  Project Structure
- `main.py`: FastAPI backend and WebSocket logic.
- `templates/index.html`: Frontend UI.
- `run.bat`: Windows automation script.
- `requirements.txt`: Python package list.

##  License
MIT
