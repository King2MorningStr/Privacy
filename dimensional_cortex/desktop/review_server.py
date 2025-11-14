from fastapi import FastAPI, Body
from pydantic import BaseModel
import uvicorn
import time

app = FastAPI()

class PromptRequest(BaseModel):
    text: str
    platform: str = "generic"

@app.post("/process_interaction")
async def mock_interaction(request: PromptRequest):
    """
    A mock endpoint that simulates the real server.
    It receives a request and returns a successful response.
    """
    print(f"\n--- MOCK SERVER ---")
    print(f"✅ Received ping from: {request.platform}")
    print(f"   Payload: '{request.text}'")
    
    # Simulate the V4 response structure
    return {
        "original_prompt": request.text,
        "enriched_prompt": "[MOCK SERVER]: Response successful.",
        "status": "Interaction processed by MOCK TRINITY."
    }

if __name__ == "__main__":
    print("="*40)
    print("  REVIEWER'S MOCK SERVER IS RUNNING")
    print("  Listening on http://127.0.0.1:8000")
    print("  (This is a safe, minimal server for review only)")
    print("="*40)
    uvicorn.run(app, host="127.0.0.1", port=8000)
