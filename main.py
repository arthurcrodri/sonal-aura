# main.py
import uvicorn
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import logging
import os
from dotenv import load_dotenv

# Loading environment variables from .env file
load_dotenv()
# Reading the key from the environment
MY_API_KEY = os.getenv("GOOGLE_API_KEY")

# Checking if the key was loaded correctly
if not MY_API_KEY:
    raise EnvironmentError("FATAL ERROR: GOOGLE_API_KEY not found in environment variables.")

# Setting up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Creating FastAPI app instance
app = FastAPI(
    title="Sonal Aura API",
    description="Analyzes audio tracks to provide mixing and mastering feedback.",
    version="0.1.0",
)

@app.get("/")
async def read_root():
    """
    Root endpoint providing a welcome message. Checks if the API is running.
    """
    return {"message": "Welcome to the Sonal Aura API! Send a POST request to /analyze to get started."}

@app.post("/analyze")
async def analyze_audio(file: UploadFile = File(...)):
    """
    Main endpoint. It will:
    1. Receive an audio file.
    2. (TODO) Save it temporarily.
    3. (TODO) Run the DSP analysis (liprosa, etc.).
    4. (TODO) Build the JSON report.
    5. (TODO) Send the report to the LLM for feedback generation.
    6. Return the feedback.
    """
    if not file.content_type.startswith("audio/"):
        logger.warning(f"Failed upload attempt with invalid file type: {file.content_type}")
        return JSONResponse(
            status_code=400,
            content={"error": f"Invalid file type. Please upload an audio file. Got {file.content_type}."}
        )
    
    logger.info(f"Received file: {file.filename} of type {file.content_type}")
    
    # LOGIC PLACEHOLDER: For now, we just acknowledge receipt of the file.
    # Future implementation will include saving the file, analyzing it, and generating feedback.
    return {"filename": file.filename, "status": "File received. Analysis pending."}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)