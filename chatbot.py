from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline
import uvicorn

app = FastAPI()

# Allow CORS (useful for frontend hosted separately)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change this for security)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load chatbot model
chatbot = pipeline("conversational", model="facebook/blenderbot-400M-distill")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            # Receive message from client
            data = await websocket.receive_text()
            
            # Generate chatbot response
            response = chatbot(data)["generated_text"]
            
            # Send response back to client
            await websocket.send_text(response)
        except Exception:
            await websocket.close()
            break

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
