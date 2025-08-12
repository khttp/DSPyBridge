"""
File upload endpoint for training data
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path

router = APIRouter()

TRAIN_DATA_DIR = Path("train-data")
TRAIN_DATA_DIR.mkdir(exist_ok=True)

@router.post("/upload-train-data")
async def upload_train_data(file: UploadFile = File(...)):
    """Upload a file and store it in the train-data directory"""
    try:
        file_location = TRAIN_DATA_DIR / file.filename
        with open(file_location, "wb") as f:
            content = await file.read()
            f.write(content)
        return {"filename": file.filename, "message": "File uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")
