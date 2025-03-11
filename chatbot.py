from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import uvicorn

# Load the model and tokenizer
MODEL_NAME = "facebook/blenderbot-400M-distill"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

# Initialize FastAPI
app = FastAPI()

# Request model
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Tokenize input message
        inputs = tokenizer(request.message, return_tensors="pt")
        # Generate response
        output_ids = model.generate(**inputs)
        # Decode response
        response = tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the app using: uvicorn script_name:app --reload
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
