from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from core.orchestrator import Orchestrator
import uvicorn
import asyncio

app = FastAPI(title="JUNE API", description="Personal AI Agent API")

orchestrator = Orchestrator()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.get("/")
def read_root():
    return {"status": "online", "agent": "JUNE"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    response = await orchestrator.process(request.message)
    return ChatResponse(response=response)

def start_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    start_server()
