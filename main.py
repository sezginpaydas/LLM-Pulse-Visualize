
from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
import uvicorn
import asyncio
import json
import httpx

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "qwen3:0.6b"

app = FastAPI()

clients = set()

@app.get("/")
async def index():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(html_content)

@app.websocket("/ws")
async def ws_dashboard(ws: WebSocket):
    await ws.accept()
    clients.add(ws)
    try:
        while True:
            await asyncio.sleep(10)
    finally:
        clients.remove(ws)

async def broadcast(payload):
    dead = []
    for ws in clients:
        try:
            await ws.send_text(json.dumps(payload))
        except:
            dead.append(ws)
    for d in dead:
        clients.remove(d)

@app.post("/prompt")
async def prompt(req: Request):
    data = await req.json()
    prompt_text = data.get("prompt", "")
    print(f"DEBUG: Received prompt: {prompt_text}")

    await broadcast({"event": "request"})

    prompt_tokens = len(prompt_text.split())
    gen_tokens = 0

    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream(
            "POST",
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt_text,
                "stream": True
            }
        ) as r:

            await broadcast({
                "event": "thinking",
                "req_tokens": prompt_tokens
            })

            final_stats = None

            async for line in r.aiter_lines():
                if not line:
                    continue

                chunk = json.loads(line)

                if "response" in chunk:
                    gen_tokens += 1
                    if gen_tokens % 5 == 0:
                        await broadcast({"event": "thinking_tick", "tokens": gen_tokens})

                if chunk.get("done") is True:
                    final_stats = {
                        "prompt_tokens": chunk.get("prompt_eval_count"),
                        "generated_tokens": chunk.get("eval_count"),
                        "prompt_time_ms": round(chunk.get("prompt_eval_duration", 0) / 1e6),
                        "generation_time_ms": round(chunk.get("eval_duration", 0) / 1e6),
                        "total_time_ms": round(chunk.get("total_duration", 0) / 1e6),
                    }
                    break

            await broadcast({
                "event": "output",
                "final_stats": final_stats
            })

    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

