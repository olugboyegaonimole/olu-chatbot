from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import uvicorn

# Load the model and tokenizer
MODEL_NAME = "facebook/blenderbot-400M-distill"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

# Initialize FastAPI
app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request structure
class ChatRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return {"message": "Welcome to the Chatbot API!"}

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        inputs = tokenizer(request.message, return_tensors="pt")
        output_ids = model.generate(**inputs)
        response = tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Start app if running locally
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
