# main.py
import uvicorn
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import logging
import os
from dotenv import load_dotenv
import tempfile
import shutil

from sonal_aura.analysis import create_audio_report

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
    2. Call the analysis layer to process it.
    3. (TODO) Send the report to the LLM for feedback generation.
    4. Return the feedback.
    """
    if not file.content_type.startswith("audio/"):
        logger.warning(f"Failed upload attempt with invalid file type: {file.content_type}")
        return JSONResponse(
            status_code=400,
            content={"error": f"Invalid file type. Please upload an audio file. Got {file.content_type}."}
        )
    
    temp_dir = tempfile.mkdtemp()
    temp_file_path = os.path.join(temp_dir, file.filename)

    try:
        # Saving the file temmporarily
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"Received file: {file.filename}, saved temporarily to: {temp_file_path}")

        # Running the DSP analysis
        report = create_audio_report(temp_file_path)

        # Sending to the LLM for feedback generation (TODO)
        # For now, we just return the raw report
        logger.info(f"Analysis complete for file: {file.filename}. Returning report.")

        return {
            "filename": file.filename,
            "status": "Analysis complete",
            "report": report
        }
    
    except Exception as e:
        logger.error(f"Error processing file {file.filename}: {e}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"error": f"An error occurred during analysis: {str(e)}"}
        )
    
    finally:
        # Cleaning up temporary files
        await file.close()
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            logger.info(f"Cleaned up temporary directory: {temp_dir}")
    
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)