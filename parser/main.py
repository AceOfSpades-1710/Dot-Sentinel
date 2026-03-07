from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import aiofiles
from contextlib import asynccontextmanager

from parser.pipeline import Pipeline

# Global pipeline instance
pipeline_instance = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global pipeline_instance
    print("[*] Starting up parser service...")
    try:
        pipeline_instance = Pipeline()
    except Exception as e:
        print(f"[!] Failed to initialize pipeline: {e}")
        # We might want to exit or just log, but let's log for now so app starts
    yield
    print("[*] Shutting down parser service...")

app = FastAPI(lifespan=lifespan)

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TEMP_DIR = "temp_uploads"
os.makedirs(TEMP_DIR, exist_ok=True)

@app.post("/analyze")
async def analyze_pcap(file: UploadFile = File(...)):
    if not file.filename.endswith(".pcap") and not file.filename.endswith(".pcapng"):
        raise HTTPException(status_code=400, detail="Only .pcap and .pcapng files are supported")

    file_path = os.path.join(TEMP_DIR, file.filename)
    
    try:
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
            
        print(f"[*] Received file: {file.filename}")
        
        if pipeline_instance is None:
            raise HTTPException(status_code=500, detail="Pipeline not initialized")
            
        # Run pipeline
        result = pipeline_instance.process_pcap(file_path)
        
        return result
        
    except Exception as e:
        print(f"[!] Error processing file: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup
        if os.path.exists(file_path):
            os.remove(file_path)

@app.get("/health")
def health_check():
    return {"status": "ok", "model_loaded": pipeline_instance is not None}
